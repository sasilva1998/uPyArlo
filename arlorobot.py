# pins and serial library
from machine import UART
import utime

# some constants
DHB10_MAX_MOTOR_PWR = 127
DT_PREV_ENCODER_CHECK = 40
LAST_EXCG_STR_LEN = 96
EXCG_STR_LEN = 96
LAST_EXCG_TX_MIN = 16
DEFAULT_TOP_SPEED = 200

# object to control de DHB-10 driver
class ArloRobot(object):
	
		# com packet sending
	def com(self, packet):
		for i in packet:
			print(i)
			self.uart.write(i)
			self.uart.write(" ")
		self.uart.write("\r")
		tinit=utime.ticks_ms()
		resp=[]
		while (utime.ticks_ms()-tinit)<1000: #timeout of 1600us
			data=self.uart.read(1)
			if data is not None:
				resp.append(data)
		return resp

	def com2(self, packet):
		for i in packet:
			print(i)
			self.uart.write(i)
			self.uart.write(" ")
		self.uart.write("\r")
		tinit=utime.ticks_ms()
		resp=[]
		while (utime.ticks_ms()-tinit)<1000: #timeout of 1600us
			data=self.uart.read(20)
			if data is not None:
				return data
		return None

	# set up/set down
	# serialid is defined as the ID of the serial bus from the
	# microcontroller, however tx and rx can be defined
	def __init__(self,serialid=2,tx=17,rx=16,baudrate=19200):
		self.tx=tx
		self.rx=rx
		self.baudrate=baudrate
		self.uart=UART(serialid,self.baudrate)
		self.uart.init(self.baudrate, bits=8, parity=None, stop=1, txbuf=0,tx=self.tx, rx=self.rx)
		self.com(["txpin","ch2"])#needed so that reading is possible
		

	# end serial connection
	def end(self):
		self.uart.deinit()

#-------------------------- movements methods------------------------

	# Turn command
	# Use not recommended unless firmware is updated
	def turn(self, motor_movement, top_speed):
		self.com(["TURN",str(motor_movement),str(top_speed)])

	# left/right -> -32767 to 32767
	# speed -> 1 to 32767
	def move(self, left, right, speed):
		self.com(["MOVE",str(left),str(right),str(speed)])

	# left/right -> -32767 to 32767
	def go_speed(self, left, right):
		self.com(["GOSPD",str(left),str(right)])

	# left/right -> -127 to 127
	def go(self, left, right):
		self.com(["GO",str(left),str(right)])


	# measurements
	def read_counts_left(self):
		return self.com(["DIST"])

	def read_counts_right(self):
		return self.com(["DIST"])

	def read_speed_left(self):
		return self.com(["SPD"])

	def read_speed_right(self):
		return self.com(["SPD"])

	# communication modes
	def write_pulse_mode(self):
		self.com(["PULSE"])

	# information
	def read_firmware_ver(self):
		return self.com(["VER"])

	def read_hardware_ver(self):
		return self.com(["HWVER"])

	def read_speedLimit(self):
		return self.topSpeed

	#communication
	def set_hex_com(self):
		return self.com(['HEX'])

	def set_dec_com(self):
		return self.com(['DEC'])

	# configuration
	def write_config(self, configString, value):
		pass

	def read_config(self, configString):
		pass

	def write_speed_limit(self, countsPerSecond):
		self.topSpeed=countsPerSecond

	def clear_counts(self):
		self.com(["RST"])

	#nonvolatile configuration storage
	def store_config(self, configString):
		pass

	def restore_config(self):
		self.com(["RESTORE"])

	def check_character(self):
		pass



def constrain(val, min_val, max_val):
    return min(max_val, max(min_val, val))


	
