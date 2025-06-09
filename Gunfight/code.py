######################################
# IMPORTATION DES DIFFERENTS MODULES #
######################################
# Modules Natifs
import time
import random
import supervisor

# Modules du dossier 'lib'
import Ressources_gunfight
import Gestion_controles

######################################
#  INSTANCIATION DES OBJETS UTILES   #
######################################
Gunfight = Ressources_gunfight.gunfight()
Controles = Gestion_controles.controles()


#############################################
# AJOUT DES ELEMENTS GRAPHIQUES SUR L'ECRAN #
#############################################
Gunfight.groupe_principal.append(Gunfight.ecran_titre)

Gunfight.groupe_principal.append(Gunfight.bouton_start)

Gunfight.ecran.root_group = Gunfight.groupe_principal

Gunfight.bouton_start.x = 70
Gunfight.bouton_start.y = 100

Gunfight.audio_pwm1.play(Gunfight.bruitage_ecran_titre)
#############################
# BOUCLE D'ATTENTE DE TITRE #
#############################
while Controles.bouton_start.value == Controles.relache:
    Gunfight.bouton_start.hidden = False
    time.sleep(0.5)
    Gunfight.bouton_start.hidden = True
    time.sleep(0.5)
Gunfight.audio_pwm1.stop()

Gunfight.groupe_principal.append(Gunfight.tir1)
Gunfight.audio_pwm2.play(Gunfight.bruitage_start)
time.sleep(0.5)
Gunfight.groupe_principal.append(Gunfight.tir2)
time.sleep(0.5)
Gunfight.groupe_principal.append(Gunfight.tir3)
time.sleep(0.9)
Gunfight.groupe_principal.append(Gunfight.tir4)
time.sleep(0.4)
Gunfight.groupe_principal.append(Gunfight.tir5)
time.sleep(1)

Gunfight.groupe_principal.pop(Gunfight.groupe_principal.index(Gunfight.ecran_titre))
Gunfight.groupe_principal.pop(Gunfight.groupe_principal.index(Gunfight.bouton_start))
Gunfight.groupe_principal.pop(Gunfight.groupe_principal.index(Gunfight.tir1))
Gunfight.groupe_principal.pop(Gunfight.groupe_principal.index(Gunfight.tir2))
Gunfight.groupe_principal.pop(Gunfight.groupe_principal.index(Gunfight.tir3))
Gunfight.groupe_principal.pop(Gunfight.groupe_principal.index(Gunfight.tir4))
Gunfight.groupe_principal.pop(Gunfight.groupe_principal.index(Gunfight.tir5))

########################
# AFFICHAGE DES REGLES #
########################
Gunfight.groupe_principal.append(Gunfight.label1_regles)
Gunfight.groupe_principal.append(Gunfight.label2_regles)
Gunfight.groupe_principal.append(Gunfight.label3_regles)
Gunfight.groupe_principal.append(Gunfight.cowboy)
Gunfight.label3_regles.text = " tu tires \n tu gagnes"

Gunfight.groupe_principal.append(Gunfight.bouton_start)

Gunfight.label1_regles.x = 5
Gunfight.label1_regles.y = 10

Gunfight.label2_regles.x = 5
Gunfight.label2_regles.y = 20

Gunfight.label3_regles.x = 5
Gunfight.label3_regles.y = 35

Gunfight.cowboy.x = 87
Gunfight.cowboy.y = 25

Gunfight.bouton_start.x = 10
Gunfight.bouton_start.y = 105
###############################
# BOUCLE D'ATTENTE DES REGLES #
###############################
while Controles.bouton_start.value == Controles.relache:
    Gunfight.bouton_start.hidden = False
    time.sleep(0.5)
    Gunfight.bouton_start.hidden = True
    time.sleep(0.5)
time.sleep(1)

