import board
import displayio
import terminalio
import busio
from adafruit_display_text import label
import adafruit_displayio_ssd1306
import time
import analogio
from digitalio import DigitalInOut, Direction, Pull

displayio.release_displays() 

spi = busio.SPI(clock=board.GP2,MOSI=board.GP3)
oled_reset = board.GP4
oled_cs = board.GP5
oled_dc = board.GP1
display_bus = displayio.FourWire(spi, command=oled_dc, chip_select=oled_cs,reset=oled_reset, baudrate=1000000)
panne_rouge = analogio.AnalogIn(board.A2)

WIDTH = 128
HEIGHT = 64
BORDER = 5
display = adafruit_displayio_ssd1306.SSD1306(display_bus, width=WIDTH,height=HEIGHT)

splash = displayio.Group()
display.root_group = splash

text_area = label.Label(terminalio.FONT, color=0xFFFFFF)
splash.append(text_area)
menu = -1
index = 0


def afficher(texte=""):
    text_area.x = 20
    text_area.y = BORDER+20
    text_area.text = texte

def config_feux(bp_menu, bp_plus, bp_moins, liste_duree, mod, panne):
    global menu
    global index
    deroulement = 0
    liste_menu = [
        f"Timer1Vert : {liste_duree[0]} s",
        f"Timer1Orange : {liste_duree[1]} s",
        f"Timer1Rouge : {liste_duree[2]} s",
        f"Timer2Vert : {liste_duree[3]} s",
        f"Timer2Orange : {liste_duree[4]} s",
        f"Timer2Rouge : {liste_duree[5]} s",
        f"Mode: {mod[index]}",
        f""
    ]
  
    if not bp_menu.value :
        menu = (menu + 1)%len(liste_menu)
        time.sleep(0.25)
    if menu <= 5 :
        if liste_duree[menu] > 0 and not bp_moins.value:
            liste_duree[menu] -=1
            time.sleep(0.25)
            print(menu)
        elif liste_duree[menu] < 60 and not bp_plus.value:
            liste_duree[menu] +=1
            time.sleep(0.25)
    elif menu == 6:
        if not bp_moins.value:
            index = (index - 1)%len(mod)
            time.sleep(0.25)
        elif not bp_plus.value:
            index = (index + 1)%len(mod)
            time.sleep(0.25)
    elif menu == 7:
        panne = 0
        deroulement = 1
    if menu >= 0:
        afficher(liste_menu[menu])

    time.sleep(0.005)
    return (index, liste_duree, deroulement)

def val_panne():
    global panne_rouge
    panne = 0
    vale_panne=panne_rouge.value*3.3/65535
    if vale_panne > 3:
        panne = 1
    return panne
