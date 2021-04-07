"""@package GPIO_drive.py
Tento modul obstarává čtení GPIO a zápis hodnoty na GPIO.
Využívá knihovnu RPi.GPIO.
"""

import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

def GPIO_read(pin):
    """
    čtení požadovaného GPIO pinu, nastavuje požadovaný pin jako vstupní a čte jeho hodnotu.
    :param pin:
    :return:
    """
    GPIO.setup(pin, GPIO.IN)
    value = GPIO.input(pin)
    return value


def GPIO_write(pin, value):
    """
    zápis na požadovaný GPIO pin, nastavuje požadovaný pin jako výtupní a připisuje mu požadovanou hodnotu.
    :param pin:
    :param value:
    :return:
    """
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, value)
