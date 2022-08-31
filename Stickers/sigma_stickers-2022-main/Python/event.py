import time


class Time(object):
    def __init__(self, time):
        # parse timeString into a time format. The incoming format is ["8:12 AM","12:30 PM"]
        self.noTime = False
        if time == "NA":
            self.noTime = True
            return
        timeStringSplit = time.replace(" ", ":").split(":")
        self.hour = int(timeStringSplit[0])
        self.min = int(timeStringSplit[1])
        self.ampm = str(timeStringSplit[2])

    # define how time will print
    def __str__(self):
        if self.noTime:
            return "NA"

        if self.hour == 0:
            hourprint = "00"
        else:
            hourprint = str(self.hour)

        minprint = str(self.min)

        if len(minprint) == 1:
            minprint = "0" + minprint

        return hourprint + ":" + minprint + " " + self.ampm

    def print_hour_and_minutes(self):
        if self.noTime:
            return "NA"

        if self.hour == 0:
            hourprint = "00"
        else:
            hourprint = str(self.hour)

        minprint = str(self.min)

        if len(minprint) == 1:
            minprint = "0" + minprint

        return hourprint + ":" + minprint

    # define less
    def __lt__(self, other):

        selfstring = str(self)
        otherstring = str(other)

        selfInt = (
            int(time.strftime("%H%M", time.strptime(selfstring, "%I:%M %p"))) - 300
        ) % 2400
        otherInt = (
            int(time.strftime("%H%M", time.strptime(otherstring, "%I:%M %p"))) - 300
        ) % 2400

        return selfInt < otherInt

    def __eq__(self, other):
        if self.noTime:
            return False
        if (
            self.ampm == other.ampm
            and self.hour == other.hour
            and self.min == other.min
        ):
            return True
        return False

    # define greater
    def __gt__(self, other):

        selfstring = str(self)
        otherstring = str(other)

        selfInt = (
            int(time.strftime("%H%M", time.strptime(selfstring, "%I:%M %p"))) - 300
        ) % 2400
        otherInt = (
            int(time.strftime("%H%M", time.strptime(otherstring, "%I:%M %p"))) - 300
        ) % 2400

        return selfInt > otherInt


class Event(object):
    def __init__(
        self, name, day, time, category
    ):  # time is a tuple of times - start, end
        if day not in [
            "Monday",
            "Tuesday",
            "Wednesday",
            "Thursday",
            "Friday",
            "Saturday",
            "Sunday",
        ]:
            raise Exception("Day of week not valid: " + day)
        self.name = name
        self.day = day
        if time != "NA":
            self.timeStart = Time(time[0])
            self.timeEnd = Time(time[1])
        else:
            self.timeStart = "NA"
            self.timeEnd = "NA"
        self.category = category

    def __lt__(self, other):
        return self.timeStart < other.timeStart

    def __eq__(self, other):
        return self.timeStart == other.timeStart

    def __gt__(self, other):
        return self.timeStart > other.timeStart


class Task:
    def __init__(self, name, category):
        self.name = name
        self.category = category
