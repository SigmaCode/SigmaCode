import latexSetup
import sheetsAPIfuncs as sheets
import os

#Originally written by Anna

#This code generates a Latex document with the 2023 workshop slip design including the names of each day's workshop

#Sets which spreadsheet (a copy of the workshop schedule) and what range to pull from
#TODO: centralize spreadsheet ids
spreadsheet_id = '1vxWPMirCnEAS8g7NVzQC4kw365pNWW2mN4RC9jXkGUc'
#TODO: automate range
range_name = 'Master!D3:D17'

#Gets D3:D17, which stores workshop names, and stores it in names.
names = sheets.get_values(spreadsheet_id, range_name)
nums = sheets.get_values(spreadsheet_id, "Master!E3:E17")

fname = "workshopSlip.tex"
def workshopBox(fl, name = "") :
    #creates a small box for writing preference numbers, and writes text next to it
    fl.write("\\fbox{ \n")
    fl.write("\\begin{minipage}{0.5cm} \n")
    fl.write("\\hfill\\vspace{0.6cm} \n")
    fl.write("\\end{minipage} \n")
    fl.write("} "+ name + "\n")

with open(fname, "w") as fl:
    #TODO: use latexSetup for this
    fl.write("\\documentclass{article}\n")
    fl.write("\\usepackage[margin=0.5in]{geometry}\n")
    fl.write("\\usepackage[pdftex,colorlinks=true]{hyperref}\n")
    fl.write("\\setlength{\parindent}{0pt} \n")
    fl.write("\r\n")
    fl.write("\\begin{document}\r\n")
    fl.write("\\pagestyle{empty} \n")
    fl.write("\\LARGE \n")
    #3 slips can fit on one page, so this runs the code to make a slip 3 times
    for i in range(3):
        fl.write("Mark preferences 1-5 \\hspace{1cm} Name: \\hrulefill \n")
        latexSetup.blSpace(fl,1) #blank space to make Latex more readable
        fl.write("\\vspace{0.1cm} \n")
        fl.write("\\noindent\\begin{tabular}{ @{}l l } \n")
        latexSetup.blSpace(fl,1)
        #to split the workshops into two columns, the code runs for half as many times as there are workshops, writing one row with two workshops every time it runs
        for i in range(int(len(names)*0.5)): 
            workshopBox(fl)
            fl.write(nums[i*2][0] + ": " + names[i*2][0])
            fl.write("& ")
            workshopBox(fl)
            fl.write(nums[i*2+1][0] + ": " + names[i*2+1][0])
            fl.write("\\\\" + " \n")
        #if the number of workshops is odd, the last one doesn't get written in the for loop and needs to be written indiviudally
        if i*2+1 < int(len(names))-1:
            workshopBox(fl)
            fl.write(nums[int(len(names))-1][0] + ": " + names[int(len(names))-1][0])
            fl.write("\\\\" + " \n")
        fl.write("\\end{tabular} \\\\ \n")
        fl.write("\\textbigcircle \\hspace{0.25cm} I'm okay with getting a lower choice if I'm with ")
        fl.write("\\hrulefill \n")
        fl.write("\\vspace{0.3cm} \n")
        fl.write("\\hrule")
        fl.write("\\vspace{0.3cm} \n")
        latexSetup.blSpace(fl,2)
    fl.write("\\end{document}\r\n")

os.system("pdflatex " + fname)