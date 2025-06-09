######################################
# IMPORTATION DES DIFFERENTS MODULES #
######################################
# Modules Natifs

import time
import supervisor
import random

# Modules du dossier 'lib'

import Gestion_controles
import Ressources_pong

######################################
#  INSTANCIATION DES OBJETS UTILES   #
######################################

Controles = Gestion_controles.controles()
Pong = Ressources_pong.pong()

#################################
# AFFICHAGE DE L'ECRAN DE TITRE #
#################################

Pong.groupe_principal.append(Pong.ecran_titre_christmas)
Pong.groupe_principal.append(Pong.guirlande)
Pong.groupe_principal.append(Pong.bouton_start)

Pong.ecran.root_group = Pong.groupe_principal

Pong.bouton_start.x = 70
Pong.bouton_start.y = 100

time.sleep(1)

Pong.audio_pwm1.play(Pong.bruitage_intro)

#############################
# BOUCLE D'ATTENTE DE TITRE #
#############################

while Controles.bouton_start.value == Controles.relache:
    Pong.bouton_start.hidden = False
    Pong.guirlande[0] = 0
    time.sleep(0.5)
    Pong.bouton_start.hidden = True
    Pong.guirlande[0] = 1
    time.sleep(0.5)
Pong.audio_pwm1.stop()

Pong.groupe_principal.pop(Pong.groupe_principal.index(Pong.ecran_titre_christmas))
Pong.groupe_principal.pop(Pong.groupe_principal.index(Pong.guirlande))
Pong.groupe_principal.pop(Pong.groupe_principal.index(Pong.bouton_start))

###################################
# AFFICHAGE DE L'ECRAN DES REGLES #
###################################

Pong.groupe_principal.append(Pong.ecran_regles_christmas)
Pong.groupe_principal.append(Pong.label1_regles)
Pong.groupe_principal.append(Pong.label2_regles)
Pong.groupe_principal.append(Pong.label3_regles)
Pong.label3_regles.text = " tu connais \n Pong non ?"

Pong.groupe_principal.append(Pong.bouton_start)

Pong.label1_regles.x = 5
Pong.label1_regles.y = 10

Pong.label2_regles.x = 5
Pong.label2_regles.y = 20

Pong.label3_regles.x = 5
Pong.label3_regles.y = 35

Pong.bouton_start.x = 10
Pong.bouton_start.y = 105

###############################
# BOUCLE D'ATTENTE DES REGLES #
###############################

while Controles.bouton_start.value == Controles.relache:
    Pong.bouton_start.hidden = False
    time.sleep(0.5)
    Pong.bouton_start.hidden = True
    time.sleep(0.5)
time.sleep(1)

Pong.groupe_principal.pop(Pong.groupe_principal.index(Pong.ecran_regles_christmas))
Pong.groupe_principal.pop(Pong.groupe_principal.index(Pong.label1_regles))
Pong.groupe_principal.pop(Pong.groupe_principal.index(Pong.label2_regles))
Pong.groupe_principal.pop(Pong.groupe_principal.index(Pong.label3_regles))
Pong.groupe_principal.pop(Pong.groupe_principal.index(Pong.bouton_start))

###############################
# AFFICHAGE DE L'ECRAN DE JEU #
###############################


Pong.groupe_principal.append(Pong.ecran_jeu_christmas)
Pong.groupe_principal.append(Pong.score_g)
Pong.groupe_principal.append(Pong.score_d)
Pong.groupe_principal.append(Pong.raquette_g_christmas)
Pong.groupe_principal.append(Pong.raquette_d_christmas)
Pong.groupe_principal.append(Pong.balle_christmas)

Pong.score_d.x = 90
Pong.score_g.x = 70

Pong.balle_christmas.x = 75


####################
# VARIABLES DU JEU #
####################
fin_de_partie = False
point_g = 0
point_d = 0
deplacement_horizontal = int(random.choice([-1, 1]))
deplacement_vertical = int(random.choice([-1, 1]))
# Initialisation des timers


#################
# BOUCLE DE JEU #
#################

