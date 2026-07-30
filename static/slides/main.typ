#import "@preview/cetz:0.5.2"
#import "@preview/fletcher:0.5.8" as fletcher: node, edge
#import "@preview/numbly:0.1.0": numbly
#import "@preview/theorion:0.6.0": *
#import "@preview/touying:0.7.4": *
#import themes.university: *

#show: show-theorion

#show: university-theme.with(
  aspect-ratio: "16-9",
  config-common(),
  config-methods(
    init: (self: none, body) => {
      set text(size: 18pt)
      show heading.where(level: 3): set text(fill: self.colors.primary)
      show heading.where(level: 4): set text(fill: self.colors.primary)
      body
    },
    alert: utils.alert-with-primary-color,
  ),
  header-right: self => box(utils.display-current-heading(level: 1)),
  config-colors(
    primary: rgb("#3F67B8"),
    primary-light: rgb("#6089CC"),
    primary-dark: rgb("#2D4F96"),
    secondary: rgb("#2D5AA0"),
    tertiary: rgb("#6089CC"),
  ),
  config-info(
    title: [$title],
    subtitle: [$part],
    author: [金融科技教研部],
    date: datetime.today(),
    logo: image("logo.png", height: 1em),
  ),
)

#set text(font: ("Alibaba PuHuiTi 3.0", "Fira Code"), lang: "zh")
#set par(leading: 0.55em, first-line-indent: 0pt)
#show raw.where(block: true): it => block(
  fill: luma(240), inset: (x: 0.8em, y: 0.5em), radius: 4pt, width: 100%, it,
)

#title-slide()

= 目 录
#outline(indent: 1em, depth: 1)

#include "section.typ"

= 谢谢

#v(2.5em)
#align(center)[
  #text(size: 2.2em, weight: "bold")[感谢聆听]
  #v(0.6em)
  #text(size: 1em, fill: gray)[欢迎提出宝贵意见与问题]
  #v(1em)
  #line(length: 30%, stroke: gray.lighten(50%))
  #v(0.4em)
  #text(size: 0.75em, fill: gray)[联系方式：contact\@digquant.com]
]
