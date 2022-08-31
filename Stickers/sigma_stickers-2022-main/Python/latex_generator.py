import os
import sys
import copy


file_dir = os.path.dirname(__file__)
sys.path.append(file_dir)

# from parser import SigmaParser
import sigma_parser

if not os.path.exists("../LaTeX/python_output"):
    os.makedirs("../LaTeX/python_output")


class cfile(file):
    # subclass file to have a more convienient use of writeline
    def __init__(self, name, mode="r"):
        self = file.__init__(self, name, mode)

    def wl(self, string):
        self.writelines(string + "\n")
        return None

    def w(self, string):
        self.writelines(string)
        return None


# Create Tournament Table


def createtournamenttable(outfile, brackets):
    if len(brackets) != 7:
        if len(brackets) == 0:
            return
        else:
            raise Exception(
                "Tournament table must have length 7. Length is " + str(len(brackets))
            )
    outfile.wl(r"\begin{tournamenttable}")

    for i in range(len(brackets)):
        outfile.w("\\large $\\" + brackets[i].team1 + "\\" + brackets[i].team2 + r"$")
        if i != len(brackets) - 1:
            outfile.w(r"&")
        else:
            outfile.wl("\\\\")
    for i in range(len(brackets)):
        outfile.w("{\small " + brackets[i].locabbr + "}")
        if i != len(brackets) - 1:
            outfile.w(r"&")
        else:
            outfile.wl("")
    outfile.wl(r"\end{tournamenttable}")


def generate_day_stickers(day):
    # create header
    outfile = cfile("../LaTeX/python_output/sticker_" + day + ".tex", "w")

    # open headerfile
    headerfile = open("../LaTeX/source/sticker_header.ptex", "r")

    # paste headerfile into output
    outfile.write(headerfile.read())
    headerfile.close()

    mydata = sigma_parser.SigmaParser()

    # prepare the data

    for row in mydata.stickerPlacement:
        for i in range(len(row)):
            name = row[i]
            createCounselorSticker(name, day, mydata, outfile)
            if i != 3:
                outfile.wl(r"\horizontalshiftfornextsticker")

        outfile.wl(r"\verticalshiftfornextsticker")

    counter = 0
    for name in mydata.staff:
        if mydata.staff[name].role == "faculty":
            counter += 1
            createCounselorSticker(name, day, mydata, outfile)
            if counter != 4:
                outfile.wl(r"\horizontalshiftfornextsticker")
            else:
                outfile.wl(r"\verticalshiftfornextsticker")
                counter = 0

    outfile.wl(r"\end{document}")
    #

    outfile.close()


def generate_camper_info_stickers():
    # create header
    outfile = cfile("../LaTeX/python_output/camper_list_stickers.tex", "w")

    # open headerfile
    headerfile = open("../LaTeX/source/sticker_header_horizontal.ptex", "r")

    # paste headerfile into output
    outfile.write(headerfile.read())
    headerfile.close()

    mydata = sigma_parser.SigmaParser()

    counter = 0
    for name in mydata.staff:
        if mydata.staff[name].role == "counselor":
            team = mydata.staff[name].team
            if team is not None:
                camperlist = [
                    camper for camper in mydata.camperInfo if camper.team == team
                ]

                counter += 1
                stickerheader = name + " -- Team " + "\\LARGE $\\" + team + "$"

                outfile.wl(r"\begin{sticker}")
                outfile.wl(r"\stickertitle{" + stickerheader + r"}")

                # create schedule table
                outfile.wl("\\begin{campertable}")
                outfile.w(
                    "\\textbf{Name} & \\textbf{Age} & \\textbf{Morning} & \\textbf{Afternoon} \\\\ \n \\hline\n"
                )

                for i in range(len(camperlist)):
                    camperSuperscript = ""
                    if not camperlist[i].past_camps and not camperlist[i].epi:
                        camperSuperscript = r"$^\text{new}$"

                    elif camperlist[i].epi and camperlist[i].past_camps:
                        camperSuperscript = r"$^\text{epi}$"

                    elif camperlist[i].epi and not camperlist[i].past_camps:
                        camperSuperscript = r"$^\text{new, epi}$"

                    outfile_string = (
                        camperlist[i].namefirst
                        + " "
                        + camperlist[i].namelast
                        + camperSuperscript
                        + "&"
                        + camperlist[i].age
                        + "&"
                        + camperlist[i].semilab1.replace("_", " ")[:13]
                        + "&"
                        + camperlist[i].semilab2.replace("_", " ")[:13]
                    )
                    outfile.w(outfile_string.encode("utf-8").strip())
                    if i != len(camperlist) - 1:
                        outfile.wl("\\\\")
                outfile.wl("\\end{campertable}")
                outfile.wl(r"\end{sticker}")
                if counter == 2:
                    outfile.wl(r"\verticalshiftfornextsticker")
                    counter = 0
                else:
                    outfile.wl(r"\horizontalshiftfornextsticker")

    outfile.wl(r"\end{document}")


