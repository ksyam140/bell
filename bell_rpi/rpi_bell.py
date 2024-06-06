import RPi.GPIO as GPIO
import time
import tkinter as tk
import json
import os

# Chemin du fichier de configuration
CONFIG_FILE = "conf/config.json"

GPIO.setwarnings(False)

status = "Unknown"

# Fonction pour lire la configuration depuis un fichier JSON
def read_config(config_file):
    if os.path.exists(config_file):
        print(config_file)
        with open(config_file, "rt") as file:
            return json.load(file)
   
# Fonction pour écrire la configuration dans un fichier JSON
def write_config(config_file):
    with open(config_file, "wt") as file:
        json.dump(config, file)

# Lire la configuration initiale
config = read_config(config_file=CONFIG_FILE)
motor_gpio = config["motor_gpio"]
button_gpio = config["button_gpio"]
motor_duration = config["motor_duration"]

# Configuration des broches GPIO
#  - GPIO.BCM : Numero de GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(motor_gpio, GPIO.OUT)  # Broche pour contrôler le moteur
GPIO.setup(button_gpio, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Broche pour lire l'état du bouton

# Fonction pour démarrer le moteur
def open_bell():
    print("opening the bell")
    GPIO.output(motor_gpio, GPIO.LOW)
    time.sleep(motor_duration)

# Fonction pour arrêter le moteur
def close_bell():
    print("closing the bell")
    GPIO.output(motor_gpio, GPIO.HIGH)
    time.sleep(motor_duration)
   
# Fonction pour savoir la position de la cloche
def get_bell_status():
    motor_status = GPIO.input(motor_gpio)
    button_status = GPIO.input(button_gpio)
    print(f"motor_status = {motor_status}, button_status = {button_status}")
   
    pos_status_str = ""
    move_status_str = ""
   
    if motor_status == GPIO.HIGH:
        pos_status_str = "close"
    else:
        pos_status_str = "open"
       

    if button_status == GPIO.LOW:
        move_status_str = "move"
    else:
        move_status_str = "stop"

    status = pos_status_str + " " + move_status_str
    status_label.config(text=status)
    print(f"status = {status}")

# Fonction pour afficher le statut
def show_status():
    current_status = status_bell()
    status_label.config(text=f"Status: {current_status}")

# Création de l'interface graphique
root = tk.Tk()
root.title("Contrôle du moteur")

start_button = tk.Button(root, text="Open", command=open_bell)
start_button.pack(pady=10)

stop_button = tk.Button(root, text="Close", command=close_bell)
stop_button.pack(pady=10)

status_button = tk.Button(root, text="Status", command=get_bell_status)
status_button.pack(pady=10)

status_label = tk.Label(root, text=f"Status: {status}")
status_label.pack(pady=10)

# Fonction pour gérer la fermeture de l'application
def on_closing():
    GPIO.cleanup()
    write_config(config)
    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_closing)

# Lancer la boucle principale de Tkinter
root.mainloop()