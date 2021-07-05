from time import sleep, sleep_ms
from machine import UART
import utime

ser = UART(2, 19200)
ser.init(19200, bits=8, parity=None, stop=1, tx=17, rx=16, txbuf=0)
ser.write(b"TXPIN CH2\r")
sleep(1)
#ser.write(b"RXPIN CH1\r")
#sleep(1)
ser.write(b"BAUD 19200\r")
sleep(1)
ser.write(b"PACE 2\r")
sleep(1)
ser.write(b"DEC\r")
sleep(1)
ser.write(b"ECHO OFF\r")
sleep(1)
ser.write(b"VERB ON\r")
sleep(1)
ser = UART(2, 19200)
ser.init(19200, bits=8, parity=None, stop=1, tx=17, rx=16, txbuf=0)
sleep(1)
ser.write(b"RST\r")
sleep(1)
ser.write(bytes("GOSPD 50 -50\r", "utf-8"))
sleep(1)
val = 2
while True:
    #ser.write(bytes("GOSPD 50 -50\r", "utf-8"))
    #sleep_ms(val)
    ser.write(b"D")
    sleep_ms(val)
    ser.write(b"I")
    sleep_ms(val)
    ser.write(b"S")
    sleep_ms(val)
    ser.write(b"T")
    sleep_ms(val)
    ser.write(b"\r")
    sleep_ms(val)
    resp ="" 
    data = ""
    while data != b"\r" and data is not None:
        data = ser.read(1)
        sleep_ms(val)
        #print(data)
        resp = resp+str(data)[2:][:-1]
    print(resp[:-2])