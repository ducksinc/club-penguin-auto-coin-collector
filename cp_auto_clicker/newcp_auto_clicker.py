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
import random

DELAY_MOVES = 15
# Timer for mouse movement.
D = 1
# Number of moves to be made by auto clicker. 8 cycles is enough to collect the Puffle treasure at the right time with default configuration.
SIZE = 8
# Images folder location.
FOLDER_PATH = "./img/"
GROUND_FOLDER_PATH = FOLDER_PATH + "ground/"
# Ground image list.
GROUND_COLORS = [[103, 80, 76], [91, 70, 67], [87, 67, 64], [95, 73, 70]]
# Icon matcher settings.
GRAYSCALE = True
CONFIDENCE = .9

# AutoClicker class. Handles all moves.
class AutoClicker():
    __size = 0
    __current = 0
    __debug = None
    __screen_size = None
    __screen_left = 0
    __screen_top = 0
    __screen_width = 0
    __screen_height = 0
    __width_range = 0
    __height_range = 0

    def __init__(self):
        self.__size = SIZE
        self.__current = 0
        self.__debug = False
        self.__screen_size = pg.size()
        # Coordinates for area that the program will search to see if it is open to be clicked on.
        # 0 is for width and 1 is for height.
        self.__screen_left = round(self.__screen_size[0]*.2617)
        self.__screen_top = round(self.__screen_size[1]*.5382)
        self.__screen_width = round(self.__screen_size[0]*.5371)
        self.__screen_height = round(self.__screen_size[1]*.3542)
        # Coordinates for calculating a random integer to be clicked on.
        self.__width_range = round(self.__screen_size[0]*.7988)
        self.__height_range =  round(self.__screen_size[1]*.8924)

    # Prints screen size. For debugging.
    def __print_screen_size(self):
        print("Screen size: height=" + str(self.__screen_size[1]) + ", width=" + str(self.__screen_size[0]))
        print("Borders: left=" + str(self.__screen_left) + ", top=" + str(self.__screen_top) + ", width=" + str(self.__screen_width) + ", height=" + str(self.__screen_height))
        pg.screenshot("screen_borders.png", region=(self.__screen_left, self.__screen_top, self.__screen_width, self.__screen_height))

    # Gets current position. For debugging.
    def __get_pos(self):
        return pg.position()

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
        found = False
        while True:
            x = random.randint(self.__screen_left, self.__width_range)
            y = random.randint(self.__screen_top, self.__height_range)
            for ground_color in GROUND_COLORS:
                if pg.pixelMatchesColor(x, y, (ground_color[0], ground_color[1], ground_color[2])):
                    found = True
                if found == True:
                    break
            if found == True:
                break
            
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
        if self.__debug == True:
            if money_icon_location == None:
                print("Puffle money icon either not found or not yet ready to be collected.")
        pg.click(money_icon_location)
        time.sleep(D)

    # Recursively calls auto_click. Starts with getting Puffle money bag, then runs until current is equal to size, then resets current to 0 and loops.
    def auto_click(self, current):
        while True:
            if current == 0:
                if self.__debug == True:
                    print("Running Puffle...")
                    if self.__get_pos() != None:
                        print("Current location: " + str(self.__get_pos()))
                    else:
                        print("Unable to find cursor location.")
                self.__run_puf()
            if current == SIZE:
                current = 0
            if self.__debug == True:
                print("Running iteration " + str(current))
                if self.__get_pos() != None:
                    print("Current location: " + str(self.__get_pos()))
                else:
                    print("Unable to find cursor location.")
            self.__move_click(current)
            self.auto_click(current+1)

    # Returns current.
    def get_current(self):
        return self.__current

    # Sets debug mode (default off).
    def set_debug(self, mode):
        print("Debug mode on.")
        self.__debug = mode
        if mode == True:
            self.__print_screen_size()

# Creates and runs auto clicker.
def main():
    start = input("Run auto clicker? (y/n): ")
    if start.lower() == "y" or "d":
        auto_clicker = AutoClicker()
        print("Running... (Ctrl + C while this window is selected to end.)")
        print(start)
        if start.lower() == "d":
            auto_clicker.set_debug(True)
        while True:
            auto_clicker.auto_click(auto_clicker.get_current())
    else:
        input("Goodbye.")
        
while __name__ == "__main__":
    main()