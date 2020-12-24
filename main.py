function modeReceiver () {
    if (stage >= 0) {
        basic.showString(" " + stageNames[stage])
        icons[stage].showImage(0)
    } else {
        basic.showIcon(IconNames.No)
    }
    basic.pause(2000)
}
function modeSender () {
    for (let index = 0; index <= icons.length - 2; index++) {
        pos = index
        stage = pos
        icons[pos].showImage(0)
        basic.pause(delays)
    }
    for (let index = 0; index <= icons.length - 2; index++) {
        pos = icons.length - index - 1
        stage = pos
        icons[pos].showImage(0)
        basic.pause(delays)
    }
}
input.onButtonPressed(Button.A, function () {
    mode = 1
    radio.sendValue("mode", mode)
    basic.showArrow(ArrowNames.West)
    basic.pause(2000)
})
input.onButtonPressed(Button.B, function () {
    stage = 0
    radio.sendValue("stage", stage)
    basic.showArrow(ArrowNames.East)
    basic.pause(2000)
})
radio.onReceivedValue(function (name, value) {
    serial.writeString("Received ")
    serial.writeString(name)
    serial.writeString(" = ")
    serial.writeLine("" + value)
    if (name == "mode") {
        if (value == 1) {
            mode = 2
        } else {
            mode = 1
        }
    } else if (name == "stage") {
        stage = value
        serial.writeString("Received stage: ")
        serial.writeString("" + (stage))
        serial.writeString(" => ")
        serial.writeLine("" + (stageNames[stage]))
    }
})
let pos = 0
let stageNames: string[] = []
let icons: Image[] = []
let stage = 0
let mode = 0
let delays = 0
basic.showLeds(`
    . # # # .
    # . . . #
    # . . . #
    # . . . #
    . # # # .
    `)
serial.writeString(control.deviceName())
serial.writeString("@")
serial.writeString("" + (control.deviceSerialNumber()))
radio.setGroup(2)
delays = 1800
mode = 0
stage = 0
icons = []
stageNames = []
let allStages: Image[][] = []
allStages.push([images.iconImage(IconNames.SmallDiamond), "Piece"])
icons.push(images.iconImage(IconNames.SmallDiamond))
stageNames.push("Piece")
icons.push(images.iconImage(IconNames.Diamond))
stageNames.push("Etoile")
icons.push(images.iconImage(IconNames.Target))
stageNames.push("Rond")
icons.push(images.iconImage(IconNames.Chessboard))
stageNames.push("Explosion")
basic.forever(function () {
    serial.writeString("Mode: ")
    serial.writeLine("" + mode)
    if (mode == 1) {
        modeSender()
    } else if (mode == 2) {
        modeReceiver()
    }
})
control.inBackground(function () {
    while (true) {
        if (mode == 0) {
            mode = 1
            serial.writeString("Send Mode: ")
            serial.writeLine("" + (mode))
            radio.sendValue("mode", 1)
        } else {
            serial.writeString("Send Mode: ")
            serial.writeLine("" + (mode))
            radio.sendValue("mode", mode)
        }
        basic.pause(3500)
    }
})
control.inBackground(function () {
    while (true) {
        if (mode == 1) {
            basic.pause(2000)
            serial.writeString("Sending stage: ")
            serial.writeLine("" + (stage))
            radio.sendValue("stage", stage)
            basic.showArrow(ArrowNames.North)
            basic.pause(11000)
        } else if (mode == 2) {
            basic.pause(5000)
        }
    }
})
