from RPiMCP23S17.MCP23S17 import MCP23S17
import time
import random
import gc
import threading
import RPi.GPIO as GPIO
from evdev import UInput, ecodes as e, AbsInfo


class Pin():
    PIN_IN = 0
    PIN_OUT = 1

    def __init__(self, pinNr):
        self.pinNr = pinNr
        self.callback = self.stdCallback

    def setupDir(self, direction):
        self.direction = direction
        print('Error: function not overwritten...')

    def setState(self, state):
        self.state = state
        print('Error: function not overwritten...')

    def getState(self):
        print('Error: function not overwritten...')
        return self.state

    def registerCallback(self, callback):
        self.callback = callback
        print('Error: function not overwritten...')

    def stdCallback(self):
        print('Warning: Base callback called')



class PinGPIO(Pin):
    PIN_GPIO_BOUNCETIME = 3

    def __init__(self, pinNr):
        self.pinNr = pinNr
        self.state = False
        self.direction = Pin.PIN_IN,
        GPIO.setmode(GPIO.BOARD)

    def setupDir(self, direction):
        self.direction = direction
        if Pin.PIN_IN == direction:
            GPIO.setup(channel=self.pinNr, direction=GPIO.IN, pull_up_down=GPIO.PUD_UP)
            self.state = GPIO.input(self.pinNr)
        else:
            GPIO.setup(channel=self.pinNr, direction=GPIO.OUT)

    def setState(self, state):
        assert Pin.PIN_OUT == self.direction
        GPIO.output(self.pinNr, state)
        self.state = state

    def getState(self):
        self.state = GPIO.input(self.pinNr)
        return self.state
        
    def registerCallback(self, callback):
        self.callback = callback
        GPIO.add_event_detect(self.pinNr, GPIO.BOTH, callback = self._gpioCallback)

    def _gpioCallback(self, channel):
        state = GPIO.input(self.pinNr)
        if self.state == state:
            return
        self.state = state
        self.callback()

class PinExp(Pin):
    PIN_EXP_SPI_SPEED = 1000000
    PIN_INTERRUPT_GPIO = 37

    def __init__(self, pinNr, expander):
        self.pinNr = pinNr
        self.expander = expander
        self.state = False
        self.direction = Pin.PIN_IN
        
    def setupDir(self, direction):
        self.direction = direction
        if Pin.PIN_IN == self.direction:
            self.expander.setDirection(self.pinNr, MCP23S17.DIR_INPUT)
            self.expander.setPullupMode(self.pinNr, MCP23S17.PULLUP_ENABLED)
        else:
            self.expander.setDirection(self.pinNr, MCP23S17.DIR_OUTPUT)

    def setState(self, state):
        assert Pin.PIN_OUT == self.direction
        self.expander.setPin(self.pinNr, state)
        self.state = state

    def getState(self):
        self.state = self.expander.getPin(self.pinNr)
        return self.state

    def registerCallback(self, callback):
        self.callback = callback
        self.expander.registerInterrupt(self)

    def expCallback(self):
        self.callback(channel=self.pinNr)

class Expander(MCP23S17):
    EXP_WATCH_INTERVAL = 0.01

    def __init__(self, bus, cs, address):
        super().__init__(bus=bus, pin_cs = cs, device_id=address)
        self.interruptPins = []
        self.interruptOccured = False
        self.inputReg = 0x0000
        self.outputReg = 0x0000

    def open(self, speed):
        # opens the serial port with choosen speed (max 10MHz) and starts syncronisaztion thread
        super().open()
        self._spi.max_speed_hz = speed
        self.inputReg = self.readGPIO()
        self._watchdog()
        self._writeRegister(0x02, 0x00)
        self._writeRegister(0x03, 0x00)

    def registerInterrupt(self, pin:PinExp):
        # registrate input pin for interrupt handling
        self.interruptPins.append(pin)

    def _interruptCallback(self, channel):
        self.interruptOccured = True

    def setPin(self, pinNr, state):
        # set or reset single pin of expander. 
        # change gets active after next periodic sync event. (EXP_WATCH_INTERVAL)
        if state:
            self.outputReg |= (1<<pinNr)
        else:
            self.outputReg &= ~(1<<pinNr)

    def getPin(self, pinNr):
        # returns state of pin at PinNr.
        # value gets updated every next periodic sync event.
        if self.inputReg & (1<<pinNr):
            return True
        else:
            return False

    def _watchdog(self):
        # thread for periodicaly synchronize and update the expander
        self.thread = threading.Timer(Expander.EXP_WATCH_INTERVAL, self._watchdog)
        self.thread.start()

        # update inputs
        inputReg = self.readGPIO()
        inputDiff = inputReg ^ self.inputReg
        self.inputReg = inputReg
        
        # call registerd callbacks
        for pin in self.interruptPins:
            if inputDiff & (1<<pin.pinNr):
                pin.expCallback()

        # update outputs
        self.writeGPIO(self.outputReg)

