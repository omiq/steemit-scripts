import os
import readchar

# place in your start up file:
# sudo nano ./.bashrc


def menu():
    while True:
        os.system('clear')
        print("\t\tChoose from the following options:\n\n")
        print("\t\tk: Kodi")
        print("\t\tr: Retro Pi")
        print("\t\tx: XWindows")
        print("\n\t\tEnter to quit to terminal\n\n\n")

        # Read a key
        key = readchar.readkey()
        if(key == 'k'):
            print("Launch Kodi")
            os.system("kodi")
        elif(key == 'r'):
            print("Launch RetroPie")
            os.system("emulationstation")
        elif(key == 'x'):
            print("Launch X Windows")
            os.system("startx")
        elif(key == readchar.key.ENTER):
            print("Exit to terminal")
            break
        else:
            print("Please choose an option from above")


if __name__ == "__main__":
    menu()
