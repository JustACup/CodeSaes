######################################
# IMPORTATION DES DIFFERENTS MODULES #
######################################
# Modules Natifs
import board
import displayio
import busio
import terminalio
import vectorio
from fourwire import FourWire       # à partir de la version 9
import audiocore
import audiopwmio
import digitalio
# Modules extérieurs
from adafruit_st7735r import ST7735R
import adafruit_imageload
from adafruit_display_text import label

class tutoriel() :

    def __init__(self, mosi_lcd=board.GP11, miso_lcd=board.GP12, sck_lcd=board.GP10, cs_lcd=board.GP13, dc_lcd=board.GP15, res_lcd=board.GP14) :
        # libère toute ressource précédemment utilisée pour un écran
        displayio.release_displays()
        # instanciation du bus SPI pour l'écran
        self.spi_lcd = busio.SPI(MOSI=mosi_lcd, MISO=miso_lcd, clock=sck_lcd)
        self.bus_affichage = FourWire(self.spi_lcd, command=dc_lcd, chip_select=cs_lcd, reset=res_lcd)
        #self.bus_affichage = displayio.FourWire(self.spi_lcd, command=dc_lcd, chip_select=cs_lcd, reset=res_lcd)
        # instanciation de l'écran
        self.ecran = ST7735R(self.bus_affichage, width=160, height=128, colstart=2, rowstart=1, rotation=90, bgr=True)
        self.largeur_ecran = 160
        self.hauteur_ecran = 128

        # instanciation du groupe d'affichage
        self.groupe_principal = displayio.Group()

        # Fond pour le titre
        fichier_image = open("images/Tutoriel/Ecran_titre.bmp", 'rb')
        image_bmp = displayio.OnDiskBitmap(fichier_image)
        self.ecran_titre = displayio.TileGrid(image_bmp, pixel_shader=displayio.ColorConverter())

        # Bouton de start
        bouton_start_bmp, palette_bouton_start = adafruit_imageload.load("images/Tutoriel/Bouton_start.bmp", bitmap=displayio.Bitmap, palette=displayio.Palette)
        palette_bouton_start.make_transparent(32)
        self.bouton_start = displayio.TileGrid(bouton_start_bmp,pixel_shader=palette_bouton_start, x=0, y=0)

        # Bouton de navigation
        boutons_direction_bmp, palette_boutons_direction = adafruit_imageload.load("images/Tutoriel/Boutons_direction.bmp", bitmap=displayio.Bitmap, palette=displayio.Palette)
        palette_boutons_direction.make_transparent(2)
        self.bouton_droite = displayio.TileGrid(boutons_direction_bmp,pixel_shader=palette_boutons_direction, width=1, height=1, tile_width=25, tile_height=25, default_tile=3 , x=130, y=100)
        self.bouton_gauche = displayio.TileGrid(boutons_direction_bmp,pixel_shader=palette_boutons_direction, width=1, height=1, tile_width=25, tile_height=25, default_tile=1 , x=130, y=100)
        self.bouton_haut = displayio.TileGrid(boutons_direction_bmp,pixel_shader=palette_boutons_direction, width=1, height=1, tile_width=25, tile_height=25, default_tile=2 , x=130, y=100)
        self.bouton_bas = displayio.TileGrid(boutons_direction_bmp,pixel_shader=palette_boutons_direction, width=1, height=1, tile_width=25, tile_height=25, default_tile=0 , x=130, y=100)

        # labels de texte pour les règles du jeu
        self.label1_regles = label.Label(terminalio.FONT, text="REGLES DU JEU", color=0xFF0000, scale=2, x=5, y=10)
        self.label2_regles = label.Label(terminalio.FONT, text="-------------", color=0xFF0000, scale=2, x=5, y=25)
        self.label3_regles = label.Label(terminalio.FONT, text="????", color=0xFFFFFF, scale=1, x=5, y=40)

        # Image pour les regles
        fichier_image = open("images/Tutoriel/Portrait_astronaute.bmp", 'rb')
        image_bmp = displayio.OnDiskBitmap(fichier_image)
        self.portrait = displayio.TileGrid(image_bmp, pixel_shader=displayio.ColorConverter(),x=100,y=0)

        # Fond pour le jeu
        fichier_image = open("images/Tutoriel/Ecran_jeu.bmp", 'rb')
        image_bmp = displayio.OnDiskBitmap(fichier_image)
        self.ecran_jeu = displayio.TileGrid(image_bmp, pixel_shader=displayio.ColorConverter())

        # Graphique du vaisseau
        vaisseau_sheet, palette_vaisseau = adafruit_imageload.load("images/Tutoriel/Vaisseau.bmp", bitmap=displayio.Bitmap, palette=displayio.Palette)
        palette_vaisseau.make_transparent(0)
        self.vaisseau = displayio.TileGrid(vaisseau_sheet,pixel_shader=palette_vaisseau, width=1, height=1, tile_width=34, tile_height=31, default_tile=0 , x=60, y=20)
        self.hauteur_vaisseau = 31
        self.largeur_vaisseau = 34

        # Graphique de l'astronaute
        astronaute_sheet, palette_astronaute = adafruit_imageload.load("images/Tutoriel/Astronaute.bmp", bitmap=displayio.Bitmap, palette=displayio.Palette)
        palette_astronaute.make_transparent(2)
        self.astronaute = displayio.TileGrid(astronaute_sheet,pixel_shader=palette_astronaute, width=1, height=1, tile_width=14, tile_height=22, default_tile=0 , x=90, y=80)
        self.hauteur_astronaute = 22
        self.largeur_astronaute = 14

        # Graphique de la barre de vie
        barre_vie_sheet, palette_barre_vie = adafruit_imageload.load("images/Tutoriel/Lifebar.bmp", bitmap=displayio.Bitmap, palette=displayio.Palette)
        palette_barre_vie.make_transparent(3)
        self.barre_vie = displayio.TileGrid(barre_vie_sheet,pixel_shader=palette_barre_vie, width=1, height=1, tile_width=48, tile_height=16, default_tile=0 , x=56, y=0)

        # Graphique asteroide
        asteroide_sheet, palette_asteroide = adafruit_imageload.load("images/Tutoriel/Asteroide.bmp", bitmap=displayio.Bitmap, palette=displayio.Palette)
        palette_asteroide.make_transparent(7)
        self.asteroide = displayio.TileGrid(asteroide_sheet,pixel_shader=palette_asteroide, x=10, y=60)
        self.hauteur_asteroide = 17
        self.largeur_asteroide = 14

        # Graphique explosion
        explosion_sheet, palette_explosion = adafruit_imageload.load("images/Tutoriel/Explosion.bmp", bitmap=displayio.Bitmap, palette=displayio.Palette)
        palette_explosion.make_transparent(2)
        self.explosion = displayio.TileGrid(explosion_sheet,pixel_shader=palette_explosion, width=1, height=1, tile_width=16, tile_height=16, default_tile=0 , x=10, y=60)

        # Labels du chrono et du score
        self.label_score = label.Label(terminalio.FONT, text="00", color=0xFFFFFF, scale=1, x=5, y=5)
        self.label_chrono = label.Label(terminalio.FONT, text="1:00", color=0xFFFFFF, scale=1, x=135, y=5)

        # Fond pour la fin de partie
        fichier_image = open("images/Tutoriel/Ecran_fin.bmp", 'rb')
        image_bmp = displayio.OnDiskBitmap(fichier_image)
        self.ecran_fin = displayio.TileGrid(image_bmp, pixel_shader=displayio.ColorConverter())

        # Labels du score final
        self.label_score_final = label.Label(terminalio.FONT, text=self.label_score.text, color=0xFFFFFF, scale=2, x=70, y=70)

        # Bruitages
        self.audio_pwm1 = audiopwmio.PWMAudioOut(board.GP16)
        self.audio_pwm2 = audiopwmio.PWMAudioOut(board.GP21)
        data1 = open("audio/Tutoriel/Start.wav", "rb")
        self.bruitage_start = audiocore.WaveFile(data1)
        data2 = open("audio/Tutoriel/Chrono.wav", "rb")
        self.bruitage_chrono = audiocore.WaveFile(data2)
        data3 = open("audio/Tutoriel/Astronaute.wav", "rb")
        self.bruitage_astronaute = audiocore.WaveFile(data3)
        data4 = open("audio/Tutoriel/Game_over.wav", "rb")
        self.bruitage_game_over = audiocore.WaveFile(data4)
        data5 = open("audio/Tutoriel/Explosion.wav", "rb")
        self.bruitage_explosion = audiocore.WaveFile(data5)
        data6 = open("audio/Tutoriel/Ecran_titre.wav", "rb")
        self.bruitage_ecran_titre = audiocore.WaveFile(data6)

    def collision(self,sprite1, sprite2):
        if (sprite1.tile_width >= sprite2.tile_width) :
            condition_x = (sprite1.x <= sprite2.x) and ((sprite1.x + sprite1.tile_width) >= (sprite2.x + sprite2.tile_width))
        else :
            condition_x = (sprite2.x <= sprite1.x) and ((sprite2.x + sprite2.tile_width) >= (sprite1.x + sprite1.tile_width))
        if (sprite1.tile_height >= sprite2.tile_height) :
            condition_y = (sprite1.y <= sprite2.y) and ((sprite1.y + sprite1.tile_height) >= (sprite2.y + sprite2.tile_height))
        else :
            condition_y = (sprite2.y <= sprite1.y) and ((sprite2.y + sprite2.tile_height) >= (sprite1.y + sprite1.tile_height))
        return (condition_x and condition_y)

class test_SPI() :

    def __init__(self, mosi_lcd=board.GP11, miso_lcd=board.GP12, sck_lcd=board.GP10, cs_lcd=board.GP13) :
        # libère toute ressource précédemment utilisée pour un écran
        displayio.release_displays()
        # instanciation du bus SPI pour l'écran
        self.bus_spi = busio.SPI(MOSI=mosi_lcd, MISO=miso_lcd, clock=sck_lcd)
        self.broche_cs = digitalio.DigitalInOut(cs_lcd)
        self.broche_cs.direction = digitalio.Direction.OUTPUT

    def Envoi(self, buf = None) :
        # broche CS à l'état bas
        self.broche_cs.value = False
        # émission du contenu du buffer
        self.bus_spi.write(buf)
        # broche CS à l'état haut
        self.broche_cs.value = True

