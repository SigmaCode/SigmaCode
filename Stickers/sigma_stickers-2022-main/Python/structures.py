from event import Event
from event import Time
class Person:
	def __init__(self, name, role):
		self.name = name
		self.role = role #counselor or faculty
		self.team = None
		self.events = []
		self.tasks = []
	def assign_team(self, team):
		self.team = team

	def add_event(self, event):
		self.events.append(event)

	def add_task(self, task):
		self.tasks.append(task)


class STBracket:
	def __init__(self, team1, team2, location, day, locabbr):
		if day not in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]:
			raise Exception("Day of week not valid: " + day)
		self.team1 = team1
		self.team2 = team2
		self.day = day
		self.location = location
		self.locabbr = locabbr

class Semilab:
	def __init__(self, nameFull, nameShort, timeOfDay, timeSlot):
		self.nameFull = nameFull
		self.nameShort = nameShort
		if timeOfDay not in ["morning", "afternoon"]:
			raise Exception("Semilab timeOfDay not valid: " + timeOfDay)
		self.timeOfDay = timeOfDay
		self.timeStart = Time(timeSlot[0])
		self.timeEnd = Time(timeSlot[1])
		self.TAs = []
		self.instructors = []

	def assign_TA(self, TA):
		self.TAs.append(TA)

	def assign_instructor(self, instructor):
		self.instructors.append(instructor)

class Team:
	def __init__(self, name):
		self.name = name
		self.counselors = []
		self.events = []
	def assign_counselor(self, counselor):
		self.counselors.append(counselor)

	def add_event(self, event):
		self.events.append(event)

class Camper:
	def __init__(self, namefirst, namelast, age, past_camps, team, semilab1, semilab2, building, nurse, epi):
		self.namefirst = namefirst
		self.namelast = namelast
		self.team = team
		self.age = age
		self.past_camps = past_camps
		self.semilab1 = semilab1
		self.semilab2 = semilab2
		self.building = building 
		self.nurse = nurse
		self.epi = epi

class uHaulItem:
	def __init__(self, person_name, item, quantity=1):
		self.person_name = person_name
		self.item = item

