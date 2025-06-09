import board
import time
from timer import TON
from digitalio import DigitalInOut, Direction, Pull
from maintenance import config_feux, val_panne

## configuration des entrées sorties

Feu1Vert = DigitalInOut(board.GP16)
Feu1Vert.direction = Direction.OUTPUT

Feu1Orange = DigitalInOut(board.GP17)
Feu1Orange.direction = Direction.OUTPUT

Feu1Rouge = DigitalInOut(board.GP18)
Feu1Rouge.direction = Direction.OUTPUT

Feu2Vert = DigitalInOut(board.GP27)
Feu2Vert.direction = Direction.OUTPUT

Feu2Orange = DigitalInOut(board.GP26)
Feu2Orange.direction = Direction.OUTPUT

Feu2Rouge = DigitalInOut(board.GP22)
Feu2Rouge.direction = Direction.OUTPUT

LedJour = DigitalInOut(board.LED)
LedJour.direction = Direction.OUTPUT


BP_Pieton1 = DigitalInOut(board.GP14)
BP_Pieton1.direction = Direction.INPUT
BP_Pieton1.pull = Pull.UP

BP_Pieton2 = DigitalInOut(board.GP19)
BP_Pieton2.direction = Direction.INPUT
BP_Pieton2.pull = Pull.UP

BoucleMag = DigitalInOut(board.GP20)
BoucleMag.direction = Direction.INPUT
BoucleMag.pull = Pull.UP

BP_Menu = DigitalInOut(board.GP12)
BP_Menu.direction = Direction.INPUT
BP_Menu.pull = Pull.UP

BP_Plus = DigitalInOut(board.GP13)
BP_Plus.direction = Direction.INPUT
BP_Plus.pull = Pull.UP

BP_Moins = DigitalInOut(board.GP11)
BP_Moins.direction = Direction.INPUT
BP_Moins.pull = Pull.UP


Timer1Vert = TON()
Timer1Orange = TON()
Timer1Rouge = TON()

Timer2Vert = TON()
Timer2Orange = TON()
Timer2Rouge = TON()

TimerC1 = TON()
TimerC2 = TON()

TimerJour = TON()
TimerNuit = TON()


X0 = 1
X1 = 1
X10 = 0
X100 = 1
X1000 = 1
X2 = 0
X20 = 0
X200 = 0
X2000 = 0
X30 = 0
X40 = 0
X50 = 0
X60 = 0

liste_duree = [5,1,1,5,1,1]
mod = ["jour/nuit", "jour", "nuit"]

while True:
    panne = val_panne()
    index, liste_duree, deroulement = config_feux(BP_Menu, BP_Plus, BP_Moins, liste_duree, mod,panne)

    Timer1Vert.maj(liste_duree[0])
    Timer1Orange.maj(liste_duree[1])
    Timer1Rouge.maj(liste_duree[2])

    Timer2Vert.maj(liste_duree[3])
    Timer2Orange.maj(liste_duree[4])
    Timer2Rouge.maj(liste_duree[5])

    TimerC1.maj(0.5)
    TimerC2.maj(0.5)

    TimerJour.maj(20)
    TimerNuit.maj(20)

    #les conditions d'évolution
    CE0_10 = X2 and X0
    CE10_20 = Timer1Vert.Q and X10 and (X100 or not BP_Pieton1.value or not BP_Pieton2.value or not BoucleMag.value or X1)

    CE20_30 = (Timer1Orange.Q or X1) and X20
    CE30_40 = (Timer1Rouge.Q or X1) and X30
    CE40_50 = (Timer2Vert.Q or X1) and X40
    CE50_60 = (Timer2Orange.Q or X1) and X50
    CE60_10 = Timer2Rouge.Q and X60 and X2
    CE60_0 = X1 and X60

    CE100_200 = (mod[index] == "jour/nuit" and TimerJour.Q and X100 ) or (mod[index] == "nuit")
    CE200_100 = (mod[index] == "jour/nuit" and TimerNuit.Q and X200 ) or (mod[index] == "jour")

    CE1_2 = X1 and deroulement
    CE2_1 = X2 and panne

    CE1000_2000 = TimerC1.Q and X1000 and X1
    CE2000_1000 = TimerC2.Q and X2000 and X1

    #Grafcet fonctionnement normal
    if CE0_10 :
        X10=1
        X0=0
    elif CE10_20 :
        X20=1
        X10=0
    elif CE20_30 :
        X30=1
        X20=0
    elif CE30_40 :
        X40=1
        X30=0
    elif CE40_50:
        X50=1
        X40=0
    elif CE50_60:
        X60=1
        X50=0
    elif CE60_10:
        X10=1
        X60=0
    elif CE60_0:
        X0=1
        X60=0

    #Grafcet jour/nuit
    if CE100_200 :
        X200=1
        X100=0
    elif CE200_100 :
        X100=1
        X200=0

    #Grafcet clignotement
    if CE1_2:
        X2=1
        X1=0
    elif CE2_1:
        X1=1
        X1000=1
        X2=0

    #Grafcet feux oranges
    if CE1000_2000:
        X2000=1
        X1000=0
    elif CE2000_1000:
        X1000=1
        X2000=0

    Feu1Vert.value = X10 and not X1
    Feu1Orange.value = X20
    Feu1Rouge.value = (X30 or X40 or X50 or X60) and not X1

    Timer1Vert.IN = X10
    Timer1Orange.IN = X20
    Timer1Rouge.IN = X30

    Feu2Vert.value = X40 and not X1
    Feu2Orange.value = X50
    Feu2Rouge.value = (X10 or X20 or X30 or X60) and not X1

    Timer2Vert.IN = X40
    Timer2Orange.IN = X50
    Timer2Rouge.IN = X60

    LedJour.value = X100

    TimerJour.IN = X100
    TimerNuit.IN = X200
    
    TimerC1.IN = X1000
    TimerC2.IN = X2000
    if X1:
        Feu1Orange.value = X1000
        Feu2Orange.value = X1000
