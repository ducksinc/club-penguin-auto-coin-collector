'''
Auto clicker for the mining room in Club Penguin.
Made for 2560x1440 monitors; specifically, made for the NewCP client while scrolled all the way down.
Make sure the monitor running Club Penguin is set as your primary monitor.
Authors:
@ChrisDaDerp
@ZoomKahow
'''
 
import pyautogui as pg 
import time

DELAY_MOVES = 15
# Timer for mouse movement.
D = 1
# Number of moves to be made by auto clicker.
SIZE = 8
# Images folder location.
FOLDER_PATH = "./img/"
# Icon matcher settings.
GRAYSCALE = True
CONFIDENCE = .9

# AutoClicker class. Handles all moves.
class AutoClicker():
    __size = 0
    __current = 0
    __debug = False

    def __init__(self):
        self.__size = SIZE
        self.__current = 0
        self.debug = False

    # Gets current position. For debugging.
    def __get_pos(self):
        print(pg.size())
        print(pg.position())

    # Clicks penguin then mines.
    def __click_mine(self):
        penguin_icon_location = pg.locateCenterOnScreen(FOLDER_PATH + "penguin_icon.png", grayscale=GRAYSCALE, confidence=CONFIDENCE)
        pg.click(penguin_icon_location)
        time.sleep(D)
        dance_icon_location = pg.locateCenterOnScreen(FOLDER_PATH + "dance_icon.png", grayscale=GRAYSCALE, confidence=CONFIDENCE)
        pg.click(dance_icon_location)
        time.sleep(D)

    # Moves cursor to coordinates and then clicks. Set on a delay to maximize profits from mining.
    def __move_click(self, current):
        if current == 0:
            x = 1051
            y = 628
        elif current == 1:
            x = 1374
            y = 652
        elif current == 2:
            x = 1893
            y = 780
        elif current == 3:
            x = 1980
            y = 972
        elif current == 4:
            x= 1625
            y = 1094
        elif current == 5:
            x = 1230
            y = 1099
        elif current == 6:
            x = 795
            y = 948
        else:
            x = 848 
            y = 703
        pg.moveTo(x, y, .1)
        pg.click(x, y)
        time.sleep(D*1.3)
        self.__click_mine()
        time.sleep(DELAY_MOVES)

    # Clicks Puffle icon, then money bag.
    def __run_puf(self):
        puffle_icon_location = pg.locateCenterOnScreen(FOLDER_PATH + "puffle_icon.png", grayscale=GRAYSCALE, confidence=CONFIDENCE)
        pg.click(puffle_icon_location)
        time.sleep(D)
        money_icon_location = pg.locateCenterOnScreen(FOLDER_PATH + "money_icon.png", grayscale=GRAYSCALE, confidence=CONFIDENCE)
        pg.click(money_icon_location)
        time.sleep(D)

    # Recursively calls auto_click. Starts with getting Puffle money bag, then runs until current is equal to size, then resets current to 0 and loops.
    def auto_click(self, current):
        while True:
            if current == 0:
                if self.__debug == True:
                    print("Running Puffle...")
                    print("Current location: " + self.__get_pos())
                self.__run_puf()
            if current == SIZE:
                current = 0
            if self.__debug == True:
                print("Running iteration " + str(current))
                print("Current location: " + self.__get_pos())
            self.__move_click(current)
            self.auto_click(current + 1)

    # Returns current.
    def get_current(self):
        return self.__current

    # Sets debug mode (default off).
    def set_debug(self, mode):
        self.__debug = mode

# Creates and runs auto clicker.
def main():
    start = str(input("Run auto clicker? (y/n): "))
    if start.lower() == "Y" or "D":
        print("Running... (Ctrl + C while this window is selected to end.)")
    while start.lower() == "Y" or "D":
        auto_clicker = AutoClicker()
        if start.lower() == "D":
            auto_clicker.set_debug(True)
        auto_clicker.auto_click(auto_clicker.get_current())
    else:
        print("Goodbye.")
        
while __name__ == "__main__":
    main()