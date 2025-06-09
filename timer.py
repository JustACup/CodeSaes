import time

class TON :
    # Initialisation de la temporisation
    def __init__(self, IN=0):
        self.IN = IN
        self.Busy = 0
    # Détermination de la valeur de la sortie de la temporisation
    def maj(self,duree) :
        self.PresetTime = duree
        if self.IN :
            if self.Busy == 0 :
                self.StartTime = time.monotonic()
                self.Busy = 1
            self.TimerElapsedTime = time.monotonic() - self.StartTime
            if self.TimerElapsedTime >= self.PresetTime :
                self.Q=1
            else :
                self.Q=0
        else :
            self.Q = 0
            self.Busy = 0
