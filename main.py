def modeReceiver():
    basic.show_string(" " + stage)
    if stage == "Piece":
        basic.show_icon(IconNames.SMALL_DIAMOND)
    elif stage == "Etoile":
        basic.show_icon(IconNames.TARGET)
    elif stage == "Rond":
        basic.show_icon(IconNames.DIAMOND)
    elif stage == "Explosion":
        basic.show_icon(IconNames.CHESSBOARD)
    else:
        basic.show_icon(IconNames.NO)
    basic.pause(2000)
def modeSender():
    global stage
    stage = "Piece"
    basic.show_icon(IconNames.SMALL_DIAMOND)
    basic.pause(delays)
    stage = "Etoile"
    basic.show_icon(IconNames.TARGET)
    basic.pause(delays)
    stage = "Rond"
    basic.show_icon(IconNames.DIAMOND)
    basic.pause(delays)
    stage = "Explosion"
    basic.show_icon(IconNames.CHESSBOARD)
    basic.pause(delays)
    stage = "Rond"
    basic.show_icon(IconNames.DIAMOND)
    basic.pause(delays)
    stage = "Etoile"
    basic.show_icon(IconNames.TARGET)
    basic.pause(delays)

def on_button_pressed_a():
    global mode
    mode = 1
    radio.send_value("mode", mode)
    basic.show_arrow(ArrowNames.SOUTH)
    basic.pause(2000)
input.on_button_pressed(Button.A, on_button_pressed_a)

def on_received_string(receivedString):
    global stage
    if mode == 2:
        stage = receivedString
        serial.write_string("Received stage: ")
        serial.write_line(stage)
radio.on_received_string(on_received_string)

def on_received_value(name, value):
    global mode
    serial.write_string("Received ")
    serial.write_string(name)
    serial.write_string(" = ")
    serial.write_line("" + str((value)))
    if name == "mode":
        if value == 1:
            mode = 2
        else:
            mode = 1
radio.on_received_value(on_received_value)

stage = ""
delays = 0
mode = 0
basic.show_leds("""
    . # # # .
    # . . . #
    # . . . #
    # . . . #
    . # # # .
    """)
radio.set_group(2)
mode = 0
delays = 1800
stage = ""
if input.button_is_pressed(Button.B):
    mode = 2

def on_forever():
    serial.write_string("Mode:")
    serial.write_line("" + str((mode)))
    if mode == 1:
        modeSender()
    elif mode == 2:
        modeReceiver()
basic.forever(on_forever)

def on_in_background():
    global mode
    while True:
        if mode == 0:
            mode = 1
            serial.write_string("Send Mode: ")
            serial.write_line("" + str((mode)))
            radio.send_value("mode", 1)
        else:
            serial.write_string("Send Mode: ")
            serial.write_line("" + str((mode)))
            radio.send_value("mode", mode)
        basic.pause(3500)
control.in_background(on_in_background)

def on_in_background2():
    while True:
        if mode == 1:
            basic.pause(5000)
            serial.write_string("Sending stage: ")
            serial.write_line(stage)
            radio.send_string(stage)
            basic.show_arrow(ArrowNames.NORTH)
            basic.pause(2000)
        elif mode == 2:
            break
control.in_background(on_in_background2)
