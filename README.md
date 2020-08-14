# uPyArlo
MicroPython library to control DBH-10 for Arlo Parallax platform.

In this repo you will find a script called `arlorobot.py`, which contains an object `ArloRobot()` with its corresponding methods in order to controll the driver DBH-10.

## Object initialization
The object is defined with the following parameters: `def __init__(self,serial_id=2,tx=17,rx=16,baudrate=19200)`, where `serialid` defines the ID of the UART bus that will be used. By default in uPy when `serialid` is defined, `tx` and `rx` are by default as well, however they can still be changed in case the pins are different in other boards.

Here is an example of how it should be:
```python
from arlorobot import *
robot=ArloRobot()
```

OR

```python
from arlorobot import *
robot=ArloRobot(serial_id=1, tx=12,rx=13,baudrate=115200)
```
**Note: In the second example, all parameters have been defined by random, it depends on the board, for example the baudrate by default is 19200.**

## Methods description

#### Movement Methods

| Method                            | What it does                                                 |
| --------------------------------- | ------------------------------------------------------------ |
| `turn(motor_movement, top_speed)` | Turns the robot in place, but instead of degrees, the `motor_movement` corresponds to the number of positions to move each wheel, constrained from -32767 to 32767, and `top_speed` to the speed which is constrained between 1 to 512. |
| `move(left, right, speed)`        | Accelerate, travel, and decelerate across a distance in positions, motors will complete the travel at the same time. `left` and `right` are the distance in position, constrained from -32767 to 32767. `speed` is the positions per second, which goes from 1 to 32767. |
| `go_speed(left, right)`           | Accelerate and sustain a speed, independently for each motor. `left`/`right` correspond to the positions per second, which goes from -32767 to 32767. |
| `go(left, right)`                 | Set and hold the motor output power, independently for each motor. `left`/`right` corresponds to the power of each motor, values go from -127 to 127. |
