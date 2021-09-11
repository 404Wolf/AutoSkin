from time import sleep
import requests

ign = None

#change the user's skin to to {num}.png
def changeSkin(style,num,bearer):
    current_png = open(f'output/{num}.png', 'rb') #open the skin file in binary mode

    #files header for the request to change skin
    files = {
        'variant': (None, style),
        'file': (f'output/{num}.png', current_png),
    }

    #auth header for the request to change skin
    headers = {"Authorization":"Bearer "+bearer}

    #make request, and if it's successful move on
    #and if it isn't, try again (max 3 attempts)
    attempt = 0
    while True: #try to change skin 3 times, or break on success
        #req is a variable that stores the status code for a skin change request
        req = requests.post(url="https://api.minecraftservices.com/minecraft/profile/skins",
        headers=headers,files=files).status_code
        if req == 200:
            break #skin change succeded, so break
        else:
            if attempt >= 3:
                print("Error changing skin")
            sleep(3)
        attempt += 1 #upon fail, increase attempt counter

    current_png.close() #close the png file