Gunfight.groupe_principal.pop(Gunfight.groupe_principal.index(Gunfight.label1_regles))
Gunfight.groupe_principal.pop(Gunfight.groupe_principal.index(Gunfight.label2_regles))
Gunfight.groupe_principal.pop(Gunfight.groupe_principal.index(Gunfight.label3_regles))
Gunfight.groupe_principal.pop(Gunfight.groupe_principal.index(Gunfight.cowboy))
Gunfight.groupe_principal.pop(Gunfight.groupe_principal.index(Gunfight.bouton_start))
###############################
# AFFICHAGE DE L'ECRAN DE JEU #
###############################
Gunfight.groupe_principal.append(Gunfight.ecran_jeu)
Gunfight.groupe_principal.append(Gunfight.label_score_J2)
Gunfight.groupe_principal.append(Gunfight.cartouches)
Gunfight.groupe_principal.append(Gunfight.cloche)
Gunfight.groupe_principal.append(Gunfight.label_score_J1)
Gunfight.groupe_principal.append(Gunfight.sheriff)
Gunfight.groupe_principal.append(Gunfight.bandit)
Gunfight.groupe_principal.append(Gunfight.label_avertissement)
Gunfight.label_score_J1.x = 40
Gunfight.label_score_J1.y = 10

Gunfight.label_score_J2.x = 110
Gunfight.label_score_J2.y = 10

Gunfight.cartouches.x = 60
Gunfight.cartouches.y = 5

Gunfight.sheriff.x = 5
Gunfight.sheriff.y = 50

Gunfight.bandit.x = 95
Gunfight.bandit.y = 50

Gunfight.cloche.x = 67
Gunfight.cloche.y = 25


Gunfight.label_avertissement.x = 5
Gunfight.label_avertissement.y = 120
# Variables du jeu
fin_de_partie = False
scoreJ1 = 0
scoreJ2 = 0
cartouches = 0
temps_cloche = 0
temps_avant = 0
Gunfight.label_avertissement.hidden = True
Controles.LED_test.value = False

#################
# BOUCLE DE JEU #
#################

while not fin_de_partie:
    Gunfight.cloche[0] = 0
    temps_cloche = random.randint(1, 5)
    while temps_avant != temps_cloche:
        temps_avant += 1
        if (
            Controles.bouton_gauche.value == Controles.appuye
            or Controles.bouton_droite.value == Controles.appuye
        ):
            Gunfight.label_avertissement.hidden = False
        Gunfight.sheriff[0] = 0
        Gunfight.bandit[0] = 0
        time.sleep(0.2)
        Gunfight.sheriff[0] = 1
        Gunfight.bandit[0] = 1
        time.sleep(0.2)
        Gunfight.sheriff[0] = 2
        Gunfight.bandit[0] = 2
        time.sleep(0.2)
        Gunfight.sheriff[0] = 3
        Gunfight.bandit[0] = 3
        time.sleep(0.2)
        Gunfight.sheriff[0] = 4
        Gunfight.bandit[0] = 4
        time.sleep(0.2)
        Gunfight.label_avertissement.hidden = True
    temps_avant = 0
    Gunfight.cloche[0] = 1
    Gunfight.audio_pwm2.play(Gunfight.bruitage_cloche)
    Controles.LED_test.value = True
    while True:
        if Controles.bouton_gauche.value == Controles.appuye:
            Gunfight.sheriff[0] = 5
            time.sleep(0.2)
            Gunfight.sheriff[0] = 6
            time.sleep(0.2)
            Gunfight.sheriff[0] = 7
            Gunfight.bandit[0] = 14
            Gunfight.audio_pwm2.play(Gunfight.bruitage_tir)
            time.sleep(0.2)
            Gunfight.sheriff[0] = 8
            Gunfight.bandit[0] = 13
            time.sleep(0.2)
            Gunfight.sheriff[0] = 9
            Gunfight.bandit[0] = 12
            time.sleep(0.2)
            Gunfight.bandit[0] = 11
            time.sleep(0.2)
            Gunfight.bandit[0] = 10
            scoreJ1 += 1
            break
        if Controles.bouton_droite.value == Controles.appuye:
            Gunfight.bandit[0] = 9
            time.sleep(0.2)
            Gunfight.bandit[0] = 8
            time.sleep(0.2)
            Gunfight.bandit[0] = 7
            Gunfight.sheriff[0] = 10
            Gunfight.audio_pwm2.play(Gunfight.bruitage_tir)
            time.sleep(0.2)
            Gunfight.bandit[0] = 6
            Gunfight.sheriff[0] = 11
            time.sleep(0.2)
            Gunfight.bandit[0] = 5
            Gunfight.sheriff[0] = 12
            time.sleep(0.2)
            Gunfight.sheriff[0] = 13
            time.sleep(0.2)
            Gunfight.sheriff[0] = 14
            scoreJ2 += 1
            break
    Gunfight.label_score_J1.text = f"{scoreJ1}"
    Gunfight.label_score_J2.text = f"{scoreJ2}"
    cartouches += 1
    Gunfight.cartouches[0] = cartouches
    Controles.LED_test.value = False
    time.sleep(1)
    if cartouches == 8:
        fin_de_partie = True
