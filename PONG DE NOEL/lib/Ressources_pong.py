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

class pong() :

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

        # instanciation des groupes d'affichage
        self.groupe_principal = displayio.Group()
        self.groupe_graphismes = displayio.Group()
        self.groupe_scores = displayio.Group(scale = 3)
        self.groupe_principal.append(self.groupe_graphismes)
        self.groupe_principal.append(self.groupe_scores)

        # Fond pour le titre
        fichier_image = open("images/Pong/Ecran_titre_christmas.bmp", 'rb')
        image_bmp = displayio.OnDiskBitmap(fichier_image)
        self.ecran_titre_christmas = displayio.TileGrid(image_bmp, pixel_shader=displayio.ColorConverter())

        # Animation guirlande lumineuse
        guirlande_bmp, palette_guirlande = adafruit_imageload.load("images/Pong/Guirlande_lumineuse.bmp", bitmap=displayio.Bitmap, palette=displayio.Palette)
        palette_guirlande.make_transparent(6)
        self.guirlande = displayio.TileGrid(guirlande_bmp,pixel_shader=palette_guirlande, width=1, height=1, tile_width=160, tile_height=17, default_tile=0 , x=0, y=0)

        # Bouton de start
        bouton_start_bmp, palette_bouton_start = adafruit_imageload.load("images/Pong/Bouton_start.bmp", bitmap=displayio.Bitmap, palette=displayio.Palette)
        palette_bouton_start.make_transparent(32)
        self.bouton_start = displayio.TileGrid(bouton_start_bmp,pixel_shader=palette_bouton_start, x=30, y=105)

        # Fond pour les règles
        fichier_image = open("images/Pong/Ecran_regles_christmas.bmp", 'rb')
        image_bmp = displayio.OnDiskBitmap(fichier_image)
        self.ecran_regles_christmas = displayio.TileGrid(image_bmp, pixel_shader=displayio.ColorConverter())

        # labels de texte pour les règles du jeu
        self.label1_regles = label.Label(terminalio.FONT, text="REGLES DU JEU", color=0xFFFFFF, scale=2, x=5, y=10)
        self.label2_regles = label.Label(terminalio.FONT, text="-------------", color=0xFFFFFF, scale=2, x=5, y=25)
        self.label3_regles = label.Label(terminalio.FONT, text="????", color=0xFFFFFF, scale=1, x=5, y=40)

        # Ecran_jeu pour la version du jeu 'christmas'
        fichier_image = open("images/Pong/Ecran_jeu_christmas.bmp", 'rb')
        image_bmp = displayio.OnDiskBitmap(fichier_image)
        self.ecran_jeu_christmas = displayio.TileGrid(image_bmp, pixel_shader=displayio.ColorConverter())
        self.bord_superieur = 9
        self.bord_inferieur = 116
        self.bord_gauche = 0
        self.bord_droit = 159

        # Raquettes pour la version 'christmas'
        raquette_christmas_bmp, palette_raquette_christmas = adafruit_imageload.load("images/Pong/Raquette_christmas.bmp", bitmap=displayio.Bitmap, palette=displayio.Palette)
        palette_raquette_christmas.make_transparent(2)
        self.raquette_g_christmas = displayio.TileGrid(raquette_christmas_bmp,pixel_shader=palette_raquette_christmas, x=1, y=55)
        self.raquette_d_christmas = displayio.TileGrid(raquette_christmas_bmp,pixel_shader=palette_raquette_christmas, x=153, y=55)
        self.largeur_raquette_christmas = 5
        self.hauteur_raquette_christmas = 23

        # Balle pour la version 'christmas'
        balle_christmas_bmp, palette_balle_christmas = adafruit_imageload.load("images/Pong/Balle_christmas.bmp", bitmap=displayio.Bitmap, palette=displayio.Palette)
        palette_balle_christmas.make_transparent(2)
        self.balle_christmas = displayio.TileGrid(balle_christmas_bmp,pixel_shader=palette_balle_christmas, x=50, y=50)
        self.diametre_balle_christmas = 10

        # Père noël animé
        santa_claus_bmp, palette_santa_claus = adafruit_imageload.load("images/Pong/Santa_claus.bmp", bitmap=displayio.Bitmap, palette=displayio.Palette)
        palette_santa_claus.make_transparent(19)
        self.santa_claus = displayio.TileGrid(santa_claus_bmp,pixel_shader=palette_santa_claus, width=1, height=1, tile_width=32, tile_height=32, default_tile=0 , x=50, y=90)
        self.offset_walk = 0
        self.offset_idle = 8
        self.offset_hurt = 16

        # Cadeau
        cadeau_christmas_bmp, palette_cadeau_christmas = adafruit_imageload.load("images/Pong/Cadeau.bmp", bitmap=displayio.Bitmap, palette=displayio.Palette)
        palette_cadeau_christmas.make_transparent(20)
        self.cadeau_christmas = displayio.TileGrid(cadeau_christmas_bmp,pixel_shader=palette_cadeau_christmas, x=60, y=20)
        self.largeur_cadeau_christmas = 16
        self.hauteur_cadeau_christmas = 18

        # Animation d'explosion
        explosion_bmp, palette_explosion = adafruit_imageload.load("images/Pong/Explosion.bmp", bitmap=displayio.Bitmap, palette=displayio.Palette)
        palette_explosion.make_transparent(3)
        self.explosion = displayio.TileGrid(explosion_bmp,pixel_shader=palette_explosion, width=1, height=1, tile_width=32, tile_height=32, default_tile=0 , x=0, y=0)

        # Scores des joueurs
        score_bmp, palette_score = adafruit_imageload.load("images/Pong/Chiffres_score.bmp", bitmap=displayio.Bitmap, palette=displayio.Palette)
        palette_score.make_transparent(1)
        self.score_g = displayio.TileGrid(score_bmp,pixel_shader=palette_score, width=1, height=1, tile_width=8, tile_height=9, default_tile=0 , x=16, y=16)
        self.score_d = displayio.TileGrid(score_bmp,pixel_shader=palette_score, width=1, height=1, tile_width=8, tile_height=9, default_tile=0 , x=30, y=16)

        # Fond pour l'écran de game over
        fichier_image = open("images/Pong/Ecran_fin_christmas.bmp", 'rb')
        image_bmp = displayio.OnDiskBitmap(fichier_image)
        self.ecran_fin_christmas = displayio.TileGrid(image_bmp, pixel_shader=displayio.ColorConverter())

        # Animation de neige
        neige_bmp, palette_neige = adafruit_imageload.load("images/Pong/Neige.bmp", bitmap=displayio.Bitmap, palette=displayio.Palette)
        palette_neige.make_transparent(0)
        self.neige = displayio.TileGrid(neige_bmp,pixel_shader=palette_neige, width=1, height=1, tile_width=160, tile_height=96, default_tile=0 , x=0, y=0)

        # Animation du traineau du père noël
        traineau_bmp, palette_traineau = adafruit_imageload.load("images/Pong/Traineau.bmp", bitmap=displayio.Bitmap, palette=displayio.Palette)
        palette_traineau.make_transparent(1)
        self.traineau = displayio.TileGrid(traineau_bmp,pixel_shader=palette_traineau, width=1, height=1, tile_width=64, tile_height=24, default_tile=0 , x=-64, y=49)

        # labels de texte pour le score final
        self.label_score_J1 = label.Label(terminalio.FONT, text="?", color=0xFFFF00, scale=3, x=38, y=60)
        self.label_score_slash = label.Label(terminalio.FONT, text="/", color=0xFFFF00, scale=3, x=73, y=60)
        self.label_score_J2 = label.Label(terminalio.FONT, text="?", color=0xFFFF00, scale=3, x=95, y=60)

        # Bruitages
        self.audio_pwm1 = audiopwmio.PWMAudioOut(board.GP16)
        self.audio_pwm2 = audiopwmio.PWMAudioOut(board.GP21)
        data1 = open("audio/Pong/Intro.wav", "rb")
        self.bruitage_intro = audiocore.WaveFile(data1)
        data2 = open("audio/Pong/Start.wav", "rb")
        self.bruitage_start = audiocore.WaveFile(data2)
        data3 = open("audio/Pong/Rebond_murs.wav", "rb")
        self.bruitage_rebond_murs = audiocore.WaveFile(data3)
        data4 = open("audio/Pong/Rebond_raquette.wav", "rb")
        self.bruitage_rebond_raquette = audiocore.WaveFile(data4)
        data5 = open("audio/Pong/Ouch.wav", "rb")
        self.bruitage_ouch = audiocore.WaveFile(data5)
        data6 = open("audio/Pong/Explosion.wav", "rb")
        self.bruitage_explosion = audiocore.WaveFile(data6)
        data7 = open("audio/Pong/Game_over.wav", "rb")
        self.bruitage_game_over = audiocore.WaveFile(data7)


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