class GamepadInput():
    # input form gamepad
    debounceTime = 0.03
    def __init__(self, input:Pin, name:str, keyCode, keyboard:UInput):
        self.input = input
        self.input.setupDir(Pin.PIN_IN)
        self.input.registerCallback(self.eventCallback)

        self.name = name
        self.keyCode = keyCode
        self.keyboard = keyboard

    def eventCallback(self, channel=0):
        if self.input.getState():
            self.inputReleased()
        else:
            self.inputPressed()

    def inputPressed(self):
        if self.keyboard is not None:
            self.keyboard.write(e.EV_KEY, self.keyCode, 1)
            self.keyboard.syn()
        time.sleep(self.debounceTime)
        Player.lastUsed = time.time()
        Player.endButtonParty()
        print(self.name + ' pressed')

    def inputReleased(self):
        if self.keyboard is not None:
            self.keyboard.write(e.EV_KEY, self.keyCode, 0)
            self.keyboard.syn()
        time.sleep(self.debounceTime)
        Player.lastUsed = time.time()
        Player.endButtonParty()

class Button(GamepadInput):
    # gamepad input with led controll
    def __init__(self, input:Pin, led:Pin, name:str, keyCode, keyboard:UInput):
        super().__init__(input, name, keyCode, keyboard)
        self.led = led
        self.led.setupDir(Pin.PIN_OUT)
        self.led.setState(True)
        self.debounceTime = 0.0005

    def inputPressed(self):
        super().inputPressed()
        self.led.setState(False)

    def inputReleased(self):
        super().inputReleased()
        self.led.setState(True)



class Player():
    
    lastUsed = 0
    activeParty = False

    def __init__(self):
        self.inputs = []
        self.keyboard = None

    def setupKeyboard(self):
        events = []
        for b in self.inputs:
            events.append(b.keyCode)
        self.keyboard = UInput({e.EV_KEY : events, 
                                e.EV_ABS : [(e.ABS_X, AbsInfo(value=0, min=0, max=255, fuzz=0, flat=0, resolution=0)),
                                            (e.ABS_Y, AbsInfo(value=0, min=0, max=255, fuzz=0, flat=0, resolution=0))
                                            ]
                                }, name='ArminsPad')    
                            
        print('device initialized') 
        for b in self.inputs:
            b.keyboard = self.keyboard
            
    def addButton(self, config):
        for buttonConfig in config:
            if buttonConfig['inSource'] != 0:
                inPin = PinExp(buttonConfig['inPin'], buttonConfig['inSource'])
            else:
                inPin = PinGPIO(buttonConfig['inPin'])
            
            if buttonConfig['ledSource'] != 0:
                ledPin = PinExp(buttonConfig['ledPin'], buttonConfig['ledSource']) 
            else:
                ledPin = PinGPIO(buttonConfig['ledPin'])
            
            button = Button(inPin, ledPin, buttonConfig['name'], buttonConfig['keyCode'], self.keyboard)
            self.inputs.append(button)

    def addJoystick(self, config):
        for joy in config:
            inPin = PinGPIO(joy['inPin'])
            a = GamepadInput(inPin, joy['name'], joy['keyCode'], self.keyboard)
            self.inputs.append(a)

    def startButtonParty():
        Player.activeParty = True
        while Player.activeParty:
            for obj in gc.get_objects():
                if isinstance(obj, Player):
                    for b in obj.inputs:
                        if isinstance(b, Button):
                            b.led.setState(bool(random.getrandbits(1)))
            time.sleep(0.5)

    def endButtonParty():
        if not Player.activeParty:
            return
        Player.activeParty = False
        time.sleep(0.05)
        for obj in gc.get_objects():
            if isinstance(obj, Player):
                for b in obj.inputs:
                    if isinstance(b, Button):
                        b.led.setState(True)

        
    

