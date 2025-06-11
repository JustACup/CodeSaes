import board
import time
import lib.maintenance as mt
from lib.timer import TON
from digitalio import DigitalInOut, Direction, Pull

# Config des GPIO

FeuVert = DigitalInOut(board.GP16)
FeuVert.direction = Direction.OUTPUT

FeuOrange = DigitalInOut(board.GP17)
FeuOrange.direction = Direction.OUTPUT

FeuRouge = DigitalInOut(board.GP18)
FeuRouge.direction = Direction.OUTPUT

Feu2Vert = DigitalInOut(board.GP27)
Feu2Vert.direction = Direction.OUTPUT

Feu2Orange = DigitalInOut(board.GP26)
Feu2Orange.direction = Direction.OUTPUT

Feu2Rouge = DigitalInOut(board.GP22)
Feu2Rouge.direction = Direction.OUTPUT

FeuJour = DigitalInOut(board.LED)
FeuJour.direction = Direction.OUTPUT

BpMag = DigitalInOut(board.GP20)
BpMag.direction = Direction.INPUT
BpMag.pull = Pull.UP

BpP1 = DigitalInOut(board.GP14)
BpP1.direction = Direction.INPUT
BpP1.pull = Pull.UP

BpP2 = DigitalInOut(board.GP19)
BpP2.direction = Direction.INPUT
BpP2.pull = Pull.UP

# initialisation des étapes

X1 = 1
X2 = 0

X5 = 1
X6 = 0

X10 = 1
X20 = 0
X30 = 0
X40 = 0
X50 = 0
X60 = 0
X70 = 0

X100 = 1
X110 = 0

Timer1 = TON()
Timer2 = TON()
Timer3 = TON()
Timer4 = TON()
Timer5 = TON()
Timer6 = TON()

listeTempos = [5,1,1,5,1,1]
modes = ["jour","nuit","jour/nuit"]

TimerJour = TON()
TimerNuit = TON()

TimerP1 = TON()
TimerP2 = TON()

while True:

    # Mise à jour du timer

    Timer1.maj(listeTempos[0])
    Timer2.maj(listeTempos[1])
    Timer3.maj(listeTempos[2])
    Timer4.maj(listeTempos[3])
    Timer5.maj(listeTempos[4])
    Timer6.maj(listeTempos[5])

    TimerJour.maj(20)
    TimerNuit.maj(20)

    TimerP1.maj(0.5)
    TimerP2.maj(0.5)

    # Les conditions dévolution

    CE1_2 = (mt.panne == 0)
    CE2_1 = (mt.panne == 1)

    CE5_6 = TimerP1.Q and X5 and X1
    CE6_5 = (TimerP2.Q and X6) or X2

    CE10_20 = X2 and X10
    CE20_30 = (Timer1.Q and X20 and X100) or BpMag.value == False or BpP1.value == False or BpP2.value == False or X1
    CE30_40 = (Timer2.Q or X1) and X30
    CE40_50 = (Timer3.Q or X1) and X40
    CE50_60 = (Timer4.Q or X1) and X50
    CE60_70 = (Timer5.Q or X1) and X60
    CE70_20 = Timer6.Q and X70 and X2
    CE70_10 = X70 and X1

    CE100_110 = (TimerJour.Q and X100 and (mt.indexMenu == 2)) or mt.indexMenu == 1
    CE110_100 = (TimerNuit.Q and X110 and (mt.indexMenu == 2)) or mt.indexMenu == 0

    # étapes

    if CE1_2 :
        X1 = 0
        X2 = 1
    if CE2_1 :
        X2 = 0
        X1 = 1

    if CE5_6 :
        X5 = 0
        X6 = 1
    if CE6_5 :
        X6 = 0
        X5 = 1

    if CE10_20:
        X20 =1
        X10 =0
    if CE20_30 :
        X30 = 1
        X20 = 0
    if CE30_40 :
        X30 = 0
        X40 = 1
    if CE40_50 :
        X40 = 0
        X50 = 1
    if CE50_60 :
        X50 = 0
        X60 = 1
    if CE60_70 :
        X60 = 0
        X70 = 1
    if CE70_20 :
        X70 = 0
        X20 = 1
    if CE70_10 :
        X70 = 0
        X10 = 1

    if CE100_110 :
        X100 = 0
        X110 = 1
    if CE110_100 :
        X110 = 0
        X100 = 1

    # Les actions

    TimerP1.IN = X5
    TimerP2.IN = X6

    Timer1.IN = FeuVert.value = X20
    Timer2.IN = X30
    Timer3.IN = X40
    Timer4.IN = Feu2Vert.value = X50
    Timer5.IN = X60
    Timer6.IN = X70

    Feu2Rouge.value = X20 or X30 or X40 or X70
    FeuRouge.value = X40 or X50 or X60 or X70

    FeuOrange.value = X6 or X30
    Feu2Orange.value = X6 or X60
    
    TimerJour.IN = FeuJour.value = X100
    TimerNuit.IN = X110

    # Affichage

    mt.config_feux(listeTempos,modes)
