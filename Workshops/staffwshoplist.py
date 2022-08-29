import pandas as pd
import os
import latexSetup

# This code uses a CSV of one day's workshop schedule and generates a 
# LaTeX document that lists a workshop's number, name, location, 
# instructor(s) and mentor(s).  

# NOTE: this was written during camp! It works but it's fairly janky
# TODO: none of this follows the naming conventions, this will get fixed soon!

# Uses Pandas to read in the data from the downloaded daily schedule
# TODO: read this from the spreadsheet using Google API
wshopdata = pd.read_csv('Friday.csv')

#Reading individual columns using headers
instructor1 = wshopdata["Instructors"]
instructor2 = wshopdata["Instructor 2"]

mentor = wshopdata["Mentor"]
name = wshopdata["Name"]
num = wshopdata["#"]
location = wshopdata["Location"]

#Sets file name and opens file to write Latex to
fname = "StaffWshopListFri.tex"

with open(fname, "w") as output:

    # Sets up the beginning of the Latex document, adds and writes the title
    latexSetup.stdSetup(output)
    latexSetup.title(output,"Sigma Workshops: Friday (Starts at 6:45)")

    output.write("\\begin{document}\r\n")
    output.write("\\maketitle\n")

    for i, wshop in enumerate(name):
        # only jic workshops have mentors
        is_jic = pd.notna(mentor[i])

        # add "JIC: " to jic workshop names
        name_ = name[i]
        if is_jic:
            name_ = "JIC: " + name_

        title = num[i] + "$\\quad$" + name_ + " (" + location[i] + ")"

        output.write("\\section*{" + title + "}\n")

        #centers line for workshop instructors
        output.write("\\begin{center}\n")

        instructors = instructor1[i]
        
        if pd.notna(instructor2[i]):
            instructors += " and " + instructor2[i]

        if is_jic:
            instructors += ", mentored by " + mentor[i]

        output.write("\\textit{by " + instructors + "}\n")
        output.write("\\end{center}\r\n")

    output.write("\\end{document}\n")

os.system("pdflatex " + fname)
