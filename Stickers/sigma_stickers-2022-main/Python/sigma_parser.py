from sheetsExtractor import sheetsExtractor
from structures import Person
from structures import Team
from structures import Semilab
from structures import STBracket
from structures import Camper
from event import Event
from event import Task
from structures import uHaulItem


class SigmaParser:
    def __init__(self):
        # define class variables:
        self.staff = {}  # dictionary of class instances Person with all staff members
        self.teams = {}  # dictionary of class instances Team with all teams
        self.semilabs = []  # array of class instances Semilab with all semilabs
        self.STBrackets = (
            []
        )  # array of class STBRacket with all SigmaTournament Brackets
        self.camperInfo = []
        self.stickerPlacement = []

        self.itemResponsibilities = []  # array of uHaulItem class

        self.daysOfWeek = [
            "Sunday",
            "Monday",
            "Tuesday",
            "Wednesday",
            "Thursday",
            "Friday",
            "Saturday",
        ]

        # Initialize the Google Sheets API connection
        # spreadsheetId = '1RkRT2sKPjEm-ygLtpTKUeJpJARZnc-0yGUfVcv_Mwuk' #ID of the Master Organizer Spreadsheet (2017)
        # spreadsheetId = '1ktniuAEbGsM-04N0L9mdbc_0TE_ZYgsUYQr9-83MQrs'  # (2018)
        # spreadsheetId = '1jUP3e884T004P5sSURbgG6jQ4JOOpcxPtar5iZmsD6c'  # 2019
        spreadsheetId = "1fWZpreFlx_OUQuZaUG7OOXw0LM8QHkR1paDWh5N3DJc"  # 2022
        self.mySheetsExtractor = sheetsExtractor(spreadsheetId)

        self.extractNames()
        self.extractTeams()
        self.extractSemilabs()

        self.extractCounselorMeeting()
        self.extractTeamDuties()
        self.extractDiningHallDuties()
        self.extractCamperInfo()

        self.extractTournament()
        self.extractSpecialSchedule()
        self.extractDuties()
        self.extractUniversalReminders()
        self.extractNurse()
        # self.extractMiscResponsibilities()
        self.extractWorkshops()
        self.extractNightShift()
        self.extractRemindersByTeam()
        self.extractStickerPlacement()

        # self.extractStuffResponsibilities()

    def extractNames(self):
        ######################################################################
        # Sheet: Names
        ######################################################################
        # extract names into a list
        data = self.mySheetsExtractor.get_range("Staff!A2:A")
        counselorList = [str(x[0]) for x in data]
        data = self.mySheetsExtractor.get_range("Staff!B2:B")
        facultyList = [str(x[0]) for x in data]

        # create an instance of person class for each name and place in dictionary
        counselors = dict((name, Person(name, "counselor")) for name in counselorList)
        faculty = dict((name, Person(name, "faculty")) for name in facultyList)

        # combine the two dictionaries
        self.staff = counselors.copy()
        self.staff.update(faculty)
        counselors = None
        faculty = None

    def extractTeams(self):
        ######################################################################
        # Sheet: Teams
        ######################################################################
        rangeName = "Teams!A2:N"
        data = self.mySheetsExtractor.get_range(rangeName)
        data = zip(*data)  # transpose the 2D list

        # assign counselors to teams as per spreadsheet
        for team in data:
            team_name = team[0]
            for i in range(1, len(team)):
                if team[i] != "":
                    self.staff[team[i]].assign_team(str(team_name))

        # create instances of team class and put into dictionary like with staff

        teamList = [str(team[0]) for team in data]
        self.teams = dict((team, Team(team)) for team in teamList)
        for teamName in self.teams:
            for staffName in self.staff:
                if teamName == self.staff[staffName].team:
                    self.teams[teamName].assign_counselor(staffName)

    def extractDiningHallDuties(self):
        ######################################################################
        # Sheet: Team Duties (Dining Hall)
        ######################################################################

        # Extract times
        rangeName = "Team Duties!B11:C13"
        data = self.mySheetsExtractor.get_range(rangeName)
        timeBreakfast = [data[0][0], data[0][1]]
        timeLunch = [data[1][0], data[1][1]]
        timeDinner = [data[2][0], data[2][1]]

        rangeName = "Team Duties!B15"
        data = self.mySheetsExtractor.get_range(rangeName)
        eventName = data[0][0]
        # Extract Teams
        rangeName = "Team Duties!A2:E8"
        data = self.mySheetsExtractor.get_range(rangeName)
        for row in range(1, len(data)):
            for column in range(1, len(data[row])):
                day = data[row][0]
                meal = data[0][column]
                team = data[row][column]
                mealtime = None
                if meal == "Breakfast":
                    mealtime = timeBreakfast
                elif meal == "Lunch":
                    mealtime = timeLunch
                elif meal == "Dinner":
                    mealtime = timeDinner
                else:
                    raise Exception("mealtime not valid")

                if team != "":
                    self.teams[team].add_event(
                        Event(
                            "Team $\\" + team + "$ on " + meal + " duty",
                            day,
                            mealtime,
                            "teamdininghall",
                        )
                    )

    def extractTeamDuties(self):
        ######################################################################
        # Sheet: Team Duties (Cleanup)
        ######################################################################

        # Extract times
        rangeName = "Team Duties!G11:H11"
        data = self.mySheetsExtractor.get_range(rangeName)
        timeCleanup = [data[0][0], data[0][1]]
        # Extract Teams
        rangeName = "Team Duties!F2:J8"
        data = self.mySheetsExtractor.get_range(rangeName)
        for row in range(1, len(data)):
            for column in range(1, len(data[row])):
                day = data[row][0]
                location = data[0][column]
                team = data[row][column]

                if team != "":
                    self.teams[team].add_event(
                        Event(
                            "Team $\\" + team + "$ cleanup in " + location,
                            day,
                            timeCleanup,
                            "teamcleanup",
                        )
                    )

    def extractSemilabs(self):
        ######################################################################
        # Sheet: Semilabs
        ######################################################################

        # Extract times
        rangeName = "Semilabs!J4:K5"
        data = self.mySheetsExtractor.get_range(rangeName)
        timeMorning = [data[0][0], data[0][1]]
        timeAfternoon = [data[1][0], data[1][1]]
        timeofday = None
        # Extract Semilabs
        rangeName = "Semilabs!A3:H"
        data = self.mySheetsExtractor.get_range(rangeName)
        for row in data:
            semilabShortName = row[0].replace("_", "-")
            semilabName = row[1]
            timeSlot = None
            timeofday = row[2]
            if timeofday == "morning":
                timeSlot = timeMorning
            elif timeofday == "afternoon":
                timeSlot = timeAfternoon
            else:
                print(timeSlot)
                raise Exception("Semilab timeslot not valid.")

            self.semilabs.append(
                Semilab(semilabName, semilabShortName, timeofday, timeSlot)
            )

            instructors = []
            teachingAssistants = []
            for i in range(3, len(row)):
                if row[i] != "":
                    if i < 6:
                        self.semilabs[-1].assign_TA(row[i])
                        instructors.append(row[i])
                    else:
                        self.semilabs[-1].assign_instructor(row[i])
                        teachingAssistants.append(row[i])

            # only add semilab into the faculty stickers (counselors have too much in their stickers)
            for name in instructors:
                if self.staff[name].role == "faculty":
                    for day in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]:
                        self.staff[name].add_event(
                            Event(
                                "Instructor for " + semilabShortName,
                                day,
                                timeSlot,
                                "semilab",
                            )
                        )
                self.staff[name].add_task(
                    Task(
                        "Instructor for " + semilabShortName + " in the " + timeofday,
                        "semilab",
                    )
                )

            for name in teachingAssistants:
                if self.staff[name].role == "faculty":
                    for day in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]:
                        self.staff[name].add_event(
                            Event(
                                "TA for " + semilabShortName, day, timeSlot, "semilab"
                            )
                        )
                self.staff[name].add_task(
                    Task(
                        "TA for " + semilabShortName + " in the " + timeofday, "semilab"
                    )
                )

    def extractTournament(self):
        ######################################################################
        # Sheet: Tournament
        ######################################################################
        # extract tournament and meeting times:
        rangeName = "Tournament!I14:J15"
        data = self.mySheetsExtractor.get_range(rangeName)
        timeMeeting = [data[0][0], data[0][1]]
        timeTournament = [data[1][0], data[1][1]]

        # Extract abbreviations for locations
        ##rangeName = 'Tournament!H36:I46'
        rangeName = "Tournament!N13:O19"
        data = self.mySheetsExtractor.get_range(rangeName)
        locationabbreviations = {}
        for pair in data:
            locationabbreviations[pair[0]] = pair[1]

        # Extract judges for regular days
        rangeName = "Tournament!A2:F"
        data = self.mySheetsExtractor.get_range(rangeName)
        headerDays = data[0]
        for row in range(1, len(data)):
            for col in range(1, len(headerDays)):
                if data[row] != [] and data[row][col] != "":
                    name = data[row][col]
                    location = data[row][0]
                    day = headerDays[col]
                    position = data[row][-1]

                    self.staff[name].add_event(
                        Event(
                            "Tournament " + position + " at " + location,
                            day,
                            timeTournament,
                            "tournament",
                        )
                    )

                    if position == "Head Judge":
                        self.staff[name].add_event(
                            Event(
                                "Judges Meeting (head judge must attend)",
                                day,
                                timeMeeting,
                                "tournament",
                            )
                        )

                    else:
                        self.staff[name].add_event(
                            Event(
                                "Judges Meeting (optional)",
                                day,
                                timeMeeting,
                                "tournament",
                            )
                        )

        # Extract teams for regular days
        rangeName = "Tournament!G2:O9"
        data = self.mySheetsExtractor.get_range(rangeName)
        for row in range(1, len(data)):
            for i in range((len(data[row]) - 1) / 2):
                col1 = 2 * i + 1
                col2 = 2 * i + 2
                if data[row][col1] != "" and data[row][col2] != "":
                    day = data[0][col1]
                    location = data[row][0]
                    team1 = data[row][col1]
                    team2 = data[row][col2]
                    self.STBrackets.append(
                        STBracket(
                            team1, team2, location, day, locationabbreviations[location]
                        )
                    )

        # Extract Grand Unification Meeting Time and Location
        rangeName = "Tournament!I19:L20"
        data = self.mySheetsExtractor.get_range(rangeName)
        timeMeetingGrandUni = [data[0][0], data[0][1]]
        timeTournamentGrandUni = [data[1][0], data[1][1]]
        locationGradUni = data[1][3]
        dayGrandUnification = data[1][2]

        locationMeetingGrandUni = data[0][3]
        dayMeetingGrandUni = data[0][2]

        # timers
        rangeName = "Tournament!H23:I36"
        data = self.mySheetsExtractor.get_range(rangeName)
        for row in data:
            if len(row) == 2:
                if row[0] in self.teams and row[1] != "":
                    self.staff[row[1]].add_event(
                        Event(
                            "Timer at GU with $\\" + row[0] + "$ at " + locationGradUni,
                            dayGrandUnification,
                            timeTournamentGrandUni,
                            "tournament",
                        )
                    )
                    self.staff[row[1]].add_event(
                        Event(
                            "GU Meeting at " + locationMeetingGrandUni,
                            dayMeetingGrandUni,
                            timeMeetingGrandUni,
                            "tournament",
                        )
                    )

        # Runners
        rangeName = "Tournament!K23:K36"
        data = self.mySheetsExtractor.get_range(rangeName)
        for row in data:
            if row != []:
                self.staff[row[0]].add_event(
                    Event(
                        "Runner at GU at" + locationGradUni,
                        dayGrandUnification,
                        timeTournamentGrandUni,
                        "tournament",
                    )
                )
                # self.staff[row[0]].add_event(Event("GU Meeting at " + locationMeetingGrandUni, dayMeetingGrandUni, timeMeetingGrandUni, "tournament"))

        # Graders
        rangeName = "Tournament!L23:L36"
        data = self.mySheetsExtractor.get_range(rangeName)
        for row in data:
            if row != []:
                self.staff[row[0]].add_event(
                    Event(
                        "Grader at GU at " + locationGradUni,
                        dayGrandUnification,
                        timeTournamentGrandUni,
                        "tournament",
                    )
                )
                self.staff[row[0]].add_event(
                    Event(
                        "GU Meeting at " + locationMeetingGrandUni,
                        dayMeetingGrandUni,
                        timeMeetingGrandUni,
                        "tournament",
                    )
                )

    def extractWorkshops(self):
        ######################################################################
        # Sheet: Workshops
        ######################################################################
        # Extract time
        rangeName = "Workshops!B1:C1"
        data = self.mySheetsExtractor.get_range(rangeName)
        time = [data[0][0], data[0][1]]

        # Extract list workshop-staff name pairs
        rangeName = "Workshops!A4:C"
        data = self.mySheetsExtractor.get_range(rangeName)
        workshops = {}  # key is workshop name, value is staff name
        for row in data:

            instructor1 = None
            instructor2 = None

            if len(row) > 1:
                instructor1 = row[1]
                try:
                    instructor2 = row[2]
                except:
                    instructor2 = None

                workshops[row[0]] = [instructor1, instructor2]

                if instructor1 in self.staff:
                    self.staff[instructor1].add_task(
                        Task("Workshop " + row[0], "workshop")
                    )
                if instructor2 in self.staff:
                    self.staff[instructor2].add_task(
                        Task("Workshop " + row[0], "workshop")
                    )

        rangeName = "Workshops!F3:O120"
        data = self.mySheetsExtractor.get_range(rangeName)

        for colId in [0, 2, 4, 6, 8]:
            day = data[0][colId]
            for rowId in range(1, len(data)):
                if len(data[rowId]) > colId:
                    try:
                        location = data[rowId][colId + 1]
                    except:
                        location = "(location not assigned)"
                    workshopName = data[rowId][colId]

                    if not workshopName in workshops:
                        print(workshopName + " not in list of workshops")
                    else:
                        [instructor1, instructor2] = workshops[workshopName]

                        if instructor1 in self.staff:

                            self.staff[instructor1].add_event(
                                Event(
                                    "Workshop: "
                                    + workshopName
                                    + ", location: "
                                    + location,
                                    day,
                                    time,
                                    "workshop",
                                )
                            )

                            dayIndex = self.daysOfWeek.index(day)
                            if (dayIndex - 1) >= 0:
                                self.staff[instructor1].add_event(
                                    Event(
                                        "Workshop tomorrow:  " + workshopName,
                                        self.daysOfWeek[dayIndex - 1],
                                        "NA",
                                        "personalreminder",
                                    )
                                )

                        else:
                            print(
                                instructor1 + ", workshop instructor, not in staff list"
                            )
                        if instructor2 is not None:
                            if instructor2 in self.staff:

                                self.staff[instructor2].add_event(
                                    Event(
                                        workshopName + " workshop at " + location,
                                        day,
                                        time,
                                        "workshop",
                                    )
                                )

                                if (dayIndex - 1) >= 0:
                                    self.staff[instructor2].add_event(
                                        Event(
                                            "Workshop tomorrow:  " + workshopName,
                                            self.daysOfWeek[dayIndex - 1],
                                            "NA",
                                            "personalreminder",
                                        )
                                    )

                            else:
                                print(
                                    instructor2
                                    + ", workshop instructor, not in staff list"
                                )
        """
        #Extract table of workshops workshop-staff name pairs
        rangeName = 'Workshops!D3:I'
        data = self.mySheetsExtractor.get_range(rangeName)

        for rowi in range(1, len(data)):
            for colj in range(1, len(data[rowi])):
                if data[rowi][colj] != "":
                    location = data[rowi][0]
                    day = data[0][colj]
                    workshopName = data[rowi][colj]
                    staffName = workshops[workshopName]
                    self.staff[staffName].add_event(Event(workshopName + " workshop at " + location, day, time, "workshop"))

        #extract JIC duty
        rangeName = 'Workshops!L3:Q'
        data = self.mySheetsExtractor.get_range(rangeName)
        for rowi in range(1,len(data)):
            for colj in range(4,len(data[rowi])):
                staffname = data[rowi][colj]
                if staffname != "":
                    campername = data[rowi][0]
                    workshoptitle = data[rowi][1]
                    day = data[rowi][2]
                    location = data[rowi][3]
                    self.staff[staffname].add_event(Event("Attend JIC workshop \"" + workshoptitle + "\" by " + campername + " at " + location, day, time,"JIC"))
        """

    def extractMiscResponsibilities(self):
        ######################################################################
        # Sheet: Misc. Responsibilities
        ######################################################################
        # Extract list
        rangeName = "Misc. Responsibilities!B3:E"
        data = self.mySheetsExtractor.get_range(rangeName)
        for rowi in range(len(data)):
            for colj in range(1, len(data[rowi])):
                if data[rowi][colj] != "":
                    task = data[rowi][0]
                    if task == "":
                        raise Exception("Task empty in row " + rowi)
                    name = data[rowi][colj]
                    self.staff[name].add_task(Task(task, "misc"))

    def extractNightShift(self):
        ######################################################################
        # Sheet: Night Shift
        ######################################################################

        # Extract times
        rangeName = "Night Shift!B12:C13"
        data = self.mySheetsExtractor.get_range(rangeName)
        shift1time = [data[0][0], data[0][1]]
        shift2time = [data[1][0], data[1][1]]

        # Extract shifts table
        rangeName = "Night Shift!A2:I10"
        data = self.mySheetsExtractor.get_range(rangeName)

        for rowi in range(2, len(data)):
            for colj in range(1, len(data[rowi])):
                day = data[rowi][0]
                location = data[0][colj]
                shift = data[1][colj]
                name = data[rowi][colj]

                # who has the next/prev shift in that location
                other_name = "noname"
                other_shift = None
                if shift == "1st shift":
                    if len(data[rowi]) <= colj + 1:
                        other_name = "no one"
                    else:
                        other_name = data[rowi][colj + 1]
                    other_shift = "2nd"
                elif shift == "2nd shift":
                    other_name = data[rowi][colj - 1]
                    other_shift = "1st"

                time = None
                if shift == "1st shift":
                    time = shift1time
                elif shift == "2nd shift":
                    time = shift2time
                else:
                    raise Exception("Shift not valid")

                if name != "":
                    self.staff[name].add_event(
                        Event(
                            "Night Shift: "
                            + shift
                            + " at "
                            + location
                            + " ("
                            + other_name
                            + " on "
                            + other_shift
                            + ")",
                            day,
                            time,
                            "nightshift",
                        )
                    )

    def extractCounselorMeeting(self):
        rangeName = "Counselor Meeting!D2:E2"
        data = self.mySheetsExtractor.get_range(rangeName)
        time = [data[0][0], data[0][1]]

        rangeName = "Counselor Meeting!A3:O"
        data = self.mySheetsExtractor.get_range(rangeName)

        for rowi in range(1, len(data)):
            day = data[rowi][0]
            for colj in range(len(data[rowi])):
                team = data[0][colj]
                nameOnDuty = data[rowi][colj]

                for name in self.staff:
                    if self.staff[name].role == "counselor":
                        if self.staff[name].team == team:
                            self.staff[name].add_event(
                                Event(
                                    nameOnDuty + " stop by counselor office hours",
                                    day,
                                    time,
                                    "counselor office hours",
                                )
                            )

    def extractNurse(self):
        ######################################################################
        # Sheet: Burse
        ######################################################################

        # Extract nurse times
        rangeName = "Nurse!F3:H10"
        data = self.mySheetsExtractor.get_range(rangeName)

        nursetimes = {}
        for row in data:
            if len(row) != 3:
                raise Exception("Nurse time table partially empty")
            elif row[0] == "" or row[1] == "":
                raise Exception("Nurse time table partially empty")

            nursetimes[row[0]] = [row[1], row[2]]

        # Extract list of campers
        rangeName = "Nurse!A3:D"
        data = self.mySheetsExtractor.get_range(rangeName)

        for row in data:
            if len(row) != 4:
                raise Exception("Nurse camper list partially empty")
            elif row[0] == "" or row[1] == "" or row[2] == "":
                raise Exception("Nurse camper list partially empty")

            camperName = row[0]
            team = row[1]
            timeOfDay = row[2]
            counselorName = row[3]
            # get all counselors for the camper
            counselors = self.teams[team].counselors

            for counselor in counselors:
                for day in [
                    "Monday",
                    "Tuesday",
                    "Wednesday",
                    "Thursday",
                    "Friday",
                    "Saturday",
                    "Sunday",
                ]:
                    if counselor == counselorName:
                        self.staff[counselor].add_event(
                            Event(
                                "Take " + camperName + " to nurse",
                                day,
                                nursetimes[timeOfDay],
                                "nurse",
                            )
                        )
                    else:
                        self.staff[counselor].add_event(
                            Event(
                                counselorName + " takes " + camperName + " to nurse",
                                day,
                                nursetimes[timeOfDay],
                                "nurse",
                            )
                        )

    def extractRemindersByTeam(self):
        ######################################################################
        # Sheet: Reminders by Team
        ######################################################################

        # Extract Reminders
        rangeName = "Team Specific Reminders!A3:H"
        data = self.mySheetsExtractor.get_range(rangeName)

        for rowi in range(1, len(data)):
            for colj in range(1, len(data[rowi])):
                reminder = data[rowi][colj]
                if reminder != "":
                    day = data[0][colj]
                    team = data[rowi][0]
                    self.teams[team].add_event(
                        Event(reminder, day, "NA", "teamreminder")
                    )

    def extractUniversalReminders(self):
        ######################################################################
        # Sheet: Reminders by Team
        ######################################################################

        # Extract Reminders
        rangeName = "All-Team Reminders!A3:H"
        data = self.mySheetsExtractor.get_range(rangeName)

        for rowi in range(1, len(data)):
            for colj in range(1, len(data[rowi])):
                reminder = data[rowi][colj]
                if reminder != "":
                    day = data[0][colj]
                    category = data[rowi][0]
                    for name in self.staff:
                        if self.staff[name].role == "counselor":
                            self.staff[name].add_event(
                                Event(reminder, day, "NA", category + "reminder")
                            )

    def extractDuties(self):
        ######################################################################
        # Sheet: Duty
        ######################################################################

        # Extract Reminders
        rangeName = "Duty!A2:K18"
        data = self.mySheetsExtractor.get_range(rangeName)

        for rowi in range(1, len(data)):
            for colj in range(4, len(data[rowi])):
                name = data[rowi][colj]
                if name != "":
                    day = data[0][colj]
                    duty = data[rowi][0]
                    time = [data[rowi][1], data[rowi][2]]
                    location = data[rowi][3]
                    if location == "":
                        self.staff[name].add_event(Event(duty, day, time, "duty"))
                    elif location != "":
                        self.staff[name].add_event(
                            Event(duty + " at " + location, day, time, "duty")
                        )

    def extractSpecialSchedule(self):
        ######################################################################
        # Sheet: Special Schedule
        ######################################################################

        # Extract Table
        rangeName = "Special Schedule!A3:D"
        data = self.mySheetsExtractor.get_range(rangeName)
        for row in data:
            if len(row) == 0:
                break
            if len(row) != 4:
                raise Exception("Incomplete Schedule Entry")
            if row[0] == "" or row[1] == "" or row[2] == "" or row[3] == "":
                raise Exception("Incomplete Schedule Entry")

            day = row[0]
            time = [row[1], row[2]]
            event = row[3]
            for name in self.staff:
                self.staff[name].add_event(Event(event, day, time, "specialschedule"))

    def extractCamperInfo(self):
        ######################################################################
        # Sheet: Special Schedule
        ######################################################################
        rangeName = "Camper Info!A2:K"
        data = self.mySheetsExtractor.get_range(rangeName)
        for row in data:
            namefirst = row[1]
            namelast = row[0]
            age = row[2]

            past_campsText = row[4]
            if past_campsText == "2022":
                past_camps = False
            else:
                past_camps = True

            team = row[5].lower()
            building = row[6]

            nurseText = row[7]
            assert nurseText in ["yes", "no"], "epi must be yes or no"
            if nurseText == "yes":
                nurse = True
            else:
                nurse = False

            epiText = row[8]
            assert epiText in ["yes", "no"], "epi must be yes or no"
            if epiText == "yes":
                epi = True
            else:
                epi = False

            semilab1 = row[9]
            semilab2 = row[10]
            self.camperInfo.append(
                Camper(
                    namefirst,
                    namelast,
                    age,
                    past_camps,
                    team,
                    semilab1,
                    semilab2,
                    building,
                    nurse,
                    epi,
                )
            )

    def extractStickerPlacement(self):
        rangeName = "Sticker Pages!B1:E14"
        self.stickerPlacement = self.mySheetsExtractor.get_range(rangeName)

    def extractStuffResponsibilities(self):
        rangeName = "Stuff responsibilities!A2:E"
        data = self.mySheetsExtractor.get_range(rangeName)
        for row in data:
            if len(row) >= 4:
                for i in range(3):
                    if row[i] != "":
                        self.itemResponsibilities.append(uHaulItem(row[i], row[3]))
