#let info-box(body) = block(
  fill: blue.lighten(92%), stroke: blue.lighten(60%),
  inset: (x: 1em, y: 0.4em), radius: 4pt, width: 100%,
  [ #text(weight: "bold", fill: blue)[提示] #body ],
)
#let emph-box(body, color: blue) = block(
  fill: color.lighten(90%), stroke: color,
  inset: 0.6em, radius: 6pt, width: 100%, body,
)
#let circle-step(n, color) = align(center, {
  block(fill: color.lighten(85%), inset: 0.2em, radius: 50%,
        width: 2em, height: 2em, text(weight: "bold", 1.2em, n))
  v(0.15em)
  []
})
#import "@preview/cetz:0.5.2"
#import "@preview/fletcher:0.5.8" as fletcher: node, edge
#import "@preview/theorion:0.6.0": *
#import "@preview/touying:0.7.4": cols


= 文本排版基础

#text(weight: "thin")[极细] #text(weight: "light")[细]
#text(weight: "regular")[常规] #text(weight: "medium")[中等]
#text(weight: "semibold")[半粗] #text(weight: "bold")[粗]
#text(weight: "extrabold")[特粗] #text(weight: "black")[黑]

#v(0.3em)
组合：#highlight[高亮] #underline[下划线] #strike[删除线]
#text(style: "italic")[斜体] #text(weight: "bold", fill: blue)[蓝色粗体]

#v(0.4em)

+ 无序列表支持无限层级嵌套
  + 嵌套子项 A：补充细节说明
  + 嵌套子项 B：结构化知识体系
1. 需求分析与问题定义
2. 算法设计与复杂度评估
  1. 伪代码编写
  2. 边界条件验证
3. 编码实现与单元测试

#v(0.2em)
#quote(block: true, attribution: [《礼记·中庸》])[
  博学之，审问之，慎思之，明辨之，笃行之。
]


= 数学排版

== 公式排版

行内公式嵌入正文：$a^2 + b^2 = c^2$、$e^(i pi) + 1 = 0$。
块级公式独立居中，适合展示核心结论：

$ integral_0^oo e^(-x^2) dif x = sqrt(pi) / 2 quad frac(d, dif x) sin x = cos x $