def generate_camper_info_stickers_lena():
    # create header
    outfile = cfile("../LaTeX/python_output/camper_list_stickers_lena.tex", "w")

    # open headerfile
    headerfile = open("../LaTeX/source/sticker_header_horizontal.ptex", "r")

    # paste headerfile into output
    outfile.write(headerfile.read())
    headerfile.close()

    mydata = sigma_parser.SigmaParser()

    counter = 0
    for team in mydata.teams:
        camperlist = [camper for camper in mydata.camperInfo if camper.team == team]

        counter = counter + 1
        counselorstring = ""

        building = camperlist[0].building

        for counselor in mydata.teams[team].counselors:
            counselorstring = counselorstring + counselor + " \ \ "
        stickerheader = (
            counselorstring + "{\\LARGE $\\" + team + "$}" + " (" + building + ")"
        )

        outfile.wl(r"\begin{sticker}")
        outfile.wl(r"\stickertitle{" + stickerheader + r"}")

        # create schedule table
        outfile.wl("\\begin{campertable}")
        outfile.w(
            "\\textbf{Name} & \\textbf{Age} & \\textbf{Morning} & \\textbf{Afternoon} \\\\ \n \\hline\n"
        )

        for i in range(len(camperlist)):
            camperSuperscript = ""
            if not camperlist[i].past_camps and not camperlist[i].epi:
                camperSuperscript = r"$^\text{new}$"

            elif camperlist[i].epi and camperlist[i].past_camps:
                camperSuperscript = r"$^\text{epi}$"

            elif camperlist[i].epi and not camperlist[i].past_camps:
                camperSuperscript = r"$^\text{new, epi}$"

            outfile_string = (
                camperlist[i].namefirst
                + " "
                + camperlist[i].namelast
                + camperSuperscript
                + "&"
                + camperlist[i].age
                + "&"
                + camperlist[i].semilab1.replace("_", " ")[:13]
                + "&"
                + camperlist[i].semilab2.replace("_", " ")[:13]
            )
            outfile.w(outfile_string.encode("utf-8").strip())
            if i != len(camperlist) - 1:
                outfile.wl("\\\\")
        outfile.wl("\\end{campertable}")
        outfile.wl(r"\end{sticker}")
        if counter == 2:
            outfile.wl(r"\verticalshiftfornextsticker")
            counter = 0
        else:
            outfile.wl(r"\horizontalshiftfornextsticker")

    outfile.wl(r"\end{document}")


def generate_camper_name_badges():
    # create header
    outfile = cfile("../LaTeX/python_output/camper_nametags.tex", "w")

    # open headerfile
    headerfile = open("../LaTeX/source/sticker_header_horizontal.ptex", "r")

    # paste headerfile into output
    outfile.write(headerfile.read())
    headerfile.close()

    mydata = sigma_parser.SigmaParser()

    counter = 0
    for camper in mydata.camperInfo:
        if counter < 1:
            team = camper.team
            campernamefirst = camper.namefirst
            campernamelast = camper.namelast

            counter = counter + 1

            outfile.wl(r"\begin{sticker}")

            outfile.wl(
                r"\nametagtitle{\fontsize{35}{40}\selectfont " + campernamefirst + r"}"
            )
            stickerheader = campernamelast
            outfile.wl(r"\nametagtitle{" + stickerheader + r"}")

            # + "}" + " -- \\Huge $\\" + team + "$"

            outfile.wl(r"\end{sticker}")
            if counter == 2:
                outfile.wl(r"\verticalshiftfornextsticker")
                counter = 0
            else:
                outfile.wl(r"\horizontalshiftfornextsticker")

    outfile.wl(r"\end{document}")


