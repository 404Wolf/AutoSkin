from time import sleep  # import sleep from time, to add cooldowns
from keyboard import press_and_release, is_pressed  # simulate control+r presses
from webbrowser import open  # for opening the namemc profile in a browser
from colorama import Fore, init
from utils import *

init()  # activate colorama
ign = None  # ign will later be stored in this variable

# have user choose between random generation mode, or namemc art mode
print(
    f"{Fore.YELLOW}Would you like to generate/apply {Fore.CYAN}[N]{Fore.YELLOW}ameMC Skin Art, or {Fore.CYAN}[R]{Fore.YELLOW}andomly generate and cache skins? (n/r){Fore.GREEN}"
)
while True:
    mode = input("> ").lower()
    if mode in ["n", "r"]:
        print()
        break
    else:
        print(
            f"{Fore.RED}Invalid mode chosen. Please choose from {Fore.CYAN}[N]{Fore.RED} or {Fore.CYAN}[R]{Fore.RED}.{Fore.GREEN}"
        )

# prompt user for account's email
print(f"{Fore.YELLOW}Input your account's email{Fore.GREEN}")
while True:
    email = input("> ")
    if "@" in email:  # make sure it's a real email
        print()
        break
    else:  # if it isn't, have them try again
        print(f"{Fore.RED}Make sure to enter a valid email!{Fore.GREEN}")

# prompt user for account's password
print(f"{Fore.YELLOW}Input your account's password{Fore.GREEN}")
password = input("> ")
print()

# prompt user for the style of the skins
# ("slim" or "classic")
print(
    f'{Fore.YELLOW}Input the style of the skins ({Fore.CYAN}"slim"{Fore.YELLOW} or {Fore.CYAN}"classic"{Fore.YELLOW}){Fore.GREEN}'
)
while True:
    style = input("> ")
    if style in ["slim", "classic"]:
        print()
        break
    else:
        # if it isn't, have them try again
        print(
            f'{Fore.RED}Please try again, the options are {Fore.CYAN}"slim"{Fore.RED} or {Fore.CYAN}"classic"{Fore.RED}.{Fore.GREEN}'
        )

# confirm the user's choices
print(
    f'{Fore.YELLOW}Setting up auto-apply bot with email {Fore.CYAN}"{email}"{Fore.YELLOW}...\n'
)

# user is applying NameMc art
if mode == "n":
    print(f"{Fore.YELLOW}Generating skins...")
    skins_gen()
    print(
        f'{Fore.GREEN}Skins succesfully generated! They can be found in the {Fore.CYAN}"output"{Fore.GREEN} folder!\n'
    )

    print(f"{Fore.YELLOW}Would you like the bot to apply your skins? (y/n){Fore.GREEN}")
    apply_skins = input("> ").lower()
    while True:
        if apply_skins == "n":
            apply_skins = False
            break
        elif apply_skins == "y":
            apply_skins_warn()
            apply_skins = True
            break
        else:
            print(
                f'{Fore.RED}Make sure to only enter {Fore.CYAN}"y"{Fore.RED} or {Fore.CYAN}"n"{Fore.GREEN}'
            )

    if apply_skins:
        bearer, ign = auth(email, password)  # obtain a bearer
        print()

        # open the namemc profile in a new window, and bring it to the top of the screen
        open("http://namemc.com/profile/" + ign.lower(), new=1, autoraise=True)

        if mode == "n":
            for skin in range(27):
                skin += 1  # increase by 1 since range() is index 0

                changeSkin(
                    style, "output/" + str(skin), bearer
                )  # use bearer to change skin

                # print status message once skin has been changed
                print(
                    f"{Fore.GREEN}Skin {Fore.CYAN}{str(skin)}{Fore.GREEN} applied successfully"
                )

                interruptible_sleep(
                    3
                )  # sleep for 3 seconds, but make it so the user can break the sleep cleanly

                # reload tab
                press_and_release("control+r")

                # print statusu message once tab is reloaded
                print(
                    f"{Fore.GREEN}Skin {Fore.CYAN}{str(skin)}{Fore.GREEN} cached on NameMC successfully"
                )

                interruptible_sleep(
                    3
                )  # sleep for 3 seconds, but make it so the user can break the sleep cleanly

    else:
        print(
            f"{Fore.YELLOW}To manually apply skins, make sure to apply from 27 down, and make sure to reload the NameMC profile so they cache.{Fore.GREEN}"
        )
        print(f"{Fore.YELLOW}Program will close in 5 seconds...")
        sleep(5)
        print(f"{Fore.RED}Exiting...")
        exit()

# user wants indefinite random skin generation
elif mode == "r":
    apply_skins_warn()

    print()
    bearer, ign = auth(email, password)  # obtain a bearer
    print()

    # open the namemc profile in a new window, and bring it to the top of the screen
    open("http://namemc.com/profile/" + ign.lower(), new=1, autoraise=True)

    i = 0  # create counter for log messages
    while True:
        i += 1  # tick up counter

        random_skin_gen()  # generate random skin (path is current.png)

        changeSkin(style, "current", bearer)  # use bearer to change skin

        # print status message once skin has been changed
        print(f"{Fore.GREEN}Skin #{Fore.CYAN}{str(i)}{Fore.GREEN} applied successfully")

        interruptible_sleep(
            3
        )  # sleep for 3 seconds, but make it so the user can break the sleep cleanly

        # reload tab
        press_and_release("control+r")

        # print statusu message once tab is reloaded
        print(
            f"{Fore.GREEN}Skin #{Fore.CYAN}{str(i)}{Fore.GREEN} cached on NameMC successfully"
        )

        interruptible_sleep(
            3
        )  # sleep for 3 seconds, but make it so the user can break the sleep cleanly
