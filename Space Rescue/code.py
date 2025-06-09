#############################################
# IMPORTATION DES DIFFERENTES BIBLIOTHEQUES #
#############################################
# Modules Natifs
import time
import random
import supervisor
# Modules du dossier 'lib'
import Ressources_tutoriel
import Gestion_controles

######################################
#  INSTANCIATION DES OBJETS UTILES   #
######################################
######################################

Tutoriel = Ressources_tutoriel.tutoriel()

Controles = Gestion_controles.controles()

score = 0
recuperation_astronaute = False
chrono = 60
sens_deplacement_asteroide_x = 1
sens_deplacement_asteroide_y = 1
compteur_barre_vie = 6
collision_asteroide = False
fin_de_partie = False
compteur_ralentissement_animation = 0

temps_enregistre = time.monotonic()

Tutoriel.groupe_principal.append(Tutoriel.ecran_titre)

Tutoriel.groupe_principal.append(Tutoriel.bouton_start)
Tutoriel.bouton_start.x = 40
Tutoriel.bouton_start.y = 110

Tutoriel.ecran.root_group = Tutoriel.groupe_principal

time.sleep(1)
Tutoriel.audio_pwm1.play(Tutoriel.bruitage_ecran_titre)

#####################
# BOUCLE PRINCIPALE #
#####################
while Controles.bouton_start.value == Controles.relache:
    Tutoriel.bouton_start.hidden = False
    time.sleep(0.5)
    Tutoriel.bouton_start.hidden = True
    time.sleep(0.5)
Tutoriel.audio_pwm1.stop()
Tutoriel.audio_pwm2.play(Tutoriel.bruitage_start)
time.sleep(1)

Tutoriel.groupe_principal.pop(Tutoriel.groupe_principal.index(Tutoriel.ecran_titre))
Tutoriel.groupe_principal.pop(Tutoriel.groupe_principal.index(Tutoriel.bouton_start))

Tutoriel.groupe_principal.append(Tutoriel.portrait)

Tutoriel.groupe_principal.append(Tutoriel.label1_regles)
Tutoriel.groupe_principal.append(Tutoriel.label2_regles)
Tutoriel.groupe_principal.append(Tutoriel.label3_regles)
Tutoriel.label3_regles.text = "Regles randoms"

Tutoriel.groupe_principal.append(Tutoriel.bouton_start)
time.sleep(1)

while Controles.bouton_start.value == Controles.relache:
    Tutoriel.bouton_start.hidden = False
    time.sleep(0.25)
    Tutoriel.bouton_start.hidden = True
    time.sleep(0.25)
Tutoriel.audio_pwm2.play(Tutoriel.bruitage_start)
time.sleep(1)

Tutoriel.groupe_principal.pop(Tutoriel.groupe_principal.index(Tutoriel.portrait))
Tutoriel.groupe_principal.pop(Tutoriel.groupe_principal.index(Tutoriel.label1_regles))
Tutoriel.groupe_principal.pop(Tutoriel.groupe_principal.index(Tutoriel.label2_regles))
Tutoriel.groupe_principal.pop(Tutoriel.groupe_principal.index(Tutoriel.label3_regles))
Tutoriel.groupe_principal.pop(Tutoriel.groupe_principal.index(Tutoriel.bouton_start))

Tutoriel.groupe_principal.append(Tutoriel.ecran_jeu)

Tutoriel.groupe_principal.append(Tutoriel.label_score)
Tutoriel.groupe_principal.append(Tutoriel.label_chrono)
Tutoriel.groupe_principal.append(Tutoriel.astronaute)
Tutoriel.groupe_principal.append(Tutoriel.vaisseau)
Tutoriel.groupe_principal.append(Tutoriel.asteroide)
Tutoriel.groupe_principal.append(Tutoriel.barre_vie)
time.sleep(1)

