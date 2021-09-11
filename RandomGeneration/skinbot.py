from PIL import Image
from random import randrange,choice
from time import sleep
import requests
import keyboard
import asyncio
from pyppeteer import launch

#prompt user for information on the account
#asks them for:
def promptUser():
    global email
    global password
    global ign
    print("Input your account's email")
    email = input(">")
    print()
    print("Input your account's password")
    password = input(">")
    print("\nSetting up skinbot with email \""+email+"\" and password \""+password+"\"...\n"+
    "Press [Enter] to confirm!")

#auth an account
#requires email+password of the account, and works for microsoft or mojang accounts
#also sets the global "ign" variable to the ign of the account, if unset already
#returns the account's bearer
def auth(email,password):
    global ign

    try:
        #make a change skin request, and store the data
        authRequest = post(
        "https://authserver.mojang.com/authenticate",
        json={"agent": {"name": "Minecraft", "version": 1},
         "username": email,"password": password}).json()
        if ign == None: #if the ign has not been set yet, grab from request data
            ign = authRequest['selectedProfile']['name']
            print("ign was detected to be \""+ign+"\"\n")
        bearer = authRequest['accessToken']
        return bearer #return the bearer obtained via the request
    except KeyError:
        authRequest = login(email,password)
        if ign == None: #if the ign has not been set yet, grab from request data
            ign = authRequest['username']
            print("ign was detected to be \""+ign+"\"\n")
        bearer = authRequest['access_token']
        return bearer

#function to randomly generate a new minecraft skin
#note: uses the base.png file's white area as a template
def skinGen():
    im = Image.open("base.png")
    pixels = im.load()
    for x in range(128):
        for y in range(128):
            try:
                pixel = list(pixels[x,y])
                if pixel == [255, 255, 255, 255]:
                    pixels[x,y] = (
                    randrange(50,255),
                    randrange(10,50),
                    randrange(50,100),
                    randrange(0,255))
                if pixel == [255, 255, 255]:
                    pixels[x,y] = (
                    randrange(50,100),
                    randrange(10,50),
                    randrange(50,100))
            except IndexError:
                pass
    im.save("current.png")
    print("Generated skin!")

#function to change the skin of an accounts
#relys on the global "bearer" variable for the minecraft account
def changeSkin():
    global bearer
    current_png = open('current.png', 'rb')
    files = {
        'variant': (None, choice(["slim","classic"])),
        'file': ('current.png', current_png),
    }
    headers = {"Authorization":"Bearer "+auth(email,password)}
    if requests.post(url="https://api.minecraftservices.com/minecraft/profile/skins",headers=headers,files=files).status_code == 200:
        print("Skin Changed!")
    current_png.close()

#main function to create a simulated browser, to cache the skin on NameMC
async def main():
    while True:
        browser = await launch(headless=False) #launch a headed browser
        page = await browser.newPage() #make a new tab
        url = ("https://namemc.com/profile/"+ign).lower()
        await page.goto(url,waitUntil='domcontentloaded') #go to the url
        await asyncio.sleep(5.5)
        skinGen()
        changeSkin()
        await browser.close() #close browser

promptUser() #prompt user for info on account login
asyncio.run(main()) #start the browser; and the loop to generate+upload skins
