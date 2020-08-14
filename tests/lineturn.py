from arlorobot import *
import utime

bot = ArloRobot()
utime.sleep(1)

while True:
    bot.turn(100, 20)
    utime.sleep(0.5)
    bot.move(200, 200, 20)
    utime.sleep(0.5)
    bot.turn(100, 20)
    utime.sleep(0.5)
