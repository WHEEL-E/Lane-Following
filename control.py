import serial

port = serial.Serial(
    port="/dev/ttyS0",
    baudrate=115200,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
)


def forward(speed=0.5):
    port.write(b'\w')


def left():
    port.write(b'\a')


def backward(speed=0.5):
    port.write(b'\s')


def right():
    port.write(b'\d')


def stop():
    port.write(b'\o')
