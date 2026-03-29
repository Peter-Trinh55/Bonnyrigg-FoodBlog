const screenWidth = 854
const columnWidth = 38

const maniaKeyColors = [
  { keys: 1, colors: `blue` },
  { keys: 2, colors: `blue green` },
  { keys: 3, colors: `blue green blue` },
  { keys: 4, colors: `blue green green blue` },
  { keys: 5, colors: `blue white green white blue` },
  { keys: 6, colors: `blue green blue blue green blue` },
  { keys: 7, colors: `blue green blue white blue green blue` },
  { keys: 8, colors: `yellow blue green blue white blue green blue` },
  { keys: 9, colors: `yellow blue green blue white blue green blue yellow` }
]

const columnBackColors = {
  green: `9, 17, 13, 230`,
  blue: `7, 18, 22, 230`,
  white: `2, 5, 6, 230`,
  yellow: `22, 17, 7, 230`
}

const maniaColumn = (color, index) => `
NoteImage${index}: mania/${color}
NoteImage${index}H: mania/${color}
NoteImage${index}L: mania/hold-${color}
NoteImage${index}T: _blank
KeyImage${index}: mania/key-${color}
KeyImage${index}D: mania/key-held-${color}
Colour${index + 1}: ${columnBackColors[color]}
`

const range = (length, value) =>
  [...Array(length)].map((_, index) => (value != null ? value : index))

const infixComma = (length, value) => range(length, value).join(",")

const maniaSection = config => `
[Mania]
Keys: ${config.keys}

JudgementLine: 0
BarLine: 0
BarlineWidth: 4
ColourBarline: 255,255,255,80

ScorePosition: 260
ComboPosition: 205

ColumnStart: ${screenWidth / 2 - (config.keys * columnWidth) / 2}
ColumnWidth: ${infixComma(config.keys, columnWidth)}
ColumnLineWidth: ${infixComma(config.keys + 1, 0)}
HitPosition: 418
LightPosition: 418

${config.colors
  .split(" ")
  .map(maniaColumn)
  .join("")}
`

const header = `
[General]
Name: Blueberry
Author: Enitoni
Version: 2.5

// Color codes
// Primary: 00baff
// Accent: 00ff90

SliderBallFlip: 0
CursorRotate: 0
//CursorTrailRotate: 0
CursorExpand: 0
CursorCentre: 1
SliderBallFrames: 10
//SpinnerFadePlayfield: 1
ComboBurstRandom : 0
HitCircleOverlayAboveNumer: 1
AllowSliderBallTint: 0
//AnimationFramerate: 10
//CustomComboBurstSounds: 30,60,100,150,200,250,300
//SliderStyle: 1

[Colours]
InputOverlayText: 255,255,255
MenuGlow: 0,255,144

//You can add up to 8 colours.
Combo1: 0,186,255
Combo2: 0,255,144

SliderBorder: 255,255,255
SliderTrackOverride: 0,0,0
//SpinnerApproachCircle: 77,139,217
SongSelectActiveText: 255,255,255
//SongSelectInactiveText: 255,255,255
//StarBreakAdditive: 0,0,0

[Fonts]
HitCirclePrefix: default
HitCircleOverlap: 3

ScorePrefix: score
ScoreOverlap: 3
`

const skinContent = `
${header}
${maniaKeyColors.map(maniaSection).join("")}
`

console.log(skinContent)
