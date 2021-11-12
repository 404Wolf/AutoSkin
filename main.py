import skinApply #to send requests to mojang's api to skin change
from skinGen import skinGen #skin gen script, to generate skins from the image
from MsAuth import login #for logging into microsoft accounts
from colorama import Fore,init
init() #activate colorama

print(f"{Fore.YELLOW}Generating skins...")

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
    print(f"{Fore.YELLOW}Input the style of the skins ({Fore.CYAN}\"slim\"{Fore.YELLOW} or {Fore.CYAN}\"classic\"{Fore.YELLOW}){Fore.GREEN}")
    while True:
        style = input(">")
        if style in ["slim","classic"]:
            print()
            break
        else:
            #if it isn't, have them try again
            print(f"{Fore.RED}Please try again, the options are {Fore.CYAN}\"slim\"{Fore.RED} or {Fore.CYAN}\"classic\"{Fore.RED}.{Fore.GREEN}")

    #confirm the user's choices
    print(f"{Fore.YELLOW}Setting up auto-apply bot with email {Fore.CYAN}\"{email}\"{Fore.YELLOW}...")

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
            print(f"{Fore.YELLOW}Username was detected to be {Fore.CYAN}\"{ign}\"{Fore.GREEN}")
        bearer = authRequest['accessToken']
        return bearer #return the bearer obtained via the request
    except KeyError:
        authRequest = login(email,password)
        if ign == None: #if the ign has not been set yet, grab from request data
            ign = authRequest['username']
            print(f"{Fore.YELLOW}Username was detected to be {Fore.CYAN}\"{ign}\"{Fore.GREEN}")
        bearer = authRequest['access_token']
        return bearer

skinGen()
print(f"{Fore.GREEN}Skins succesfully generated! They can be found in the {Fore.CYAN}\"output\"{Fore.GREEN} folder!")

print(f"{Fore.YELLOW}Would you like the bot to apply your skins? (y/n){Fore.GREEN}")
while True:
    apply_skins = input("> ").lower()
    if apply_skins == "n":
        apply_skins = False
        break
    elif apply_skins == "y":
        apply_skins = True
        break
    else:
        print(f"{Fore.RED}Make sure to only enter {Fore.CYAN}\"y\"{Fore.RED} or {Fore.CYAN}\"n\"{Fore.GREEN}")

if apply_skins:
    promptUser()
    print()
    print(f"{Fore.YELLOW}Once started, your browswer will open, to cache skins on NameMC")
    print(f"{Fore.RED}DO NOT{Fore.YELLOW} USE YOUR PC while the skins are being applied.")
    print(f"{Fore.YELLOW}This process will take 4-8 minutes or so.")
    print(f"{Fore.YELLOW}To stop the program at any point, press control+space\n{Fore.GREEN}")
    input(f"Press [Enter] to start!")
else:
    print(f"{Fore.YELLOW}To manually apply skins, make sure to apply from 27 down, and make sure to reload the NameMC profile so they cache.{Fore.GREEN}")
    sleep(.7)
    print(f"{Fore.RED}Exiting...")
    exit()

auth(email,password)

#function to check if exit keybind is being held
def check_exit():
    if is_pressed("control+space"):
        print(f"{Fore.RED}Exiting!{Fore.GREEN}")
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
    print(f"{Fore.GREEN}Skin {Fore.CYAN}{str(skin)}{Fore.GREEN} applied successfully")

    #reload tab
    press_and_release("control+r")

    for x in range(300): #sleep for 3 seconds
        sleep(.01)
        check_exit()

    #print statusu message once tab is reloaded
    print(f"{Fore.GREEN}Skin {Fore.CYAN}{str(skin)}{Fore.GREEN} cached on NameMC successfully")
