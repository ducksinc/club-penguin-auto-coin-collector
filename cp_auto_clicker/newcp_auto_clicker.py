'''
Auto clicker for the mining room in Club Penguin.
Made for 2560x1440 monitors; specifically, made for the NewCP client while scrolled all the way down.
Make sure the monitor running Club Penguin is set as your primary monitor.
Authors:
@ducksinc
@ZoomKahow
'''
 
import pyautogui as pg 
import time
import random
import os
import math

DELAY_MOVEMENT = 15
'''Timer to delay next movement. Default config optimized for mining the most coins.'''
DELAY_TIME = .2
'''Timer for mouse movement.'''
SIZE = 8
'''Number of moves to be made by auto clicker. 8 cycles is enough to collect the Puffle treasure at the right time with default configuration.'''
FOLDER_PATH = "./img/"
'''Images folder location.'''
GROUND_COLORS = [[103, 80, 76], [91, 70, 67], [87, 67, 64], [95, 73, 70]]
'''Ground RGB values list.'''
GRAYSCALE = True
'''Grayscale is true by default.'''
CONFIDENCE = .9
'''Confidence default.'''
SPEED = 250
'''Penguin movement speed, in pixels/sec (measured at 2560x1440).'''

class AutoClicker():
    '''
    AutoClicker class. Handles all moves.
    '''
    __size = 0
    __current = 0
    __debug = None
    __puffle = None
    __speed = 0
    __current_position = None
    __screen_size = None
    __screen_left = 0
    __screen_top = 0
    __screen_width = 0
    __screen_height = 0
    __width_range = 0
    __height_range = 0

    def __init__(self):
        self.__before_first_click = False
        self.__size = SIZE
        self.__current = 0
        self.__debug = False
        self.__screen_size = pg.size()
        self.__puffle = None
        self.__money_icon = None
        # 0 is for width and 1 is for height.
        self.__width = self.__screen_size[0]
        self.__height = self.__screen_size[1]
        # Sets default position to center of screen.
        self.__current_position = [self.__width/2, self.__height/4]
        # Coordinate math for area that the program will search to see if it is open to be clicked on. Also for determining penguin speed in pixels/second.
        self.__speed = SPEED * ((self.__width / 2560) ** 2)
        self.__screen_left = round(self.__screen_size[0]*.2617)
        self.__screen_top = round(self.__height*.5382)
        self.__screen_width = round(self.__width*.5371)
        self.__screen_height = round(self.__height*.3542)
        # Coordinates for calculating a random integer to be clicked on.
        self.__width_range = round(self.__width*.7988)
        self.__height_range =  round(self.__height*.8924)


    def __print_screen_size(self):
        '''Prints screen size. For debugging.'''
        print("Screen size: height=" + str(self.__height) + ", width=" + str(self.__width))
        print("Borders: left=" + str(self.__screen_left) + ", top=" + str(self.__screen_top) + ", width=" + str(self.__screen_width) + ", height=" + str(self.__screen_height))
        pg.screenshot("screen_borders.png", region=(self.__screen_left, self.__screen_top, self.__screen_width, self.__screen_height))

    def __get_pos(self):
        '''Gets current position. For debugging.'''
        return pg.position()

    def __mine(self, x, y, movement_time):
        '''Clicks penguin icon then mine (dance) icon.'''
        pg.click(x, y)
        self.__current_position = pg.position()
        time.sleep(movement_time)
        pg.press('d')

    def __move_click(self, current):
        '''Moves cursor to coordinates and then clicks. Set on a delay to maximize profits from mining.'''
        found = False
        while True:
            x = random.randint(self.__screen_left, self.__width_range)
            y = random.randint(self.__screen_top, self.__height_range)
            new_position = [x, y]
            for ground_color in GROUND_COLORS:
                if pg.pixelMatchesColor(new_position[0], new_position[1], (ground_color[0], ground_color[1], ground_color[2])):
                    found = True
                if found == True:
                    movement_time = self.__calc_distance(new_position)
                    break
            # Can change movement time to be whatever you want.
            if found == True and movement_time <= 2.5:
                break

        # Next position to mine is queued to maximize efficiency.
        if self.__before_first_click != False:
            time.sleep(DELAY_MOVEMENT)
            self.__before_first_click = True
        self.__mine(x, y, movement_time)

    def __run_puf(self):
        '''Clicks Puffle icon, then money bag.'''
        # Figures out which Puffle you have and sets that as the default for as long as the program runs.
        if self.__puffle == None:
            for image in os.listdir(FOLDER_PATH + "puffles/"):
                try:
                    if pg.locateOnScreen(FOLDER_PATH + "puffles/" + image, grayscale=self.__debug):
                        self.__puffle = FOLDER_PATH + "puffles/" + image
                        if self.__debug == True:
                            print("Puffle found: " + image)
                        break
                except:
                    continue
            if self.__puffle == None:
                self.__puffle = False
                if self.__debug == True:
                    print("No Puffle found.")
        # Finds Puffle on the screen and then clicks it.
        try:
            puffle_icon_location = pg.locateCenterOnScreen(self.__puffle, grayscale=GRAYSCALE)
            pg.click(puffle_icon_location)
            # Sets correct money bag icon.
            for image in os.listdir(FOLDER_PATH + "money_icons/"):
                try:
                    if pg.locateOnScreen(FOLDER_PATH + "money_icons/" + image, grayscale=self.__debug):
                        self.__money_icon = FOLDER_PATH + "money_icons/" + image
                        if self.__debug == True:
                            print("Money bag icon found: " + image)
                        break
                except:
                    continue
            # Finds money bag on the screen and clicks it, if it is ready.
            money_icon_location = pg.locateCenterOnScreen(self.__money_icon, grayscale=GRAYSCALE)
            if self.__debug == True:
                if money_icon_location == None:
                    print("Puffle money icon either not found or not yet ready to be collected.")
            pg.click(money_icon_location)
            time.sleep(DELAY_TIME)
        except:
            if self.__debug == True:
                print("No Puffle found. Continuing.")

    def auto_click(self, current):
        '''Recursively calls auto_click. Starts with getting Puffle money bag, then runs until current is equal to size, then resets current to 0 and loops.'''
        while True:
            if current == self.__size:
                current = 0
            if current == 0:
                if self.__debug == True and self.__puffle != False:
                    print("Running Puffle...")
                    if self.__get_pos() != None:
                        print("Current location: " + str(self.__get_pos()))
                    else:
                        print("Unable to find cursor location.")
                if self.__puffle != False:
                    self.__run_puf()
            if self.__debug == True:
                print("Running iteration " + str(current))
                if self.__get_pos() != None:
                    print("Current location: " + str(self.__get_pos()))
                else:
                    print("Unable to find cursor location.")
            self.__move_click(current)
            self.auto_click(current+1)

    def __calc_distance(self, new_position):
        '''Calculates pixels traveled.'''
        movement_time = math.hypot(self.__current_position[1] - new_position[1], self.__current_position[0] - new_position[0])
        if self.__debug == True:
            print("Speed=" + str(self.__speed))
            print("x1=" + str(self.__current_position[1]) + " x2=" + str(new_position[1]) + " y1=" + str(self.__current_position[0]) + " y2=" + str(new_position[0]))
            print("Pixels to travel=" + str(movement_time))
            print("Movement time=" + str(movement_time / self.__speed))
        return (movement_time  / self.__speed)

    def get_current(self):
        '''Returns current.'''
        return self.__current

    def set_debug(self, mode):
        '''Sets debug mode (default off).'''
        print("Debug mode on.")
        self.__debug = mode
        if mode == True:
            self.__print_screen_size()

def main():
    '''Creates and runs auto clicker.'''
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
