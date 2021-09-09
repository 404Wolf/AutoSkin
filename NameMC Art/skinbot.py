from random import randrange,choice
from time import sleep
import requests
import keyboard
from pyppeteer import launch
from PIL import Image

print("Welcome to Twilak's NameMC Bot!")

#get a bearer to a mojang account with username+pass
def auth():
    try:
        authRequest = requests.post("https://authserver.mojang.com/authenticate", json={"agent": {"name": "Minecraft", "version": 1}, "username": email,"password": password}).json()
        bearer = authRequest['accessToken']
        return bearer
    except KeyError:	
        print("Invalid Account!\n")

def changeSkin(num):
    global bearer
    global style
    current_png = open(f'{num}.png', 'rb')
    files = {
        'variant': (None, style),
        'file': (f'{num}.png', current_png),
    }
    headers = {"Authorization":"Bearer "+auth()}
    if requests.post(url="https://api.minecraftservices.com/minecraft/profile/skins",headers=headers,files=files).status_code == 200:
        print("Skin Changed!")
    current_png.close()

#prompt user for info to set up variables
print("Input your account's email")
while True:
    email = input(">")
    if "@" in email:
        print()
        break
    else:
        print("Make sure to enter a valid email!")

print("Input your account's password")
password = input(">")
print()

print("Input the style of the skins")
while True:
    style = input(">")
    if style in ["slim","classic"]:
        print()

print("\nSetting up auto-apply bot with email \""+email+"\" and password \""+"*"*len(password)+"\"...\n")
input("Press enter to start.")

for num in range(27):
    changeSkin(27-(num))
    keyboard.press_and_release("control+r")
    sleep(5.5)