def generate_team_schedule():
    # create header
    outfile = cfile("../LaTeX/python_output/team_schedule.tex", "w")

    # open headerfile
    headerfile = open("../LaTeX/source/team_schedule_header.ptex", "r")

    # paste headerfile into output
    outfile.write(headerfile.read())
    headerfile.close()

    mydata = sigma_parser.SigmaParser()

    for team in mydata.teams:
        all_events = mydata.teams[team].events

        outfile.wl("\\titletext{Team $\\" + team + "$  Duty Schedule}")

        counter = 0
        for day in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]:
            counter = counter + 1
            today_events = [
                event
                for event in all_events
                if event.day == day and event.timeStart != "NA"
            ]
            ordered_events = sorted(today_events)
            if len(ordered_events) != 0:
                outfile.wl("\\vspace{0.20in}")
                outfile.wl("\\dayheader{Day " + str(counter) + " -- " + day + "}\n")

                for myevent in ordered_events:
                    outfile.wl("\\vspace{0.25in}")
                    outfile.wl(
                        "\\event{\\Large "
                        + str(myevent.timeStart)
                        + "}{\\Large "
                        + myevent.name
                        + "} \\\\"
                    )
        outfile.wl("\\newpage")
        outfile.wl("\\thispagestyle{empty}")

    outfile.wl("\\end{document}")


def createCounselorSticker(name, day, mydata, outfile):
    if mydata.staff[name].team is not None:
        stickerheader = name + " -- " + day + " ($\\" + mydata.staff[name].team + "$)"
    else:
        stickerheader = name + " -- " + day
    # extract all events from counselor
    all_events = mydata.staff[name].events

    # extract team-related tasks and associate with counselor name
    if mydata.staff[name].role == "counselor":
        team = mydata.staff[name].team
        if team is not None:
            all_events.extend(mydata.teams[team].events)

    filtered_events = []

    for event in all_events:
        if event.day == day:
            if event.timeStart != "NA":
                filtered_events.append(event)
            else:
                pass
                # print(event.name)

    ordered_events = sorted(filtered_events)

    morningreminders = [
        event.name
        for event in mydata.staff[name].events
        if event.category == "morningreminder" and event.day == day
    ]
    afternoonreminders = [
        event.name
        for event in mydata.staff[name].events
        if event.category == "afternoonreminder" and event.day == day
    ]
    eveningreminders = [
        event.name
        for event in mydata.staff[name].events
        if event.category == "eveningreminder" and event.day == day
    ]
    teamreminders = [
        event.name
        for event in mydata.staff[name].events
        if event.category == "teamreminder" and event.day == day
    ]
    personalreminders = [
        event.name
        for event in mydata.staff[name].events
        if event.category == "personalreminder" and event.day == day
    ]

    outfile.wl(r"\begin{sticker}")

    # create tournament table
    tournamentBracketsToday = [
        bracket for bracket in mydata.STBrackets if bracket.day == day
    ]
    createtournamenttable(outfile, tournamentBracketsToday)

    outfile.wl(r"\stickertitle{" + stickerheader + r"}")

    # insertion times for reminders
    morningRemindersTime = "8:30 AM"
    afternoonRemindersTime = "1:00 PM"
    eveningRemindersTime = "10:00 PM"

    if len(teamreminders) != 0:
        outfile.wl("\\header{" + "black" + "}{Team Reminders}\n\\begin{stickerlist}")
        for reminder in teamreminders:
            outfile.wl("\\item " + reminder)
        outfile.wl("\\end{stickerlist}")

    if len(personalreminders) != 0:
        outfile.wl(
            "\\header{" + "black" + "}{Personal Reminders}\n\\begin{stickerlist}"
        )
        for reminder in personalreminders:
            outfile.wl("\\item " + reminder)
        outfile.wl("\\end{stickerlist}")

    # schedule table for entries before breakfast
    outfile.wl("\\begin{scheduletable}")
    for entry in ordered_events:
        if entry.timeStart < morningRemindersTime:
            outfile.wl(
                "\\scheduleentry{"
                + entry.timeStart.print_hour_and_minutes()
                + "}{"
                + entry.timeStart.ampm
                + "}{"
                + entry.name
                + "}"
            )
    outfile.wl("\\end{scheduletable}")

    # morning reminders
    if len(morningreminders) != 0:
        outfile.wl("\\header{" + "red" + "}{Morning Reminders}\n\\begin{stickerlist}")
        for reminder in morningreminders:
            outfile.wl("\\item " + reminder)
        outfile.wl("\\end{stickerlist}")

    # schedule table for entries before lunch and after breakfast
    outfile.wl("\\begin{scheduletable}")
    for entry in ordered_events:
        if (
            entry.timeStart > morningRemindersTime
            and entry.timeStart < afternoonRemindersTime
        ):
            outfile.wl(
                "\\scheduleentry{"
                + entry.timeStart.print_hour_and_minutes()
                + "}{"
                + entry.timeStart.ampm
                + "}{"
                + entry.name
                + "}"
            )
    outfile.wl("\\end{scheduletable}")

    # afternoon reminders
    if len(afternoonreminders) != 0:
        outfile.wl(
            "\\header{" + "green" + "}{Afternoon Reminders}\n\\begin{stickerlist}"
        )
        for reminder in afternoonreminders:
            outfile.wl("\\item " + reminder)
        outfile.wl("\\end{stickerlist}")

    # create schedule table for entries before team time and after lunch
    outfile.wl("\\begin{scheduletable}")
    for entry in ordered_events:
        if (
            entry.timeStart > afternoonRemindersTime
            and entry.timeStart < eveningRemindersTime
        ):
            outfile.wl(
                "\\scheduleentry{"
                + entry.timeStart.print_hour_and_minutes()
                + "}{"
                + entry.timeStart.ampm
                + "}{"
                + entry.name
                + "}"
            )
    outfile.wl("\\end{scheduletable}")

    # evening reminders
    if len(eveningreminders) != 0:
        outfile.wl("\\header{" + "blue" + "}{Evening Reminders}\n\\begin{stickerlist}")
        for reminder in eveningreminders:
            outfile.wl("\\item " + reminder)
        outfile.wl("\\end{stickerlist}")

    # create schedule table for entries before dinner and after lunch
    outfile.wl("\\begin{scheduletable}")
    for entry in ordered_events:
        if entry.timeStart > eveningRemindersTime:
            outfile.wl(
                "\\scheduleentry{"
                + entry.timeStart.print_hour_and_minutes()
                + "}{"
                + entry.timeStart.ampm
                + "}{"
                + entry.name
                + "}"
            )
    outfile.wl("\\end{scheduletable}")

    outfile.wl(r"\end{sticker}")