while not fin_de_partie:
    if (
        Controles.bouton_haut.value == Controles.appuye
        and Pong.raquette_g_christmas.y != Pong.bord_superieur
    ):
        Pong.raquette_g_christmas.y = Pong.raquette_g_christmas.y - 1
    if (
        Controles.joystick_vertical.value > 51000
        and Pong.raquette_d_christmas.y != Pong.bord_superieur
    ):
        Pong.raquette_d_christmas.y = Pong.raquette_d_christmas.y - 1
    if (
        Controles.bouton_bas.value == Controles.appuye
        and Pong.raquette_g_christmas.y
        != Pong.bord_inferieur - Pong.hauteur_raquette_christmas
    ):
        Pong.raquette_g_christmas.y = Pong.raquette_g_christmas.y + 1
    if (
        Controles.joystick_vertical.value < 15000
        and Pong.raquette_d_christmas.y
        != Pong.bord_inferieur - Pong.hauteur_raquette_christmas
    ):
        Pong.raquette_d_christmas.y = Pong.raquette_d_christmas.y + 1
    if Pong.balle_christmas.y >= Pong.bord_inferieur - Pong.diametre_balle_christmas:
        deplacement_vertical = -1
        Pong.audio_pwm2.play(Pong.bruitage_rebond_murs)
    elif Pong.balle_christmas.y <= Pong.bord_superieur:
        deplacement_vertical = 1
        Pong.audio_pwm2.play(Pong.bruitage_rebond_murs)
    if (
        Pong.balle_christmas.x + Pong.diametre_balle_christmas
        >= Pong.raquette_d_christmas.x
        and Pong.balle_christmas.x
        <= Pong.raquette_d_christmas.x + Pong.largeur_raquette_christmas
        and Pong.balle_christmas.y + Pong.diametre_balle_christmas / 2
        >= Pong.raquette_d_christmas.y
        and Pong.balle_christmas.y - Pong.diametre_balle_christmas / 2
        <= Pong.raquette_d_christmas.y + Pong.hauteur_raquette_christmas
    ):
        deplacement_horizontal = -1
        Pong.audio_pwm2.play(Pong.bruitage_rebond_raquette)
    if (
        Pong.balle_christmas.x
        <= Pong.raquette_g_christmas.x + Pong.largeur_raquette_christmas
        and Pong.balle_christmas.x + Pong.diametre_balle_christmas / 2
        >= Pong.raquette_g_christmas.x
        and Pong.balle_christmas.y + Pong.diametre_balle_christmas / 2
        >= Pong.raquette_g_christmas.y
        and Pong.balle_christmas.y - Pong.diametre_balle_christmas / 2
        <= Pong.raquette_g_christmas.y + Pong.hauteur_raquette_christmas
    ):
        deplacement_horizontal = 1
        Pong.audio_pwm2.play(Pong.bruitage_rebond_raquette)
    Pong.balle_christmas.x += deplacement_horizontal
    Pong.balle_christmas.y += deplacement_vertical
    if Pong.balle_christmas.x <= Pong.bord_gauche - Pong.diametre_balle_christmas:
        point_d += 1
        Pong.score_d[0] = point_d
        Pong.balle_christmas.x = 140
        Pong.balle_christmas.y = Pong.raquette_d_christmas.y + 7
        deplacement_horizontal = -1
        deplacement_vertical = int(random.choice([-1, 1]))
        time.sleep(1)
        while (
            Controles.joystick_vertical.value < 51000
            and Controles.joystick_vertical.value > 15000
        ):
            pass
    if Pong.balle_christmas.x >= Pong.bord_droit:
        point_g += 1
        Pong.score_g[0] = point_g
        Pong.balle_christmas.x = 10
        Pong.balle_christmas.y = Pong.raquette_g_christmas.y + 7
        deplacement_horizontal = 1
        deplacement_vertical = int(random.choice([-1, 1]))
        time.sleep(1)
        while (
            Controles.bouton_haut.value != Controles.appuye
            and Controles.bouton_bas.value != Controles.appuye
        ):
            pass
    if point_d == 10 or point_g == 10:
        fin_de_partie = True
    time.sleep(0.015)
Pong.groupe_principal.pop(Pong.groupe_principal.index(Pong.ecran_jeu_christmas))
Pong.groupe_principal.pop(Pong.groupe_principal.index(Pong.balle_christmas))
Pong.groupe_principal.pop(Pong.groupe_principal.index(Pong.score_d))
Pong.groupe_principal.pop(Pong.groupe_principal.index(Pong.score_g))
Pong.groupe_principal.pop(Pong.groupe_principal.index(Pong.raquette_d_christmas))
Pong.groupe_principal.pop(Pong.groupe_principal.index(Pong.raquette_g_christmas))

###############################
# AFFICHAGE DE L'ECRAN DE FIN #
###############################
Pong.groupe_principal.append(Pong.ecran_fin_christmas)
Pong.groupe_principal.append(Pong.label_score_J1)
Pong.groupe_principal.append(Pong.label_score_J2)
Pong.groupe_principal.append(Pong.label_score_slash)

Pong.label_score_J1.text = f"{point_g}"
Pong.label_score_J2.text = f"{point_d}"

###########################
# BOUCLE D'ATTENTE FINALE #
###########################

while True:
    if Controles.bouton_start.value == Controles.appuye:
        supervisor.reload()
