from machine import UART
import utime

DHB10_MAX_MOTOR_PWR = 127
DT_PREV_ENCODER_CHECK = 40
LAST_EXCG_STR_LEN = 96
EXCG_STR_LEN = 96
LAST_EXCG_TX_MIN = 16
DEFAULT_TOP_SPEED = 200

class ArloRobot(object):

	#set up/set down
	def __init__(self,serialid=2,tx=17,rx=16,baudrate=19200):
		self.tx=tx
		self.rx=rx
		self.baudrate=baudrate
		self.uart=UART(serialid,self.baudrate)
		self.uart.init(self.baudrate, bits=8, parity=None, stop=1, txbuf=0,tx=self.tx, rx=self.rx)
		self.uart.write("TXPIN CH2\r")
		#speeds
		self.topSpeed=DEFAULT_TOP_SPEED
		self.paramVal=[]

	def end(self):
		self.uart.deinit()

#-------------------------- movements methods------------------------

	# Turn command

	def turn(self, motor_movement, top_speed):
		self.paramVal.clear()
		self.paramVal=[motor_movement, top_speed]
		self.com("TURN")

	# left/right -> -32767 to 32767
	# speed -> 1 to 32767
	def move(self, left, right, speed):
		self.paramVal.clear()
		self.paramVal=[left, right, speed]
		self.com("MOVE")

	# left/right -> -32767 to 32767
	def go_speed(self, left, right):
		self.paramVal.clear()
		self.paramVal=[left,right]
		self.com("GOSPD")

	# left/right -> -127 to 127
	def go(self, left, right):
		self.paramVal=[left, right]
		self.com("GO")


	# measurements
	def readCountsLeft(self):
		return self.com("DIST")[0]

	def readCountsRight(self):
		return self.com("DIST")[1]

	def readSpeedLeft(self):
		return self.com("SPD")[0]

	def readSpeedRight(self):
		return self.com("SPD")[1]

	# communication modes
	def writePulseMode(self):
		self.com("PULSE")

	# information
	def readFirmwareVer(self):
		return self.com("VER")

	def readHardwareVer(self):
		return self.com("HWER")

	def readSpeedLimit(self):
		return self.topSpeed

	# configuration
	def writeConfig(self, configString, value):
		self.paramVal.clear()
		self.paramVal=[value]
		self.com(configString,1,0)

	def readConfig(self, configString):
		pass

	def writeSpeedLimit(self, countsPerSecond):
		self.topSpeed=countsPerSecond

	def clearCounts(self):
		self.com("RST", 0, 0)

	#nonvolatile configuration storage
	def storeConfig(self, configString):
		pass

	def restoreConfig(self):
		self.com("RESTORE", 0, 0)

	def checkCharacter(self):
		pass

	# com packet sending
	def com(self, command):
		packet=command
		for i in self.paramVal:
			packet+=" "+str(i)
		packet+="\r"
		print(packet)
		self.uart.write(packet)
		tinit=utime.ticks_us()
		while (utime.ticks_us()-tinit)<5000000: #timeout of 1600us
			resp=self.uart.read(5)
			if resp is not None:
				return resp
		return None


def constrain(val, min_val, max_val):
    return min(max_val, max(min_val, val))


	