def generate_semilab_camper_profiles():
    # create header
    outfile = cfile("../LaTeX/python_output/semilab_camper_profiles.tex", "w")

    # open headerfile
    headerfile = open("../LaTeX/source/sticker_header.ptex", "r")

    # paste headerfile into output
    outfile.write(headerfile.read())
    headerfile.close()

    mydata = sigma_parser.SigmaParser()
    temp = 0
    counter = 0

    camperListTempSubtract = copy.copy(mydata.camperInfo)
    camperListTempSubtract = camperListTempSubtract * 2

    for semilab in mydata.semilabs:
        for camper in mydata.camperInfo:
            if semilab.timeOfDay == "morning":
                camperSemilab = camper.semilab1
            elif semilab.timeOfDay == "afternoon":
                camperSemilab = camper.semilab2
            else:
                raise Exception("Semilab time not valid " + semilab.timeOfDay)
            if (
                camperSemilab.replace("_", " ") == semilab.nameShort
            ):  # and camper.namelast in camperlist:

                if camper.team == "":
                    print(camper.namefirst + " has no team assigned, ignoring...")
                    continue

                camperListTempSubtract.pop(camperListTempSubtract.index(camper))

                team = camper.team
                campernamefirst = camper.namefirst
                campernamelast = camper.namelast

                outfile.wl(r"\renewcommand{\baselinestretch}{1} \begin{sticker}")

                out_string = (
                    r"\stickertitle{" + campernamefirst + " " + campernamelast + r"}"
                )
                outfile.wl(out_string.encode("utf-8").strip())
                semilabHeader = (
                    r"\stickertitle{\fontsize{10}{10}\selectfont "
                    + semilab.nameShort
                    + ", "
                    + semilab.timeOfDay
                    + r"}"
                )
                outfile.wl(semilabHeader.replace("_", "-"))

                filename = campernamelast + " " + campernamefirst + ".jpg"
                out_string_photo = (
                    r"\noindent\begin{minipage}{0.5\textwidth}\includegraphics[width=1in]{camper_photos/"
                    + filename
                    + r"}\end{minipage}\begin{minipage}{0.45\textwidth}"
                )

                outfile.wl(out_string_photo.encode("utf-8").strip())

                if camper.past_camps == "":
                    outfile.wl("\\textbf{New camper} \n")

                outfile.wl("Team: {\Large $\\" + camper.team + "$}\n")
                outfile.wl("Age: " + str(camper.age) + r"\\")
                counselors = ""
                for counselor in mydata.teams[camper.team].counselors:
                    counselors = counselors + r"\ \ " + counselor + r"\\"
                outfile.wl(r"Counselors: \\" + counselors)

                outfile.wl(r"\end{minipage} \\ \vspace{0.07in}")

                otherSemilab = (
                    camper.semilab2
                    if semilab.timeOfDay == "morning"
                    else camper.semilab1
                )

                outfile.wl(r"Other semilab: " + otherSemilab.replace("_", "-"))
                outfile.wl(r"\end{sticker}")

                counter = counter + 1
                if counter == 4:
                    outfile.wl(r"\verticalshiftfornextsticker")
                    counter = 0
                else:
                    outfile.wl(r"\horizontalshiftfornextsticker")

    outfile.wl(r"\end{document}")

    print("UNMATCHED CAMPERS:")
    for camper in camperListTempSubtract:
        print(camper.namelast, camper.semilab1, camper.semilab2)