多行公式用 `&` 指定对齐点，`\` 换行：

$
  f(x) &= 3x^2 + 2x + 1 \
       &= 3(x^2 + 2/3 x) + 1 \
       &= 3(x + 1/3)^2 + 2/3
$

矩阵通过 `mat` 函数构造，`dots` 系列命令生成不同方向的省略号：

$
  A = mat(a_11, a_12, dots, a_(1 n); dots.v, dots.v, dots.down, dots.v; a_(m 1), a_(m 2), dots, a_(m n))
$

== 定理环境

$
  "ReLU"(x) = cases(x, "当" x > 0, 0, "当" x <= 0) quad
  "sgn"(x) = cases(1, x > 0, 0, x = 0, -1, x < 0)
$

#v(0.3em)
#theorem(title: [定义：质数])[
  大于 $1$ 的自然数，若只有 $1$ 和自身两个正因子则为 #highlight[质数]。前几个质数是 $2,3,5,7,11,13,17,19,dots$。
]
#theorem(title: [欧几里得定理])[质数有无穷多个。]
#proof[
  假设质数有限，列出全部 $p_1,dots,p_n$。构造 $P = product_i p_i + 1$，$P$ 不被任一 $p_i$ 整除，推出 $P$ 为新质数，与假设矛盾。$square$
]
#corollary[不存在最大的质数，且对任意 $n$ 存在至少 $n$ 个质数。]


= 代码与算法

== 分治算法

快速排序是分治法的代表。每轮选取基准值，将数组划分为小于和大于基准的两部分，再对子数组递归执行。平均时间 $O(n log n)$，最坏 $O(n^2)$。

```python
def quick_sort(arr):
    if len(arr) <= 1: return arr
    pivot = arr[len(arr) // 2]
    left  = [x for x in arr if x < pivot]
    mid   = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quick_sort(left) + mid + quick_sort(right)
```

#v(0.2em)
二分查找在有序数组中定位目标，每次将搜索范围折半，时间 $O(log n)$：

```text
BinarySearch(A[0..n-1], target)
1. left ← 0, right ← n - 1
2. while left ≤ right do
3.     mid ← ⌊(left + right) / 2⌋
4.     if A[mid] = target then return mid
5.     else if A[mid] < target then left ← mid + 1
6.     else right ← mid - 1
7. return -1
```


= 表格排版

== 数据展示

#table(
  columns: 4, align: (left, center, center, center),
  table.header([*姓名*], [*语文*], [*数学*], [*英语*]),
  [张三], [95], [87], [92], [李四], [88], [76], [85],
  [王五], [72], [91], [78], [赵六], [90], [88], [95],
)

#v(0.3em)

#figure(
  table(
    columns: (2fr, 1fr, 1fr, 1fr), align: (left, center, center, center),
    table.header([*算法*], [*最优*], [*平均*], [*最坏*]),
    [快速排序], [$n log n$], [$n log n$], [$n^2$],
    [归并排序], [$n log n$], [$n log n$], [$n log n$],
    [堆排序],   [$n log n$], [$n log n$], [$n log n$],
    [插入排序], [$n$],       [$n^2$],     [$n^2$],
    [冒泡排序], [$n$],       [$n^2$],     [$n^2$],
  ),
  caption: [排序算法时间复杂度对比],
)


= 多栏布局

== 多栏展示

#cols(columns: (1fr, 1fr), gutter: 0.8em)[
  #emph-box(color: blue)[
    *迭代法* — 循环结构，空间 $O(1)$\
    注意死循环与边界条件
  ]
][
  #emph-box(color: green)[
    *递归法* — 自调用，代码简洁\
    注意栈溢出与重复计算
  ]
]

#v(0.3em)

#cols(columns: (1fr, 1fr, 1fr), gutter: 0.6em)[
  #align(center, block(fill: blue.lighten(93%), inset: 0.4em, radius: 4pt)[*理论分析* \ 建模推导])
][
  #align(center, block(fill: green.lighten(93%), inset: 0.4em, radius: 4pt)[*算法实现* \ 编码优化])
][
  #align(center, block(fill: orange.lighten(93%), inset: 0.4em, radius: 4pt)[*实验验证* \ 基准对比])
]

#v(0.3em)

#cols(columns: (1fr, 1fr), gutter: 0.8em)[
  机器学习让算法从样本中学习规律，不依赖人工编写规则。ResNet、Transformer、AlphaGo 是不同领域的代表性成果。
][
  #emph-box(color: purple)[
    *学习范式* \
    监督（标签）· 无监督（结构）· 强化（奖励）
  ]
]


= CeTZ 绘图

== 图表与拓扑

#cols(columns: (1fr, 1fr), gutter: 0.8em)[
  #cetz.canvas({
    import cetz.draw: *
    rect((-1.8, 2.5), (1.8, 3.5), fill: blue.lighten(85%), stroke: blue.darken(20%), name: "s")
    content("s", [开始])
    rect((-1.8, 0.3), (1.8, 1.3), fill: blue.lighten(85%), stroke: blue.darken(20%), name: "i")
    content("i", [输入])
    rect((-1.8, -2), (1.8, -1), fill: orange.lighten(85%), stroke: orange.darken(20%), name: "v")
    content("v", [验证])
    rect((-3, -4.5), (-0.5, -3.5), fill: green.lighten(85%), stroke: green.darken(20%), name: "ok")
    content("ok", [成功])
    rect((0.5, -4.5), (3, -3.5), fill: red.lighten(85%), stroke: red.darken(20%), name: "no")
    content("no", [失败])
    line("s", "i"); line("i", "v"); line("v", "ok"); line("v", "no")
  })
][
  #cetz.canvas({
    import cetz.draw: *
    line((-0.6, -4), (-0.6, 0.3), stroke: black)
    line((-0.6, -4), (7.5, -4), stroke: black)
    mark((-0.6, -4), (7.5, -4), symbol: ">")
    mark((-0.6, -4), (-0.6, 0.3), symbol: ">")
    for i in range(5) {
      let y = -4 + i * 0.95
      line((-0.8, y), (-0.6, y))
      if i > 0 { content((-1, y), str(i), anchor: "east") }
    }
    for (x, l, h, c) in ((0.1,"Q1",3.2,blue),(1.8,"Q2",2.5,green),(3.5,"Q3",3.8,orange),(5.2,"Q4",1.7,red)) {
      rect((x, -4), (x + 0.9, -4 + h), fill: c.lighten(70%), stroke: c)
      content((x + 0.45, -4.25), l)
    }
  })
]

#v(0.3em)

#cols(columns: (1fr, 1fr), gutter: 0.8em)[
  #cetz.canvas({
    import cetz.draw: *
    for (pos, n, f) in (
      ((0, 3), "1", blue), ((-2.2, 0.8), "2", blue.lighten(60%)),
      ((2.2, 0.8), "3", blue.lighten(60%)), ((-3.5, -1.5), "4", blue.lighten(30%)),
      ((-0.8, -1.5), "5", blue.lighten(30%)), ((0.8, -1.5), "6", blue.lighten(30%)),
      ((3.5, -1.5), "7", blue.lighten(30%)),
    ) {
      circle(pos, radius: if n.len()==1{0.35}else{0.28}, fill: f, name: n)
      content(n, if f==blue{text(white,n)}else{n})
    }
    line("1","2",stroke:gray); line("1","3",stroke:gray)
    line("2","4",stroke:gray); line("2","5",stroke:gray)
    line("3","6",stroke:gray); line("3","7",stroke:gray)
  })
][
  #cetz.canvas({
    import cetz.draw: *
    circle((0,0), radius: 0.7, fill: blue.darken(30%), name: "c")
    content("c", text(white, [核心]))
    let L = ("A","B","C","D","E","F")
    for (i,l) in L.enumerate() {
      let a = i*60deg; let x=2.5*calc.cos(a); let y=2.5*calc.sin(a)
      circle((x,y), radius: 0.28, fill: blue.lighten(80%), stroke: blue, name: l)
      content((x,y), l); line("c", l, stroke: gray)
    }
    for i in range(6) { line(L.at(i), L.at(calc.rem(i+1,6)), stroke: gray.lighten(40%)) }
  })
]


== 示意图表

#cols(columns: (1.3fr, 1fr), gutter: 0.6em)[
  #fletcher.diagram(
    node-stroke: .06em,
    node-fill: gradient.radial(blue.lighten(85%), blue.lighten(70%), radius: 80%),
    spacing: 5em,
    edge((-1,0),"r","->",[创建]),
    node((0,0),[新建]),
    edge((0,0),(1,0),"->",[打开]),
    node((1,0),[打开]),
    edge((1,0),(2,0),"->",[关闭]),
    node((2,0),[关闭]),
    edge((1,0),(0,-1),"->",[重命名],label-side:right),
    node((0,-1),[重命名]),
    edge((0,-1),(1,0),"->",[完成],label-side:right),
    edge((1,0),(1,-1),"->",[保存]),
    node((1,-1),[保存]),
    edge((1,-1),(2,0),"->",[关闭],label-side:right),
  )
][
  #fletcher.diagram(
    node-stroke: .06em,
    node-fill: gradient.radial(green.lighten(85%), green.lighten(65%), radius: 80%),
    spacing: 1.3em,
    node((0,0),[动物],radius:1.3em),
    edge((0,0),(-1.6,-2),"->",[继承],label-pos:0.35,label-side:center),
    edge((0,0),(1.6,-2),"->",[继承],label-pos:0.35,label-side:center),
    node((-1.6,-2),[哺乳动物],radius:1.3em),
    node((1.6,-2),[鸟类],radius:1.3em),
    edge((-1.6,-2),(-1,-4),"->",label-pos:0.3,label-side:right),
    edge((-1.6,-2),(-2.5,-4),"->",label-pos:0.3,label-side:left),
    node((-1,-4),[猫科],radius:1em),
    node((-2.5,-4),[犬科],radius:1em),
    edge((1.6,-2),(2.5,-4),"->",label-pos:0.3,label-side:right),
    edge((1.6,-2),(0.7,-4),"->",label-pos:0.3,label-side:left),
    node((2.5,-4),[雀形目],radius:1em),
    node((0.7,-4),[鹰形目],radius:1em),
  )
]


= 综合排版示例

== 综合演示

#cols(columns: (1fr, 1fr), gutter: 1em)[
  #align(center, block(fill: luma(240), inset: (y: 1.8em), radius: 6pt,
    stroke: gray, width: 100%, text(fill: gray, size: 0.9em)[[架构示意图]],
  ))
][
  *三层架构*
  - 表示层：用户交互与界面
  - 业务层：规则与流程编排
  - 数据层：持久化存储
  各层职责独立，通过接口通信，修改任一层不影响其他层。
]

#v(0.4em)

#cols(columns: (auto, auto, auto, auto, auto), gutter: 0.15em)[
  #circle-step("1", blue)
  [*需求分析*]
][ #align(center + horizon)[→] ][
  #circle-step("2", green)
  [*方案设计*]
][ #align(center + horizon)[→] ][
  #circle-step("3", orange)
  [*编码实现*]
]
#v(0.2em)
#cols(columns: (auto, auto, auto), gutter: 0.15em)[
  #circle-step("4", purple)
  [*测试验证*]
][ #align(center + horizon)[→] ][
  #circle-step("5", red)
  [*部署上线*]
]
