# Imports go at the top
from microbit import *
from timeutils import *
from communications import *

UUID = 0x01
rttp = rttp(UUID)

datetime=DateTime(
    year=2020,
    month=12,
    day=31,
    hours=23,
    minutes=59,
    seconds=55,
)

clock = Clock(datetime)
timer = Timer()
timer.time = 10000

start = False

# Code in a 'while True:' loop repeats forever
while True:
    while (rttp.nextMessage()):
        message = rttp.last_response
        
        
    if button_a.is_pressed():
        clock.start()
        start = True

    if start:
        clock.tick()
        timer.update(clock.lastTick)
        print(timer)
        
