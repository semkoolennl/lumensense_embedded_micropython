import time

class DateTime:        
    def __init__(self,
                 year    = 0,
                 month   = 0,
                 day     = 0,
                 hours   = 0,
                 minutes = 0,
                 seconds = 0,
                ):
        self.year   = year
        self.month  = month
        self.day    = day
        self.hours   = hours
        self.minutes = minutes
        self.seconds = seconds
                    
        self.daysInMonth = [31,28,31,30,31,30,31,31,30,31,30,31]

    def addTimeInMs(self, timeInMs):
        self.seconds += timeInMs / 1000
        if self.seconds >= 60:
            self.seconds  = 0
            self.minutes += 1
        if self.minutes >= 60:
            self.minutes = 0
            self.hours  += 1
        if self.hours >= 24:
            self.hours = 0
            self.day += 1
        if self.day > self.getDaysInMonth():
            self.day    = 1
            self.month += 1
        if self.month > 12:
            self.month = 1
            self.year += 1
        
    def getDaysInMonth(self):
        if self.month == 2 and self.year % 4 == 0:
            return 29
        return self.daysInMonth[self.month-1]
    
    def __repr__(self):
        dateString = '/'.join(self.getDateArray())
        timeString = ':'.join(self.getTimeArray())

        return dateString + "-" + timeString

    def fromString(self, string):
        date, time = string.split("-")
        date = date.split('/')
        time = time.split(':')

        self.year    = date[0]
        self.month   = date[1]
        self.day     = date[2]
        self.hours   = time[0]
        self.minutes = time[1]
        self.seconds = time[2]

        return self

    def getDateArray(self):
        if self.month < 10:
            month = '0' + str(self.month)
        else:
            month = str(self.month)
        if self.day < 10:
            day = '0' + str(self.day)
        else:
            day = str(self.day)

        return [str(self.year), month, day]

    def getTimeArray(self):
        if self.seconds < 10:
            seconds = '0' + str(int(self.seconds))
        else:
            seconds = str(int(self.seconds))

        if self.minutes < 10:
            minutes = '0' + str(self.minutes)
        else:
            minutes = str(self.minutes)

        if self.hours < 10:
            hours = '0' + str(self.hours)
        else:
            hours = str(self.hours)

        return [hours, minutes, seconds]
        
    

class Clock:
    def __init__(self, datetime=DateTime()):
        self.lastTick = 0
        self.lastcount = time.ticks_ms()
        self.datetime = datetime
    
    def tick(self):
        if self.datetime.seconds >= 0:
            newcount = time.ticks_ms()
            self.lastTick = abs(time.ticks_diff(newcount, self.lastcount))
            self.datetime.addTimeInMs(self.lastTick)
            self.lastcount = newcount
            if (int(self.datetime.seconds / 1000)+1) % 120 == 0:
                self.datetime.seconds += 1.600

    
class Timer:
    def __init__(self, time = 0):
        self.time = time

    def update(self, tick):        
        if self.time > 0:
            self.time -= tick
        elif self.time < 0:
            self.time = 0

    def isRunning(self):
        return self.time > 0

    def __repr__(self):
        return self.time / 1000
        
