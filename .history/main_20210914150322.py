import skinApply #to send requests to mojang's api to skin change
import skinGen #skin gen script, to generate skins from the image
from time import sleep #import sleep from time, to add cooldowns
from requests import post #to make skin change requests
from keyboard import press_and_release,is_pressed #simulate control+r presses
from webbrowser import open #for opening the namemc profile in a browser
from MsAuth import login #for logging into microsoft accounts
from colorama import Fore,init
init() #activate colorama

ign = None #ign will later be stored in this variable

#prompt the user to set up the variables
def promptUser():
    global email
    global password
    global style

    #prompt user for account's email
    print(f"{Fore.YELLOW}Input your account's email{Fore.GREEN}")
    while True:
        email = input(">")
        if "@" in email: #make sure it's a real email
            print()
            break
        else: #if it isn't, have them try again
            print(f"{Fore.RED}Make sure to enter a valid email!{Fore.GREEN}")

    #prompt user for account's password
    print(f"{Fore.YELLOW}Input your account's password{Fore.GREEN}")
    password = input(">")
    print()

    #prompt user for the style of the skins
    #("slim" or "classic")
    print(f"{Fore.YELLOW}Input the style of the skins ({Fore.BLUE}\"slim\"{Fore.YELLOW} or {Fore.BLUE}\"classic\"{Fore.YELLOW}){Fore.GREEN}")
    while True:
        style = input(">")
        if style in ["slim","classic"]:
            print()
            break
        else:
            #if it isn't, have them try again
            print(f"{Fore.RED}Please try again, the options are \"slim\" or \"classic\".{Fore.GREEN}")

    #confirm the user's choices
    print(f"{Fore.YELLOW}Setting up auto-apply bot with email \""+email+"\"...\n")
    print(f"{Fore.YELLOW}Once started, your browswer will open, to cache skins on NameMC")
    print(f"{Fore.YELLOW}DO NOT USE YOUR PC while the skins are being applied.")
    print(f"{Fore.YELLOW}This process will take 4-8 minutes or so.")
    print(f"{Fore.YELLOW}To stop the program at any point, press control+space\n")
    input(f"{Fore.YELLOW}Press {Fore.BLUE}[Enter]{Fore.YELLOW} to start{Fore.GREEN}")

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
            print(f"{Fore.YELLOW}Username was detected to be \""+ign+"\"\n")
        bearer = authRequest['accessToken']
        return bearer #return the bearer obtained via the request
    except KeyError:
        authRequest = login(email,password)
        if ign == None: #if the ign has not been set yet, grab from request data
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
