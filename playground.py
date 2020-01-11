from RPiMCP23S17.MCP23S17 import MCP23S17
import time
import RPi.GPIO as GPIO
import uinput
from InputConfig import Player0

GPIO.setmode(GPIO.BOARD)
GPIO.setup(channel=3, direction=GPIO.IN, pull_up_down=GPIO.PUD_UP)

state = False

def pushed(channel):
    global state
    if GPIO.input(channel) == GPIO.LOW and state == False:
        print('push detected! ' + str(channel) + ' ' + str(GPIO.input(channel)))
        state = True

def released(channel):
    global state
    if GPIO.input(channel) == GPIO.HIGH and state == True:
        print('release detected! ' + str(channel) + ' ' + str(GPIO.input(channel)))
        state = False

GPIO.add_event_detect(3, GPIO.BOTH, bouncetime=3)
GPIO.add_event_callback(3, pushed)
GPIO.add_event_callback(3, released)

mcp2 = MCP23S17(bus=0x00, pin_cs=0x01, device_id=0x04)
mcp2.open()
mcp2._spi.max_speed_hz=1000000

for x in range(0, 16):
    mcp2.setDirection(x, MCP23S17.DIR_OUTPUT)

mcp2.setDirection(2, MCP23S17.DIR_OUTPUT)
mcp2.digitalWrite(2, MCP23S17.LEVEL_HIGH)

GP0 = uinput.Device([uinput.KEY_A])
GP1 = uinput.Device([uinput.KEY_1])

try:
    while True:
        pass
    
except KeyboardInterrupt:
    GPIO.cleanup()
    print('Bye')
    GPIO.setmode(GPIO.BOARD)
    GPIO.remove_event_detect(3)


# mcp1 = MCP23S17(bus=0x00, pin_cs=0x00, device_id=0x00)
# mcp2 = MCP23S17(bus=0x00, pin_cs=0x01, device_id=0x04)
# mcp1.open()
# mcp2.open()

# mcp1._spi.max_speed_hz=1000000
# mcp2._spi.max_speed_hz=1000000

# inputMCP1 = [0, 2, 4, 7, 8, 10, 12, 14, 15]
# outputMCP1 = {1, 3, 5, 6, 9, 11, 13}


# for x in range(0, 16):
#     mcp1.setDirection(x, mcp1.DIR_OUTPUT)
#     mcp2.setDirection(x, mcp1.DIR_OUTPUT)

# print("Starting blinky on all pins (CTRL+C to quit)")
# while (True):
#     for x in range(0, 16):
#         mcp1.digitalWrite(x, MCP23S17.LEVEL_HIGH)
#         mcp2.digitalWrite(x, MCP23S17.LEVEL_HIGH)
#     time.sleep(1)

#     for x in range(0, 16):
#         mcp1.digitalWrite(x, MCP23S17.LEVEL_LOW)
#         mcp2.digitalWrite(x, MCP23S17.LEVEL_LOW)
#     time.sleep(1)

#     # the lines below essentially have the same effect as the lines above
#     mcp1.writeGPIO(0xFFFF)
#     mcp2.writeGPIO(0xFFFF)
#     time.sleep(1)

#     mcp1.writeGPIO(0x0)
#     mcp2.writeGPIO(0x0)
#     time.sleep(1)