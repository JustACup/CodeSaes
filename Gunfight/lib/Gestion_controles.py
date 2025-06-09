######################################
# IMPORTATION DES DIFFERENTS MODULES #
######################################
# Modules Natifs
import board
import digitalio
import analogio

class controles() :

    def __init__(self,joy_x=board.GP26, joy_y=board.GP27, joy_bp=board.GP22, bph=board.GP6, bpb=board.GP7, bpg=board.GP8, bpd=board.GP9, ledpin=board.GP4, reset=board.GP0, shut=board.GP18) :
        # Joysticks analogiques 2 axes
        self.joystick_vertical = analogio.AnalogIn(joy_y)
        self.joystick_horizontal = analogio.AnalogIn(joy_x)

        # LED interne à la Pico
        self.LED_pico = digitalio.DigitalInOut(board.GP25)
        self.LED_pico.direction = digitalio.Direction.OUTPUT
        self.LED_pico.value = False

        # LED de test
        self.LED_test = digitalio.DigitalInOut(ledpin)
        self.LED_test.direction = digitalio.Direction.OUTPUT
        self.LED_test.value = False

        # Valeurs des boutons
        self.appuye = False
        self.relache = True
		
        # Bouton du joystick
        self.bouton_start = digitalio.DigitalInOut(joy_bp)
        self.bouton_start.direction = digitalio.Direction.INPUT
        self.bouton_start.pull = digitalio.Pull.UP

        # Bouton haut
        self.bouton_haut = digitalio.DigitalInOut(bph)
        self.bouton_haut.direction = digitalio.Direction.INPUT
        self.bouton_haut.pull = digitalio.Pull.UP

        # Bouton bas
        self.bouton_bas = digitalio.DigitalInOut(bpb)
        self.bouton_bas.direction = digitalio.Direction.INPUT
        self.bouton_bas.pull = digitalio.Pull.UP

        # Bouton droit
        self.bouton_droite = digitalio.DigitalInOut(bpd)
        self.bouton_droite.direction = digitalio.Direction.INPUT
        self.bouton_droite.pull = digitalio.Pull.UP

        # Bouton gauche
        self.bouton_gauche = digitalio.DigitalInOut(bpg)
        self.bouton_gauche.direction = digitalio.Direction.INPUT
        self.bouton_gauche.pull = digitalio.Pull.UP

        # Bouton reset
        self.bouton_reset = digitalio.DigitalInOut(reset)
        self.bouton_reset.direction = digitalio.Direction.INPUT
        self.bouton_reset.pull = digitalio.Pull.UP

        # Broche de mise en veille de l'ampli audio
        self.audio_shutdown = digitalio.DigitalInOut(shut)
        self.audio_shutdown.direction = digitalio.Direction.OUTPUT
        self.audio_shutdown.value = False

