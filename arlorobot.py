# pins and serial library
from machine import UART
import utime

# object to control de DHB-10 driver
class ArloRobot(object):
	
		# com packet sending
	def com(self, packet):
		for i in packet:
			self.uart.write(i)
			self.uart.write(" ")
		self.uart.write("\r")
		tinit=utime.ticks_ms()
		resp=''
		while (utime.ticks_ms()-tinit)<150: #timeout of 1600us
			data=self.uart.read(1)
			if data is not None and data!=b'\r':
				resp=resp+str(data)[2:][:-1]

		if resp is not None:
			resp=resp.split("xd6")[-1].split("xc3")[-1].split(" ")

			try:
				resp=[int(i) for i in resp]
			except:
				return None

			if len(resp)!=2:
				return resp[0]
			return resp
		return resp

	# set up/set down
	# serialid is defined as the ID of the serial bus from the
	# microcontroller, however tx and rx can be defined
	def __init__(self,serialid=2,tx=17,rx=16,baudrate=19200):
		self.tx=tx
		self.rx=rx
		self.baudrate=baudrate
		self.uart=UART(serialid,self.baudrate)
		self.uart.init(self.baudrate, bits=8, parity=None, stop=1, txbuf=0,tx=self.tx, rx=self.rx)
		self.com(["TXPIN","CH2"])#needed so that reading is possible
		self.com(["DEC"])
		self.com(["ECHO","ON"])
		

	# end serial connection
	def end(self):
		self.uart.deinit()

#-------------------------- movements methods------------------------

	# Turn command
	# motor_movements corresponds to the amount of encode positions
	# top_speed to the positions per second
	def turn(self, motor_movement, top_speed):
		self.com(["TURN",str(motor_movement),str(top_speed)])

	# arc turns the motors so that the platform moves along the arc of a circle
	# of a given radius with a speed and an angle
	def arc(self, radius, top_speed, angle):
		self.com(["ARC",str(radius),str(top_speed),str(angle)])

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

	def travel(self,distance,top_speed,angle):
		self.com(["TRVL",str(distance),str(top_speed),str(angle)])



#--------------------------- information methods -----------------------
	
	def read_left_counts(self):
		return self.com(["DIST"])[0]

	def read_right_counts(self):
		return self.com(["DIST"])[1]

	def read_left_speed(self):
		return self.com(["SPD"])[0]

	def read_right_speed(self):
		return self.com(["SPD"])[1]

	def read_head_angle(self):
		return self.com(["HEAD"])[0]

	def read_firmware_ver(self):
		return self.com(["VER"])

	def read_hardware_ver(self):
		return self.com(["HWVER"])

	def clear_counts(self):
		return self.com(["RST"])


# ---------------------------- communication modes -----------------------

	def write_pulse_mode(self):
		self.com(["PULSE"])

	def set_lf_mode(self,status):
		return self.com(["SETLF",str(status)])

	def set_hex_com(self):
		return self.com(['HEX'])

	def set_dec_com(self):
		return self.com(['DEC'])

	def set_echo_mode(self,status):
		return self.com(["ECHO",str(status)])

	def set_verbose_mode(self,status):
		return self.com(["VERB",str(status)])

	def set_rx_pin(self,pin):
		return self.com(["RXPIN",str(pin)])

	def set_tx_pin(self,pin):
		return self.com(["TXPIN",str(pin)])

	def set_baud_rate(self,baud):
		return self.com(["BAUD",str(baud)])

	def set_pwm_scale(self,scale):
		return self.com(["SCALE",str(scale)])

	def set_pace(self,pace):
		return self.com(["PACE",str(pace)])

	def set_hold(self,hold):
		return self.com(["HOLD",str(baud)])

#-------------------------- closed loop constants ----------------------

	def set_ki_limit(self, limit):
		return self.com(["KIP",str(limit)])

	def set_ki_decay(self, decay):
		return self.com(["KIT",str(decay)])


def constrain(val, min_val, max_val):
    return min(max_val, max(min_val, val))


	
