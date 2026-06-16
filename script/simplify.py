from courseforge.util.astral_uv import AstralUv


uv = AstralUv.fromDefault()
for name, pkgs in uv.get_redundants().items():
    if not pkgs:
        continue
    info = "[{}] uv remove {}".format(name, " ".join(sorted(pkgs)))
    print(info)
