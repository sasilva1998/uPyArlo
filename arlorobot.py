from machine import UART
import time

DHB10_MAX_MOTOR_PWR = 127
DT_PREV_ENCODER_CHECK = 40
LAST_EXCG_STR_LEN = 96
EXCG_STR_LEN = 96
LAST_EXCG_TX_MIN = 16
DEFAULT_TOP_SPEED = 200

class ArloRobot(object):

	#set up/set down
	def __init__(self,tx=17,rx=16,baudrate=19200):
		self.tx=tx
		self.rx=rx
		self.baudrate=baudrate
		self.uart=UART(tx=self.tx, rx=self.rx, baudrate=self.baudrate)
		self.uart.init(self.baudrate, bits=8, parity=None, stop=1, txbuf=0)

		#speeds
		self.topSpeed=DEFAULT_TOP_SPEED
		self.paramVal=None
	def end(self):
		self.uart.deinit()

	# movements
	def writeCounts(self, left, right):
		self.paramVal.clear()
		self.paramVal=[left, right, self.topSpeed]
		self.com("MOVE",3,0)

	def writeSpeed(self, left, right):
		pass

	def writeMotorPower(self, left, right):
		pass

	# measurements
	def readCountsLeft(self):
		pass

	def readCountsRight(self):
		pass

	def readSpeedLeft(self):
		pass

	def readSpeedRight(self):
		pass

	# communication modes
	def writePulseMode(self):
		pass

	# information
	def readFirmwareVer(self):
		pass
	def readHardwareVer(self):
		pass

	def readSpeedLimit(self):
		pass

	# configuration
	def writeConfig(self, configString, value):
		pass

	def readConfig(self, configString):
		pass

	def writeSpeedLimit(self, countsPerSecond):
		pass

	def clearCounts(self):
		pass

	#nonvolatile configuration storage
	def storeConfig(self, configString):
		pass

	def restoreConfig(self):
		pass

	def checkCharacter(self):
		pass

	# com packet sending
	def com(self, command, paramCount, retCount):
		packet=command
		for i in self.paramVal:
			packet+=" "+str(i)
		self.uart.write(bytearray(packet))


def constrain(val, min_val, max_val):
    return min(max_val, max(min_val, val))






	