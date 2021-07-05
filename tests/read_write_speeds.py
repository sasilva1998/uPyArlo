from arlorobot import *

robot = ArloRobot(serial_id=2, baudrate=19200, tx=17, rx=16, pace=2)

robot.go_speed(50, 50)
robot.clear_counts()
while True:
    robot.go_speed(0,0)
    data = robot.read_counts()
    print(data)
    #robot.go_speed(50,-50)