Gunfight.groupe_principal.pop(Gunfight.groupe_principal.index(Gunfight.ecran_jeu))
Gunfight.groupe_principal.pop(Gunfight.groupe_principal.index(Gunfight.label_score_J2))
Gunfight.groupe_principal.pop(Gunfight.groupe_principal.index(Gunfight.cartouches))
Gunfight.groupe_principal.pop(Gunfight.groupe_principal.index(Gunfight.cloche))
Gunfight.groupe_principal.pop(Gunfight.groupe_principal.index(Gunfight.label_score_J1))
Gunfight.groupe_principal.pop(Gunfight.groupe_principal.index(Gunfight.sheriff))
Gunfight.groupe_principal.pop(Gunfight.groupe_principal.index(Gunfight.bandit))
Gunfight.groupe_principal.pop(
    Gunfight.groupe_principal.index(Gunfight.label_avertissement)
)

###############################
# AFFICHAGE DE L'ECRAN DE FIN #
###############################
Gunfight.groupe_principal.append(Gunfight.ecran_fin)
Gunfight.groupe_principal.append(Gunfight.portrait_J1)
Gunfight.groupe_principal.append(Gunfight.portrait_J2)
Gunfight.groupe_principal.append(Gunfight.label_score_final)

# Gunfight.portrait_J1.hidden = True
# Gunfight.portrait_J2.hidden = True

###########################
# BOUCLE D'ATTENTE FINALE #
###########################

while True:
    if scoreJ1 == scoreJ2:
        Gunfight.label_score_final.text = "DRAW"

        Gunfight.label_score_final.x = 60
        Gunfight.label_score_final.y = 120

        Gunfight.portrait_J1.x = 10
        Gunfight.portrait_J1.y = 40

        Gunfight.portrait_J2.x = 80
        Gunfight.portrait_J2.y = 40
        break
    elif scoreJ1 > scoreJ2:
        Gunfight.label_score_final.text = f"{scoreJ1}"

        Gunfight.label_score_final.x = 30
        Gunfight.label_score_final.y = 120

        Gunfight.portrait_J1.x = 20
        Gunfight.portrait_J1.y = 40
        Gunfight.portrait_J2.hidden = True
        break
    elif scoreJ1 < scoreJ2:
        Gunfight.label_score_final.text = f"{scoreJ2}"

        Gunfight.label_score_final.x = 30
        Gunfight.label_score_final.y = 120

        Gunfight.portrait_J2.x = 20
        Gunfight.portrait_J2.y = 40
        Gunfight.portrait_J1.hidden = True
        break
while True:
    if Controles.bouton_start.value == Controles.appuye:
        supervisor.reload()
