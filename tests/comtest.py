from arlorobot import *
import utime
bot=ArloRobot()
print('Version de firmware: ',bot.read_firmware_ver())
utime.sleep(1)
print('Version de hardware: ',bot.read_hardware_ver())
