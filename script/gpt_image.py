import asyncio
import contextlib as ctx
import json
import os
import pathlib as p
import typing as t

import httpx

from tenacity import retry, stop_after_attempt, wait_fixed


ENDPOINT = os.environ["GPT_BASE_URL"]
TIMEOUT = 600


type PathLike = str | p.Path
type Size = t.Literal[
    "auto",
    "1:1",
    "3:2",
    "2:3",
    "16:9",
    "9:16",
    "4:3",
    "3:4",
    "21:9",
    "9:21",
    "1:3",
    "3:1",
    "2:1",
    "1:2",
]


@retry(stop=stop_after_attempt(3), wait=wait_fixed(3.0))
async def generate(
    prompt: str,
    size: Size = "auto",
    files: dict[str, str] = {},
    skip_missing: bool = True,
) -> str:
    async with (
        ctx.AsyncExitStack() as stack,
        httpx.AsyncClient(timeout=TIMEOUT) as client,
    ):
        temp = [
            ("files", (name, stack.enter_context(path.open("rb"))))
            for name, file in files.items()
            if (path := p.Path(file)).exists() or not skip_missing
        ] or None
        data = {"prompt": prompt, "size": size}
        response = await client.post(ENDPOINT, data=data, files=temp)
        return response.raise_for_status().json()


async def download(url: str, path: PathLike) -> None:
    path = p.Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    async with httpx.AsyncClient(timeout=TIMEOUT) as client:
        response = await client.get(url)
        path.write_bytes(response.raise_for_status().content)


async def main() -> None:
    import img2pdf

    root = p.Path(__file__).parent
    prompts: list[str] = json.loads((root / "prompts.json").read_text())
    directory = root / "image"
    directory.mkdir(parents=True, exist_ok=True)
    for ith, prompt in enumerate(prompts):
        path = directory / f"{ith + 1:02d}.png"
        if path.exists():
            continue
        url = await generate(prompt, size="16:9")
        await download(url, path)
    paths = sorted(directory.iterdir())
    (root / "main.pdf").write_bytes(img2pdf.convert(paths))


if __name__ == "__main__":
    asyncio.run(main())
