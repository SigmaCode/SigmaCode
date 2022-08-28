import pandas as pd
import os
import latexSetup

#This code uses a CSV of one day's workshop schedule and generates a Latex document that lists a workshop's number, name, location, instructor(s) and mentor(s).
#NOTE: this was written during camp! It works but it's fairly janky
#TODO: none of this follows the naming conventions, this will get fixed soon!

#Uses Pandas to read in the data from the downloaded daily schedule
#TODO: read this from the spreadsheet using Google API
wshopdata = pd.read_csv('Friday.csv')
#Reading individual columns using headers
instructor = wshopdata["Instructors"]
instructor2 = wshopdata["Instructor 2"]
mentor = wshopdata["Mentor"]
name = wshopdata["Name"]
num = wshopdata["#"]
location = wshopdata["Location"]

#Sets file name and opens file to write Latex to
fname = "StaffWshopListFri.tex"
output = open(fname,"w")

#Sets up the beginning of the Latex document, adds and writes the title
latexSetup.stdSetup(output)
latexSetup.title(output,"Sigma Workshops: Friday (Starts at 6:45)")
output.write("\\begin{document}\r\n")
output.write("\\maketitle\n")

loctitle = ""
i = 0
#TODO: reduce general file writing jank (this was code written during camp)
#TODO: make this less janky, using a counter in a for loop like this is just messy
#iterates through the workshops, additionally using a counter variable to index other columns (this is bad, see above)
for wshop in name:
    #If a cell isn't filled, Pandas stores it as NaN, and the Pandas isna() function is the best to check it
    #If the workshop has a mentor, it is a JIC workshop, and therefore the title includes "JIC: " before the title
    #The format of the title is "Number     Name (Location)"
    if pd.isna(mentor[i]) != True:
        output.write("\\section*{" + num[i] +"$\quad$" + "JIC: " + name[i] + " (" + location[i] + ")}\n")
    #If the workshop isn't a JIC workshop, it just gets a title with the workshop number, name, and location
    else: 
        output.write("\\section*{" + num[i] +"$\quad$" + name[i] + " (" + location[i] + ")}\n")
    #centers line for workshop instructors
    output.write("\\begin{center}\n")
    #NOTE: this is quite possibly the worst way to do this.
    if pd.isna(mentor[i]) != True:
        if pd.isna(instructor2[i]) != True:
            #If the workshop has a mentor and two instructors, they are all written to the file, in the format "by instructor1 and instructor2, mentored by mentor"
            output.write("\\textit{by "+ instructor[i] + " and " + instructor2[i] + ", mentored by " + mentor[i] + "}\n")
        else:
            #If the workshop has a mentor and one instructor, they are all written to the file, in the format "by instructor, mentored by mentor"
            output.write("\\textit{by "+ instructor[i] + ", mentored by " + mentor[i] + "}\n")
    elif pd.isna(instructor2[i]) != True:
        #If the workshop has two instructors, they are both written to the file, in the format "by instructor1 and instructor2"
        output.write("\\textit{by "+ instructor[i] + " and " + instructor2[i] + "}\n")
    else:
        #If the workshop has one instructors, they are written to the file, in the format "by instructor"
        output.write("\\textit{by "+ instructor[i] + "}\n")
    output.write("\\end{center}\r\n")
    i += 1 #increases counter for indexing through columns

#closes document and parses the Latex into a PDF (only works from command line)
output.write("\\end{document}\n")
output.close()
os.system("pdflatex " + fname)