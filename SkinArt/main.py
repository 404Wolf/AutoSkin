import skinApply #skin apply script, to send requests to mojang's api to skin change
import skinGen #skin gen script, to generate skins from the image
from time import sleep #import sleep from time, to add cooldowns
from requests import post #import post requests from requests, to make skin change requests
from keyboard import press_and_release,is_pressed #import keyboard module functions, for simulating control+r presses, and enabling an exit command
from webbrowser import open #for opening the namemc profile in a browser, to cache skins on namemc
from MsAuth import login #for logging into microsoft accounts

ign = None #ign will later be stored in this variable

#prompt the user to set up the variables
def promptUser():
    global email
    global password
    global style

    #prompt user for account's email
    print("Input your account's email")
    while True:
        email = input(">")
        if "@" in email: #make sure it's a real email
            print()
            break
        else: #if it isn't, have them try again
            print("Make sure to enter a valid email!")

    #prompt user for account's password
    print("Input your account's password")
    password = input(">")
    print()

    #prompt user for the style of the skins
    #("slim" or "classic")
    print("Input the style of the skins (\"slim\" or \"classic\")")
    while True:
        style = input(">")
        if style in ["slim","classic"]:
            print()
            break
        else:
            #if it isn't, have them try again
            print("Please try again, the options for skin style are \"slim\" or \"classic\".")

    #confirm the user's choices
    print("Setting up auto-apply bot with email \""+email+"\"...\n")
    print("Once started, chrome will open and close multiple times, to cache the skins in NameMC")
    print("Do not stop the script until all skins have been applied.")
    print("This process will take 5-10 minutes or so.")
    print("\nThis program will simulate control+r keypresses.")
    print("To stop the program at any point, press control+space\n")
    input("Press [Enter] to start")

#get a bearer to a mojang account with username+pass
def auth(email,password):
    global ign
    
    try:
        #make a change skin request, and store the data
        authRequest = post("https://authserver.mojang.com/authenticate", json={"agent": {"name": "Minecraft", "version": 1}, "username": email,"password": password}).json()
        if ign == None: #if the ign has not been set yet, grab it from the request data
            ign = authRequest['selectedProfile']['name']
            print("ign was detected to be \""+ign+"\"\n")
        bearer = authRequest['accessToken']
        return bearer #return the bearer obtained via the request
    except KeyError:	
        authRequest = login(email,password)
        if ign == None: #if the ign has not been set yet, grab it from the request data
            ign = authRequest['username']
            print("ign was detected to be \""+ign+"\"\n")
        bearer = authRequest['access_token']
        return bearer

promptUser()
print()

auth(email,password)

#function to check if exit keybind is being held
def check_exit():
    if is_pressed("control+space"):
        print("Exiting!")
        exit()

#open the namemc profile in a new window, and bring it to the top of the screen
open('http://namemc.com/profile/'+ign.lower(),new=1,autoraise=True)

for skin in range(27):
    skin += 1 #increase by 1 since range() is index 0

    bearer = auth(email,password) #obtain a bearer
    skinApply.changeSkin(style,skin,bearer) #use bearer to change skin

    for x in range(300): #sleep for 3 seconds
        sleep(.01)
        check_exit()

    #print status message once skin has been changed
    print("Skin "+str(skin)+" applied successfully")

    #reload tab
    press_and_release("control+r")

    for x in range(300): #sleep for 3 seconds
        sleep(.01)
        check_exit()

    #print statusu message once tab is reloaded
    print("Skin "+str(skin)+" cached on NameMC successfully")