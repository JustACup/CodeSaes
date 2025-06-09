######################################
# IMPORTATION DES DIFFERENTS MODULES #
######################################
# Modules Natifs
import board
import displayio
import busio
import terminalio
from fourwire import FourWire       # à partir de la version 9
import audiocore
import audiopwmio
import digitalio
import random
# Modules extérieurs
from adafruit_st7735r import ST7735R
import adafruit_imageload
from adafruit_display_text import label

class gunfight() :

    def __init__(self,mosi_lcd=board.GP11, miso_lcd=board.GP12, sck_lcd=board.GP10, cs_lcd=board.GP13, dc_lcd=board.GP15, res_lcd=board.GP14) :
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
        fichier_image = open("images/Gunfight/Ecran_titre.bmp", 'rb')
        image_bmp = displayio.OnDiskBitmap(fichier_image)
        self.ecran_titre = displayio.TileGrid(image_bmp, pixel_shader=displayio.ColorConverter())

        # Bouton de start
        bouton_start_bmp, palette_bouton_start = adafruit_imageload.load("images/Gunfight/Bouton_start.bmp", bitmap=displayio.Bitmap, palette=displayio.Palette)
        palette_bouton_start.make_transparent(32)
        self.bouton_start = displayio.TileGrid(bouton_start_bmp,pixel_shader=palette_bouton_start, x=0, y=0)

        # Bullet hole
        trou_tir_bmp, palette_trou_tir = adafruit_imageload.load("images/Gunfight/Bullet_hole.bmp", bitmap=displayio.Bitmap, palette=displayio.Palette)
        palette_trou_tir.make_transparent(6)
        self.tir1 = displayio.TileGrid(trou_tir_bmp,pixel_shader=palette_trou_tir, x=random.randint(30,50), y=random.randint(20,40))
        self.tir2 = displayio.TileGrid(trou_tir_bmp,pixel_shader=palette_trou_tir, x=random.randint(80,130), y=random.randint(30,70))
        self.tir3 = displayio.TileGrid(trou_tir_bmp,pixel_shader=palette_trou_tir, x=random.randint(30,90), y=random.randint(60,100))
        self.tir4 = displayio.TileGrid(trou_tir_bmp,pixel_shader=palette_trou_tir, x=random.randint(40,80), y=random.randint(20,60))
        self.tir5 = displayio.TileGrid(trou_tir_bmp,pixel_shader=palette_trou_tir, x=random.randint(50,100), y=random.randint(90,110))

        # Bouton de navigation
        boutons_direction_bmp, palette_boutons_direction = adafruit_imageload.load("images/Gunfight/Boutons_direction.bmp", bitmap=displayio.Bitmap, palette=displayio.Palette)
        palette_boutons_direction.make_transparent(2)
        self.bouton_droite = displayio.TileGrid(boutons_direction_bmp,pixel_shader=palette_boutons_direction, width=1, height=1, tile_width=25, tile_height=25, default_tile=3 , x=130, y=100)
        self.bouton_gauche = displayio.TileGrid(boutons_direction_bmp,pixel_shader=palette_boutons_direction, width=1, height=1, tile_width=25, tile_height=25, default_tile=1 , x=130, y=100)
        self.bouton_haut = displayio.TileGrid(boutons_direction_bmp,pixel_shader=palette_boutons_direction, width=1, height=1, tile_width=25, tile_height=25, default_tile=2 , x=130, y=100)
        self.bouton_bas = displayio.TileGrid(boutons_direction_bmp,pixel_shader=palette_boutons_direction, width=1, height=1, tile_width=25, tile_height=25, default_tile=0 , x=130, y=100)

        # Cowboy pour les règles du jeu
        fichier_image = open("images/Gunfight/Cowboy.bmp", 'rb')
        image_bmp = displayio.OnDiskBitmap(fichier_image)
        self.cowboy = displayio.TileGrid(image_bmp, pixel_shader=displayio.ColorConverter(), x=0, y=0)

        # labels de texte pour les règles du jeu
        self.label1_regles = label.Label(terminalio.FONT, text="REGLES DU JEU", color=0xECD913, scale=2, x=0, y=0)
        self.label2_regles = label.Label(terminalio.FONT, text="-------------", color=0x543917, scale=2, x=0, y=0)
        self.label3_regles = label.Label(terminalio.FONT, text="????", color=0xFFFFFF, scale=1, x=0, y=0)

        # Fond pour le jeu
        fichier_image = open("images/Gunfight/Ecran_jeu.bmp", 'rb')
        image_bmp = displayio.OnDiskBitmap(fichier_image)
        self.ecran_jeu = displayio.TileGrid(image_bmp, pixel_shader=displayio.ColorConverter())

        # Barre de cartouches
        cartouches_bmp, palette_cartouches = adafruit_imageload.load("images/Gunfight/Cartouches.bmp", bitmap=displayio.Bitmap, palette=displayio.Palette)
        palette_cartouches.make_transparent(1)
        self.cartouches = displayio.TileGrid(cartouches_bmp,pixel_shader=palette_cartouches, width=1, height=1, tile_width=40, tile_height=15, default_tile=0 , x=0, y=0)

        # Personnage du sheriff animé
        sheriff_bmp, palette_sheriff = adafruit_imageload.load("images/Gunfight/Sheriff.bmp", bitmap=displayio.Bitmap, palette=displayio.Palette)
        palette_sheriff.make_transparent(12)
        self.sheriff = displayio.TileGrid(sheriff_bmp,pixel_shader=palette_sheriff, width=1, height=1, tile_width=64, tile_height=64, default_tile=0 , x=0, y=0)

        # Personnage du bandit animé
        bandit_bmp, palette_bandit = adafruit_imageload.load("images/Gunfight/Bandit.bmp", bitmap=displayio.Bitmap, palette=displayio.Palette)
        palette_bandit.make_transparent(17)
        self.bandit = displayio.TileGrid(bandit_bmp,pixel_shader=palette_bandit, width=1, height=1, tile_width=64, tile_height=64, default_tile=4 , x=0, y=0)

        # Cloche animée
        cloche_bmp, palette_cloche = adafruit_imageload.load("images/Gunfight/Desk_bell.bmp", bitmap=displayio.Bitmap, palette=displayio.Palette)
        palette_cloche.make_transparent(24)
        self.cloche = displayio.TileGrid(cloche_bmp,pixel_shader=palette_cloche, width=1, height=1, tile_width=24, tile_height=24, default_tile=0 , x=0, y=0)

        # Labels des scores
        self.label_score_J1 = label.Label(terminalio.FONT, text="0", color=0xFFFFFF, scale=2, x=0, y=0)
        self.label_score_J2 = label.Label(terminalio.FONT, text="0", color=0xFFFFFF, scale=2, x=0, y=0)

        # Label d'avertissement
        self.label_avertissement = label.Label(terminalio.FONT, text="La cloche n'a pas sonne !", color=0xFFFFFF, scale=1, x=0, y=0)

        # Bruitages
        self.audio_pwm1 = audiopwmio.PWMAudioOut(board.GP16)
        self.audio_pwm2 = audiopwmio.PWMAudioOut(board.GP21)
        data1 = open("audio/Gunfight/Desk_bell.wav", "rb")
        self.bruitage_cloche = audiocore.WaveFile(data1)
        data2 = open("audio/Gunfight/Gun_shot.wav", "rb")
        self.bruitage_tir = audiocore.WaveFile(data2)
        data3 = open("audio/Gunfight/Ecran_titre.wav", "rb")
        self.bruitage_ecran_titre = audiocore.WaveFile(data3)
        data4 = open("audio/Gunfight/Ecran_fin.wav", "rb")
        self.bruitage_ecran_fin = audiocore.WaveFile(data4)
        data5 = open("audio/Gunfight/Gun_shots.wav", "rb")
        self.bruitage_start = audiocore.WaveFile(data5)

        # Fond pour la fin de partie
        fichier_image = open("images/Gunfight/Ecran_fin.bmp", 'rb')
        image_bmp = displayio.OnDiskBitmap(fichier_image)
        self.ecran_fin = displayio.TileGrid(image_bmp, pixel_shader=displayio.ColorConverter())

        # portraits des joueurs
        J1_bmp, palette_J1 = adafruit_imageload.load("images/Gunfight/Portrait_J1.bmp", bitmap=displayio.Bitmap, palette=displayio.Palette)
        palette_J1.make_transparent(28)
        self.portrait_J1 = displayio.TileGrid(J1_bmp,pixel_shader=palette_J1, x=0, y=0)
        J2_bmp, palette_J2 = adafruit_imageload.load("images/Gunfight/Portrait_J2.bmp", bitmap=displayio.Bitmap, palette=displayio.Palette)
        palette_J2.make_transparent(27)
        self.portrait_J2 = displayio.TileGrid(J2_bmp,pixel_shader=palette_J2, x=0, y=0)

        # Labels du score final
        self.label_score_final = label.Label(terminalio.FONT, text="xxx", color=0xFFFFFF, scale=2, x=0, y=0)

