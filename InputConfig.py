SOURCE_RPI = 0
SOURCE_EXP0 = 1
SOURCE_EXP1 = 2

TYPE_BUTTON = 0
TYPE_JOYSTICK = 0

# Setup Player0
################################
Player0_A = {
    'name' : 'Button A Player0',
    'type' : TYPE_BUTTON,
    'input' : {
        'source' : SOURCE_RPI,
        'pinNr' : 2
    },
    'led' : {
        'source' : SOURCE_EXP1,
        'pinNr' : 2
    }
}

Player0_B = {
    'name' : 'Button B Player0',
    'type' : TYPE_BUTTON,
    'input' : {
        'source' : SOURCE_RPI,
        'pinNr' : 3
    },
    'led' : {
        'source' : SOURCE_EXP1,
        'pinNr' : 3
    }
}

Player0_X = {
    'name' : 'Button X Player0',
    'type' : TYPE_BUTTON,
    'input' : {
        'source' : SOURCE_RPI,
        'pinNr' : 4
    },
    'led' : {
        'source' : SOURCE_EXP1,
        'pinNr' : 4
    }
}

Player0_Y = {
    'name' : 'Button Y Player0',
    'type' : TYPE_BUTTON,
    'input' : {
        'source' : SOURCE_RPI,
        'pinNr' : 17
    },
    'led' : {
        'source' : SOURCE_EXP1,
        'pinNr' : 5
    }
}

Player0_L = {
    'name' : 'Button L Player0',
    'type' : TYPE_BUTTON,
    'input' : {
        'source' : SOURCE_RPI,
        'pinNr' : 27
    },
    'led' : {
        'source' : SOURCE_EXP1,
        'pinNr' : 6
    }
}

Player0_R = {
    'name' : 'Button R Player0',
    'type' : TYPE_BUTTON,
    'input' : {
        'source' : SOURCE_RPI,
        'pinNr' : 22
    },
    'led' : {
        'source' : SOURCE_EXP1,
        'pinNr' : 7
    }
}

Player0_Select = {
    'name' : 'Button Select Player0',
    'type' : TYPE_BUTTON,
    'input' : {
        'source' : SOURCE_EXP0,
        'pinNr' : 12
    },
    'led' : {
        'source' : SOURCE_EXP0,
        'pinNr' : 13
    }
}

Player0_Start = {
    'name' : 'Button Start Player0',
    'type' : TYPE_BUTTON,
    'input' : {
        'source' : SOURCE_EXP0,
        'pinNr' : 10
    },
    'led' : {
        'source' : SOURCE_EXP0,
        'pinNr' : 11
    }
}

Player0_Joystick = {
    'name' : 'Joystick Player0',
    'type' : TYPE_JOYSTICK,
    'up' : {
        'source' : SOURCE_RPI,
        'pinNr' : 19
    },
    'down' : {
        'source' : SOURCE_RPI,
        'pinNr' : 13
    },
    'left' : {
        'source' : SOURCE_RPI,
        'pinNr' : 6
    },
    'right' : {
        'source' : SOURCE_RPI,
        'pinNr' : 5
    }
}

Player0 = {
    'a' : Player0_A,
    'b' : Player0_B,
    'x' : Player0_X,
    'y' : Player0_Y,
    'l' : Player0_L,
    'r' : Player0_R,
    'joystick' : Player0_Joystick
}

# Setup Player1
################################
Player1_A = {
    'name' : 'Button A Player1',
    'type' : TYPE_BUTTON,
    'input' : {
        'source' : SOURCE_RPI,
        'pinNr' : 14
    },
    'led' : {
        'source' : SOURCE_EXP1,
        'pinNr' : 13
    }
}

Player1_B = {
    'name' : 'Button B Player1',
    'type' : TYPE_BUTTON,
    'input' : {
        'source' : SOURCE_RPI,
        'pinNr' : 15
    },
    'led' : {
        'source' : SOURCE_EXP1,
        'pinNr' : 12
    }
}

Player1_X = {
    'name' : 'Button X Player1',
    'type' : TYPE_BUTTON,
    'input' : {
        'source' : SOURCE_RPI,
        'pinNr' : 18
    },
    'led' : {
        'source' : SOURCE_EXP1,
        'pinNr' : 11
    }
}

Player1_Y = {
    'name' : 'Button Y Player1',
    'type' : TYPE_BUTTON,
    'input' : {
        'source' : SOURCE_RPI,
        'pinNr' : 23
    },
    'led' : {
        'source' : SOURCE_EXP1,
        'pinNr' : 10
    }
}

Player1_L = {
    'name' : 'Button L Player1',
    'type' : TYPE_BUTTON,
    'input' : {
        'source' : SOURCE_RPI,
        'pinNr' : 24
    },
    'led' : {
        'source' : SOURCE_EXP1,
        'pinNr' : 8
    }
}

Player1_R = {
    'name' : 'Button R Player1',
    'type' : TYPE_BUTTON,
    'input' : {
        'source' : SOURCE_RPI,
        'pinNr' : 25
    },
    'led' : {
        'source' : SOURCE_EXP1,
        'pinNr' : 9
    }
}

Player1_Select = {
    'name' : 'Button Select Player1',
    'type' : TYPE_BUTTON,
    'input' : {
        'source' : SOURCE_EXP0,
        'pinNr' : 0
    },
    'led' : {
        'source' : SOURCE_EXP0,
        'pinNr' : 1
    }
}

Player1_Start = {
    'name' : 'Button Start Player1',
    'type' : TYPE_BUTTON,
    'input' : {
        'source' : SOURCE_EXP0,
        'pinNr' : 2
    },
    'led' : {
        'source' : SOURCE_EXP0,
        'pinNr' : 3
    }
}

Player1_Joystick = {
    'name' : 'Joystick Player1',
    'type' : TYPE_JOYSTICK,
    'up' : {
        'source' : SOURCE_RPI,
        'pinNr' : 2
    },
    'down' : {
        'source' : SOURCE_RPI,
        'pinNr' : 2
    },
    'left' : {
        'source' : SOURCE_RPI,
        'pinNr' : 3
    },
    'right' : {
        'source' : SOURCE_RPI,
        'pinNr' : 3
    }
}

Player1 = {
    'a' : Player1_A,
    'b' : Player1_B,
    'x' : Player1_X,
    'y' : Player1_Y,
    'l' : Player1_L,
    'r' : Player1_R,
    'joystick' : Player1_Joystick
}