if __name__ == "__main__":
    GPIO.setmode(GPIO.BOARD)
    exp0 = Expander(0, 0, 0)
    exp1 = Expander(0, 1, 4)
    exp0.open(10000000)
    exp1.open(10000000)

    buttonPlayer0 = [
        {'inPin' : 0,    'inSource' : exp0,  'ledPin' : 1,   'ledSource' : exp0,    'keyCode' : e.BTN_START,     'name' : 'select'  }, 
        {'inPin' : 2,    'inSource' : exp0,  'ledPin' : 3,   'ledSource' : exp0,    'keyCode' : e.BTN_SELECT,    'name' : 'start'   },
        {'inPin' : 8,    'inSource' : exp0,  'ledPin' : 9,   'ledSource' : exp0,    'keyCode' : e.BTN_BASE,      'name' : 'home'    },
        {'inPin' : 7,    'inSource' : exp0,  'ledPin' : 6,   'ledSource' : exp0,    'keyCode' : e.BTN_MIDDLE,    'name' : 'res'     },
        {'inPin' : 15,   'inSource' : 0,     'ledPin' : 7,   'ledSource' : exp1,    'keyCode' : e.BTN_A,         'name' : 'a'       }, 
        {'inPin' : 11,   'inSource' : 0,     'ledPin' : 5,   'ledSource' : exp1,    'keyCode' : e.BTN_B,         'name' : 'b'       }, 
        {'inPin' : 13,   'inSource' : 0,     'ledPin' : 6,   'ledSource' : exp1,    'keyCode' : e.BTN_X,         'name' : 'x'       }, 
        {'inPin' : 7,    'inSource' : 0,     'ledPin' : 4,   'ledSource' : exp1,    'keyCode' : e.BTN_Y,         'name' : 'y'       }, 
        {'inPin' : 3,    'inSource' : 0,     'ledPin' : 2,   'ledSource' : exp1,    'keyCode' : e.BTN_TL,        'name' : 'r'       }, 
        {'inPin' : 5,    'inSource' : 0,     'ledPin' : 3,   'ledSource' : exp1,    'keyCode' : e.BTN_TR,        'name' : 'l'       }  
    ]

    joyStickPlayer0 = [
        {'inPin' : 32, 'keyCode' : e.BTN_DPAD_UP    , 'name' : 'up'     },   
        {'inPin' : 40, 'keyCode' : e.BTN_DPAD_DOWN  , 'name' : 'down'   },  
        {'inPin' : 36, 'keyCode' : e.BTN_DPAD_LEFT  , 'name' : 'left'   },  
        {'inPin' : 38, 'keyCode' : e.BTN_DPAD_RIGHT , 'name' : 'right'  }   
    ]

    player0 = Player()
    player0.addButton(buttonPlayer0)
    player0.addJoystick(joyStickPlayer0)
    player0.setupKeyboard()

    buttonPlayer1 = [
        {'inPin' : 12,   'inSource' : exp0,  'ledPin' : 13,  'ledSource' : exp0,     'keyCode' : e.BTN_SELECT,    'name' : 'select' },
        {'inPin' : 10,   'inSource' : exp0,  'ledPin' : 11,  'ledSource' : exp0,     'keyCode' : e.BTN_START,     'name' : 'start'  },
        {'inPin' : 4,    'inSource' : exp0,  'ledPin' : 5,   'ledSource' : exp0,     'keyCode' : e.BTN_BASE,      'name' : 'home'   },
        {'inPin' : 8,    'inSource' : 0,     'ledPin' : 13,  'ledSource' : exp1,     'keyCode' : e.BTN_A,         'name' : 'a'      },
        {'inPin' : 12,   'inSource' : 0,     'ledPin' : 11,  'ledSource' : exp1,     'keyCode' : e.BTN_B,         'name' : 'b'      }, 
        {'inPin' : 10,   'inSource' : 0,     'ledPin' : 12,  'ledSource' : exp1,     'keyCode' : e.BTN_X,         'name' : 'x'      }, 
        {'inPin' : 16,   'inSource' : 0,     'ledPin' : 10,  'ledSource' : exp1,     'keyCode' : e.BTN_Y,         'name' : 'y'      }, 
        {'inPin' : 22,   'inSource' : 0,     'ledPin' : 8,   'ledSource' : exp1,     'keyCode' : e.BTN_TL,        'name' : 'r'      },
        {'inPin' : 18,   'inSource' : 0,     'ledPin' : 9,   'ledSource' : exp1,     'keyCode' : e.BTN_TR,        'name' : 'l'      }
    ]

    joyStickPlayer1 = [
        {'inPin' : 31, 'keyCode' : e.BTN_DPAD_UP    , 'name' : 'up'     },   
        {'inPin' : 33, 'keyCode' : e.BTN_DPAD_DOWN  , 'name' : 'down'   },
        {'inPin' : 29, 'keyCode' : e.BTN_DPAD_LEFT  , 'name' : 'left'   },  
        {'inPin' : 35, 'keyCode' : e.BTN_DPAD_RIGHT , 'name' : 'right'  }  
    ]

    #{'inPin' : 35, 'keyCode' : test , 'name''down' : 33, 'left' : 31, 'right' : 29}

    player1 = Player()
    player1.addButton(buttonPlayer1)
    player1.addJoystick(joyStickPlayer1)
    player1.setupKeyboard()


    while True:
        time.sleep(0.2)
        if Player.lastUsed < time.time() - 10 :
            if not Player.activeParty:
                print('party active')
                t0 = threading.Thread(target=Player.startButtonParty)
                t0.start()

        elif Player.activeParty:
            Player.endButtonParty()
            print('party end')

