import RPi.GPIO as GPIO
from data.dico_couleurs import dico_couleurs


class LedRgb:
    def __init__(self, r_pin: int, g_pin: int, b_pin: int):
        # définition des pins
        self.pins = (r_pin, g_pin, b_pin)

        self.setup()

    def setup(self):
        GPIO.setwarnings(False)  # désactive les warnings parce que qui en a quelque chose à faire sérieusement :lul:
        GPIO.setmode(GPIO.BCM)  # on fonctionne en utilisant le numéro de GPIO pas le numéro de broche

        # définition des pins en sortie
        for pin in self.pins:
            GPIO.setup(pin, GPIO.OUT)

    def set_color(self, couleur: str):
        color = dico_couleurs[couleur]
        for i in range(2):
            if color[i]:
                GPIO.output(self.pins[i], GPIO.HIGH)
            else:
                GPIO.output(self.pins[i], GPIO.LOW)

    def stop(self):
        for i in range(2):
            GPIO.output(self.pins[i], GPIO.LOW)
