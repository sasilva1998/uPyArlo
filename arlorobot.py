# pins and serial library
from machine import UART
import utime

# object to control de DHB-10 driver
class ArloRobot(object):

    # com packet sending
    def com(self, packet, ret):
        for i in packet:
            self.uart.write(i)
            self.uart.write(" ")
        self.uart.write("\r")
        tinit = utime.ticks_ms()
        resp = ""

        if ret:
            while (utime.ticks_ms() - tinit) < 150:  # timeout of 1600us
                data = self.uart.read(1)
                if data is not None and data != b"\r":
                    resp = resp + str(data)[2:][:-1]
                elif data == b"\r":
                    break

            if resp is not None:
                resp = resp.split("xd6")[-1].split("xc3")[-1].split(" ")

                try:
                    resp = [int(i) for i in resp]
                except:
                    return resp

                if len(resp) != 2:
                    return resp[0]
                return resp
            return resp
        else:
            pass

    # set up/set down
    # serialid is defined as the ID of the serial bus from the
    # microcontroller, however tx and rx can be defined
    def __init__(self, serial_id=2, baudrate=19200, **kwargs):
        self.baudrate = baudrate
        self.serial_id = serial_id

        if "serial" in kwargs:
            self.uart = kwargs.get("serial")
        elif "tx" in kwargs and "rx" in kwargs:
            self.uart = UART(self.serial_id, self.baudrate)
            self.uart.init(
                self.baudrate,
                tx=kwargs.get("tx"),
                rx=kwargs.get("rx"),
                bits=8,
                parity=None,
                stop=1,
                txbuf=0,
            )
        else:
            self.uart = UART(self.serial_id, self.baudrate)
            self.uart.init(self.baudrate, bits=8, parity=None, stop=1, txbuf=0)

        self.com(["TXPIN", "CH2"], False)  # needed so that reading is possible
        self.com(["DEC"], False)
        self.com(["ECHO", "ON"], False)

    # end serial connection
    def end(self):
        self.uart.deinit()

    # -------------------------- movements methods------------------------

    # Turn command
    # motor_movements corresponds to the amount of encode positions
    # top_speed to the positions per second
    def turn(self, motor_movement, top_speed, ret=False):
        self.com(["TURN", str(motor_movement), str(top_speed)], ret)

    # arc turns the motors so that the platform moves along the arc of a circle
    # of a given radius with a speed and an angle
    def arc(self, radius, top_speed, angle, ret=False):
        self.com(["ARC", str(radius), str(top_speed), str(angle)], ret)

    # left/right -> -32767 to 32767
    # speed -> 1 to 32767
    def move(self, left, right, speed, ret=False):
        self.com(["MOVE", str(left), str(right), str(speed)], ret)

    # left/right -> -32767 to 32767
    def go_speed(self, left, right, ret=False):
        self.com(["GOSPD", str(left), str(right)], ret)

    # left/right -> -127 to 127
    def go(self, left, right, ret=False):
        self.com(["GO", str(left), str(right)], ret)

    def travel(self, distance, top_speed, angle, ret=False):
        self.com(["TRVL", str(distance), str(top_speed), str(angle)], ret)

    # --------------------------- information methods -----------------------

    def read_counts(self, ret=True):
        return self.com(["DIST"], ret)

    def read_left_counts(self, ret=True):
        return self.com(["DIST"], ret)[0]

    def read_right_counts(self, ret=True):
        return self.com(["DIST"], ret)[1]

    def read_left_speed(self, ret=True):
        return self.com(["SPD"], ret)[0]

    def read_right_speed(self, ret=True):
        return self.com(["SPD"], ret)[1]

    def read_head_angle(self, ret=True):
        data = self.com(["HEAD"], ret)
        try:
            if len(data) == 2:
                return int((data[1]))
            else:
                return int(data[0])
        except:
            return data

    def read_firmware_ver(self, ret=True):
        return self.com(["VER"], ret)

    def read_hardware_ver(self, ret=True):
        return self.com(["HWVER"], ret)

    def clear_counts(self, ret=True):
        return self.com(["RST"], ret)

    # ---------------------------- communication modes -----------------------

    def write_pulse_mode(self, ret=False):
        return self.com(["PULSE"], ret)

    def set_lf_mode(self, status, ret=False):
        return self.com(["SETLF", str(status)], ret)

    def set_hex_com(self, ret=False):
        return self.com(["HEX"], ret)

    def set_dec_com(self, ret=False):
        return self.com(["DEC"], ret)

    def set_echo_mode(self, status, ret=False):
        return self.com(["ECHO", str(status)], ret)

    def set_verbose_mode(self, status, ret=False):
        return self.com(["VERB", str(status)], ret)

    def set_rx_pin(self, pin, ret=False):
        return self.com(["RXPIN", str(pin)], ret)

    def set_tx_pin(self, pin, ret=False):
        return self.com(["TXPIN", str(pin)], ret)

    def set_baud_rate(self, baud, ret=False):
        return self.com(["BAUD", str(baud)], ret)

    def set_pwm_scale(self, scale, ret=False):
        return self.com(["SCALE", str(scale)], ret)

    def set_pace(self, pace, ret=False):
        return self.com(["PACE", str(pace)], ret)

    def set_hold(self, hold, ret=False):
        return self.com(["HOLD", str(baud)], ret)

    # -------------------------- closed loop constants ----------------------

    def set_ki_limit(self, limit, ret=False):
        return self.com(["KIP", str(limit)], ret)

    def set_ki_decay(self, decay, ret=False):
        return self.com(["KIT", str(decay)], ret)

    def set_kimax(self, maxim, ret=False):
        return self.com(["KIMAX", str(maxim)], ret)

    def set_ki_constant(self, constant, ret=False):
        return self.com(["KI", str(constant)], ret)

    def set_kp_constant(self, constant, ret=False):
        return self.com(["KP", str(constant)], ret)

    def set_acc_rate(self, acc, ret=False):
        return self.com(["ACC", str(acc)], ret)

    def set_ramp_rate(self, rate, ret=False):
        return self.com(["RAMP", str(rate)], ret)

    def set_live_zone(self, limit, ret=False):
        return self.com(["LZ", str(limit)], ret)

    def set_dead_zone(self, limit, ret=False):
        return self.com(["DZ", str(limit)], ret)

    def set_ppr(self, ppr, ret=False):
        return self.com(["PPR", str(ppr)], ret)

    # -------- config ----------
    def restore_config(self, ret=False):
        return self.com(["RESTORE"], ret)


def constrain(val, min_val, max_val):
    return min(max_val, max(min_val, val))