while not fin_de_partie:
    if (
        Controles.bouton_gauche.value == Controles.appuye
        or Controles.joystick_horizontal.value < 15000
    ):
        Tutoriel.vaisseau[0] = 4
        Tutoriel.vaisseau.x = Tutoriel.vaisseau.x - 1
        if Tutoriel.vaisseau.x < -Tutoriel.largeur_vaisseau:
            Tutoriel.vaisseau.x = 159
    if (
        Controles.bouton_droite.value == Controles.appuye
        or Controles.joystick_horizontal.value > 51000
    ):
        Tutoriel.vaisseau[0] = 5
        Tutoriel.vaisseau.x = Tutoriel.vaisseau.x + 1
        if Tutoriel.vaisseau.x > 159:
            Tutoriel.vaisseau.x = -Tutoriel.largeur_vaisseau
    if (
        Controles.bouton_haut.value == Controles.appuye
        or Controles.joystick_vertical.value > 51000
    ):
        Tutoriel.vaisseau[0] = 3
        Tutoriel.vaisseau.y = Tutoriel.vaisseau.y - 1
        if Tutoriel.vaisseau.y < -Tutoriel.hauteur_vaisseau:
            Tutoriel.vaisseau.y = 127
    if (
        Controles.bouton_bas.value == Controles.appuye
        or Controles.joystick_vertical.value < 15000
    ):
        Tutoriel.vaisseau[0] = 3
        Tutoriel.vaisseau.y = Tutoriel.vaisseau.y + 1
        if Tutoriel.vaisseau.y > 127:
            Tutoriel.vaisseau.y = -Tutoriel.hauteur_vaisseau
    if Controles.bouton_start.value == Controles.appuye:
        break
    if Tutoriel.collision(Tutoriel.vaisseau, Tutoriel.astronaute):
        Controles.LED_test.value = True
        if recuperation_astronaute is False:
            recuperation_astronaute = True
            score = score + 1
            Tutoriel.audio_pwm2.play(Tutoriel.bruitage_astronaute)
            Tutoriel.label_score.text = f"{score:02d}"
            time.sleep(0.25)
            while True:
                Tutoriel.astronaute.x = random.randint(
                    0, Tutoriel.largeur_ecran - Tutoriel.largeur_astronaute
                )
                Tutoriel.astronaute.y = random.randint(
                    0, Tutoriel.hauteur_ecran - Tutoriel.hauteur_astronaute
                )
                if (
                    (Tutoriel.astronaute.x < Tutoriel.vaisseau.x)
                    or (
                        Tutoriel.astronaute.x
                        > Tutoriel.vaisseau.x + Tutoriel.largeur_vaisseau
                    )
                ) and (
                    (Tutoriel.astronaute.y < Tutoriel.vaisseau.y)
                    or (
                        Tutoriel.astronaute.y
                        > Tutoriel.vaisseau.y + Tutoriel.hauteur_vaisseau
                    )
                ):
                    break
    else:
        Controles.LED_test.value = False
        recuperation_astronaute = False
    temps_actuel = time.monotonic()
    if temps_actuel - temps_enregistre > 1:
        chrono = chrono - 1
        Tutoriel.audio_pwm1.play(Tutoriel.bruitage_chrono)
        if chrono == 0:
            fin_de_partie = True
        temps_enregistre = temps_actuel
        Tutoriel.label_chrono.text = f"0:{chrono}"
    Tutoriel.asteroide.x = (
        Tutoriel.asteroide.x + sens_deplacement_asteroide_x * random.randint(0, 1)
    )
    Tutoriel.asteroide.y = (
        Tutoriel.asteroide.y + sens_deplacement_asteroide_y * random.randint(0, 1)
    )
    if (Tutoriel.asteroide.x < 0) or (
        Tutoriel.asteroide.x > (Tutoriel.largeur_ecran - Tutoriel.largeur_asteroide)
    ):
        sens_deplacement_asteroide_x = -sens_deplacement_asteroide_x
    if (Tutoriel.asteroide.y < 0) or (
        Tutoriel.asteroide.y > (Tutoriel.hauteur_ecran - Tutoriel.hauteur_asteroide)
    ):
        sens_deplacement_asteroide_y = -sens_deplacement_asteroide_y
    if Tutoriel.collision(Tutoriel.vaisseau, Tutoriel.asteroide):
        if collision_asteroide is False:
            collision_asteroide = True
            compteur_barre_vie = compteur_barre_vie - 1
            Tutoriel.barre_vie[0] = 5 - compteur_barre_vie
            Tutoriel.audio_pwm2.play(Tutoriel.bruitage_explosion)
            print(f"Barre de vie : {compteur_barre_vie}")
            if compteur_barre_vie == 0:
                fin_de_partie = True
    else:
        collision_asteroide = False
    compteur_ralentissement_animation = compteur_ralentissement_animation + 1
    if compteur_ralentissement_animation >= 10:
        compteur_ralentissement_animation = 0
        Tutoriel.astronaute[0] = (Tutoriel.astronaute[0] + 1) % 8
    time.sleep(0.007)
Tutoriel.groupe_principal.pop(Tutoriel.groupe_principal.index(Tutoriel.ecran_jeu))
Tutoriel.groupe_principal.pop(Tutoriel.groupe_principal.index(Tutoriel.label_score))
Tutoriel.groupe_principal.pop(Tutoriel.groupe_principal.index(Tutoriel.label_chrono))
Tutoriel.groupe_principal.pop(Tutoriel.groupe_principal.index(Tutoriel.astronaute))
Tutoriel.groupe_principal.pop(Tutoriel.groupe_principal.index(Tutoriel.asteroide))
Tutoriel.groupe_principal.pop(Tutoriel.groupe_principal.index(Tutoriel.vaisseau))
Tutoriel.groupe_principal.pop(Tutoriel.groupe_principal.index(Tutoriel.barre_vie))

Tutoriel.groupe_principal.append(Tutoriel.ecran_fin)

Tutoriel.label_score_final.text = Tutoriel.label_score.text
Tutoriel.groupe_principal.append(Tutoriel.label_score_final)

Tutoriel.audio_pwm2.stop()
Tutoriel.audio_pwm1.stop()
time.sleep(1)
Tutoriel.audio_pwm2.play(Tutoriel.bruitage_game_over)

while True:
    if Controles.bouton_start.value == Controles.appuye :
        supervisor.reload()
