import board # n° des broches de la pico
import displayio # gestion d'afficheurs
import terminalio # gestion de la fonte
import busio # liaison série
from digitalio import DigitalInOut, Direction, Pull
import analogio
import time
from adafruit_display_text import label # gestion des zones de texte
import adafruit_displayio_ssd1306 # driver de l'afficheur

displayio.release_displays() # Libère les broches de l'afficheur

# Config du bus SPI de l'afficheur et des GPIOS

spi = busio.SPI(clock=board.GP2,MOSI=board.GP3)
oled_reset = board.GP4
oled_cs = board.GP5
oled_dc = board.GP1
display_bus = displayio.FourWire(spi, command=oled_dc, chip_select=oled_cs,
reset=oled_reset, baudrate=1000000)

bp_menu = DigitalInOut(board.GP12)
bp_menu.direction = Direction.INPUT
bp_menu.pull = Pull.UP

bp_plus = DigitalInOut(board.GP13)
bp_plus.direction = Direction.INPUT
bp_plus.pull = Pull.UP

bp_moins = DigitalInOut(board.GP11)
bp_moins.direction = Direction.INPUT
bp_moins.pull = Pull.UP

detecpanne = analogio.AnalogIn(board.A2)

WIDTH = 128
HEIGHT = 64
BORDER = 5
display = adafruit_displayio_ssd1306.SSD1306(display_bus, width=WIDTH,
height=HEIGHT)

splash = displayio.Group()
display.root_group = splash

text_area = label.Label(terminalio.FONT, color=0xFFFFFF)
splash.append(text_area)

index = 0
indexMenu = 2
panne = 1

def config_feux(tempos, modes):

    global index
    global indexMenu
    global panne

    if detecpanne.value >= 60000:
        panne = 1

    if not bp_menu.value :
        index += 1
        if index == 8:
            index = 0
            if detecpanne.value < 40000:
                panne = 0
        if index >=0 and index <= 6:
            afficher(tempos)
        if index == 7:
            afficher(modes[indexMenu])
        time.sleep(0.05)
    while not bp_menu.value:
        pass

    if index >=0 and index <= 6:
        if not bp_plus.value :
            tempos[index - 1] += 1
            afficher(tempos)
        while not bp_plus.value:
            pass
        if not bp_moins.value and tempos[index - 1] != 1:
            tempos[index - 1] -= 1
            afficher(tempos)
        while not bp_moins.value:
            pass

    if index == 7:
        if not bp_plus.value and indexMenu !=2 :
            indexMenu += 1
            print(indexMenu)
            afficher(modes[indexMenu])
        while not bp_plus.value:
            pass
        if not bp_moins.value and indexMenu !=0:
            indexMenu -= 1
            print(indexMenu)
            afficher(modes[indexMenu])
        while not bp_moins.value:
            pass
        print(index)

    print(panne,detecpanne.value)
    time.sleep(0.05)

def afficher(val):

    global index

    if index == 0:
        text_area.x = 20
        text_area.y = BORDER+20
        text_area.text = ""

    if index == 1:
        text_area.x = 20
        text_area.y = BORDER+20
        text_area.text = f"Config Duree\nFeu1Vert : { val[index - 1]}s"

    if index == 2:
        text_area.x = 20
        text_area.y = BORDER+20
        text_area.text = f"Config Duree\nFeu1Orange : { val[index - 1]}s"

    if index == 3:
        text_area.x = 20
        text_area.y = BORDER+20
        text_area.text = f"Duree des\n2FeuRouge : { val[index - 1]}s"

    if index == 4:
        text_area.x = 20
        text_area.y = BORDER+20
        text_area.text = f"Config Duree\nFeu2Vert : { val[index - 1]}s"

    if index == 5:
        text_area.x = 20
        text_area.y = BORDER+20
        text_area.text = f"Config Duree\nFeu2Orange : { val[index - 1]}s"

    if index == 6:
        text_area.x = 20
        text_area.y = BORDER+20
        text_area.text = f"Duree des\n2FeuRouge2 : { val[index - 1]}s"

    if index == 7:
        text_area.x = 20
        text_area.y = BORDER+20
        text_area.text = f"Mode : \n{val}"