def generate_custom_named_sticker(filename):
    # create header
    outfile = cfile("../LaTeX/python_output/" + filename + ".tex", "w")

    # open headerfile
    headerfile = open("../LaTeX/source/sticker_header.ptex", "r")

    # paste headerfile into output
    outfile.write(headerfile.read())
    headerfile.close()

    mydata = sigma_parser.SigmaParser()

    # prepare the data

    for row in mydata.stickerPlacement:
        for i in range(len(row)):
            name = row[i]

            outfile.wl(
                r"\renewcommand{\baselinestretch}{0.8} \begin{sticker} \stickertitle{"
                + name
                + " ($\\"
                + mydata.staff[name].team
                + "$)"
                + r"}"
            )

            contents = open("../LaTeX/source/" + filename + ".ptex", "r")
            outfile.write(contents.read())
            contents.close()
            outfile.wl(r"\end{sticker}")
            if i != 3:
                outfile.wl(r"\horizontalshiftfornextsticker")

        outfile.wl(r"\verticalshiftfornextsticker")

    """
    counter = 0
    for name in mydata.staff:
        if mydata.staff[name].role == "faculty":
            counter += 1
            createCounselorSticker(name, day, mydata, outfile)
            if counter != 4:
                outfile.wl(r'\horizontalshiftfornextsticker')
            else:
                outfile.wl(r'\verticalshiftfornextsticker')
                counter = 0
    """

    outfile.wl(r"\end{document}")
    #

    outfile.close()


def generate_item_responsibilities_stickers():
    # create header
    outfile = cfile("../LaTeX/python_output/item_responsibilities_sticker.tex", "w")

    # open headerfile
    headerfile = open("../LaTeX/source/sticker_header.ptex", "r")

    # paste headerfile into output
    outfile.write(headerfile.read())
    headerfile.close()

    mydata = sigma_parser.SigmaParser()

    # prepare the data

    for row in mydata.stickerPlacement:
        for i in range(len(row)):
            name = row[i]

            if name in [item.person_name for item in mydata.itemResponsibilities]:
                outfile.wl(r"\begin{sticker}")
                outfile.wl(r"\stickertitle{" + name + r"}")
                outfile.wl(r"\stickertitle{Item Responsibilities}")
                outfile.wl(r"\begin{stickerlist}")
                for item in mydata.itemResponsibilities:
                    if item.person_name == name:
                        outfile.wl(r"\item " + item.item)
                outfile.wl(r"\end{stickerlist}")
                outfile.wl(r"\end{sticker}")

            if i != 3:
                outfile.wl(r"\horizontalshiftfornextsticker")

        outfile.wl(r"\verticalshiftfornextsticker")

    """
    counter = 0
    for name in mydata.staff:
        if mydata.staff[name].role == "faculty":
            counter += 1
            createCounselorSticker(name, day, mydata, outfile)
            if counter != 4:
                outfile.wl(r'\horizontalshiftfornextsticker')
            else:
                outfile.wl(r'\verticalshiftfornextsticker')
                counter = 0
    """

    outfile.wl(r"\end{document}")
    #

    outfile.close()


days = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]

# generate_camper_info_stickers_lena()

# generate_camper_info_stickers()

# generate_semilab_camper_profiles()

generate_day_stickers("Saturday")

# generate_team_schedule()

# generate_custom_named_sticker("first_night_info")


###########################
# not used
###########################
# generate_camper_name_badges()

# generate_item_responsibilities_stickers()

# lots of JIC this year, each one needs a faculty to be present
