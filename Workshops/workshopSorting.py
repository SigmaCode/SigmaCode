import numpy as np
from pulp import * #used for LP solver
import pandas as pd
import os
import latexSetup
import sheetsAPIfuncs as sheets

#Originally written by Alex F, additional documentation and API usage by Anna

#Algorithm To Do List (feel free to add):
#TODO: Seperate glassblowing
#TODO: JIC system
#TODO: Favor unlucky campers
#TODO: Clean up LaTeX
#TODO: Refactor some weird bits to make it make more sense
#TODO: Make main stuff into a function
#TODO: naming conventions? probably not worth it

def sanitizePrefs(prs):
	#Ideally, will get rid of garbage in the preference sheet if it makes it through
	return None

def sanitizeWshops(sched):
	#Ideally, would make workshops Latex compatible without manual effort
	return None

default = 10000
#set coefficients of minimization for the objective function
#getting their first preference gets a score of 1, and their last gives a score of 12. The linear optimization seeks to minimize the total score
pref2score = {0:1,1:2,2:4,3:7,4:12}
score2pref = {1:0,2:1,4:2,7:3,12:4}

#Reads off camper preferences and workshop schedules. The header is the above list of running workshops.
#TODO: try except
prefid = "18FYysCjoPQyR9QmOeix30vmNnzZEUS4eCJDsWQs6nM8" #https://docs.google.com/spreadsheets/d/18FYysCjoPQyR9QmOeix30vmNnzZEUS4eCJDsWQs6nM8/edit#gid=0
prefrange = "Test!A2:G121"
prefs = sheets.get_values(prefid, prefrange)
prefs = pd.DataFrame(prefs[1:], columns=prefs[0])

schedid = "1vxWPMirCnEAS8g7NVzQC4kw365pNWW2mN4RC9jXkGUc" #https://docs.google.com/spreadsheets/d/1vxWPMirCnEAS8g7NVzQC4kw365pNWW2mN4RC9jXkGUc/edit#gid=1326176959
schedrange = "Monday Raw Data!A1:F17"
schedule = sheets.get_values(schedid, schedrange)
wshopSched = pd.DataFrame(schedule[1:], columns=schedule[0])
#wshopSched = pd.read_csv('WSched5.csv')

# Get the lists of campers' names, and the list of workshop numbers (we don't care about workshop name))
wshopscodes = list(wshopSched["Number"])
for num in wshopscodes:
	try:
		num = int(num)
	except:
		continue
wshopscodes = sorted(wshopscodes)
campers = list(prefs["Camper Name"])

ncampers = len(campers)
nwshops = len(wshopscodes)

#Order gives the position of the workshop in the ordered list. E.g. in the list 2, 6, 14,... order(2) = 0, order(6) = 1, order(14) = 2, etc.
order = dict(zip(range(nwshops),wshopscodes))
invorder = dict(zip(wshopscodes,range(nwshops)))

#Creates a dictionary of each camper as the key and the name of the team they're on as the value
Camper_letters = dict(zip(campers,prefs["Letter"]))

#Creates an isolated table of preferences in order with a header of which preference is which
prefs_only = prefs[['Pref ' + str(i) for i in np.arange(1,6)]]

#Creates a dictionary of each workshop code as the key and the capacity of that workshop as the value
caps = dict(zip(wshopscodes,wshopSched["Capacity"]))

'''The following block defines the preference table. At the intersection of camper and workshop, it tells you
how bad it would be if that camper was assigned to that workshop (from the perspective of the objective function)'''

#makes a table the width of the number of campers and the height of the number of workshops and initializes it with the default value (10000).
pref_table = default*np.ones([ncampers, nwshops])

#Iterates through each camper in the table of camper preferences
for i in range(ncampers):
	#Iterates through each preference of that camper
	for j in range(5):
		#For each preference, finds the workshop code
		p = prefs_only['Pref ' + str(j+1)][i] #Uses the "Pref #" headers to index the colums
		try:
			'''If the workshop code is in the list of workshops in the schedule, it finds the 
			score associated with that preference and writes that in the cell where the camper 
			and that workshop intersect'''
			if p in wshopscodes:
				pref_table[i,invorder[p]] = pref2score[j] #Finds the index of the workshop code, and the score based on preference (the first column is first preference etc)
			#Debugging if workshop code is not in list of workshops
			else:
				print("error: " + str(p) + ", " + campers[i])
		except ValueError:
			continue

#DANGER ZONE: if you are touching the code below, please be EXTREMELY careful, this is the logic that drives the algorithm.

#Define a linear programming optimization problem.
lpprob = LpProblem("Workshop_Assignments",LpMinimize)

#Creates an array of dictionaries - one dictionary for each camper - each of which has a variable for each workshop - these are the variables that will be minimized.
#If you want to see more documentation, https://s3.amazonaws.com/assets.datacamp.com/production/course_8835/slides/chapter2.pdf has an explanation of LpVariable.dicts()
assign_variables = [
    LpVariable.dicts(
        "assign_"+str(camper), #For each camper, they recieve a number from 0 to 1 less than the total number of campers: the first camper is 0, the 119th is 118 etc
        list(range(nwshops)), #Iterates through how many workshops there are
        0, 1, cat=LpInteger #Makes one per camper, of category LpInteger
    )
    for camper in range(ncampers)
]

#upper and lower bounds for each semilab
#Iterates through each workshop
for i_w in range(nwshops):
	to_sum = []
	#Iterates through each camper
	for i_c in range(ncampers):
		to_sum.append(assign_variables[i_c][i_w])
	lpprob += np.sum(to_sum) <= int(caps[order[i_w]]) #The number of campers needs to be lower than the capacity
	lpprob += np.sum(to_sum) >= 0

for i_c in range(ncampers):
    to_sum = []
    for i_w in range(nwshops):
        to_sum.append(assign_variables[i_c][i_w])
    lpprob += np.sum(to_sum) == 1

#List of addends in the objective function, in terms of the camper variables defined above
to_sum_objective = []
for i_w in range(nwshops):
    #summing over all assignments*preferences
    for i_c in range(ncampers):
        to_sum_objective.append(
            assign_variables[i_c][i_w]*pref_table[i_c][i_w]
        )

#Sum everything into the objective function        
lpprob += np.sum(to_sum_objective)
solved = lpprob.solve() #actually does the thing

#Writes which preference they recieved to the preference spreadsheet
nprefs = []
for i_c in range(ncampers):
	for i_w in range(nwshops):
		if assign_variables[i_c][i_w].varValue > 0:
			try:
				towrite = str(score2pref[pref_table[i_c][i_w]]+1)
			except:
				towrite = "JIC or error"
			nprefs.append([towrite])
#add try except
try:
	sheets.update_values(prefid, "H3:H", nprefs)
except:
	print("Error writing to spreadsheet")

#Some debugging booleans - plist1 will print out what preferences each camper got.
plist1 = True
plist2 = True

if (plist1):
	for i_c in range(ncampers):
		toprint = str(prefs["Camper Name"][i_c])
		for i_w in range(nwshops):
			if assign_variables[i_c][i_w].varValue > 0:
				toprint = toprint + " " + str(order[i_w]) + " " + str(pref_table[i_c][i_w])
		print(toprint)

#Dictionary between workshops and campers assigned to them
worToCamp = {}
campToWor = {}
for i_w in range(nwshops):
	camps = []
	for i_c in range(ncampers):
		if assign_variables[i_c][i_w].varValue > 0:
			wsh = order[i_w]
			wr = wshopSched.loc[wshopSched['Number'] == wsh]
			nwsh = wr.iloc[0]['Workshop Running']
			campToWor[prefs["Camper Name"][i_c]] = nwsh
			camps.append(prefs["Camper Name"][i_c])
	worToCamp[order[i_w]] = camps

print(worToCamp)

# The below generates a tex file, which will be compiled to make everything looks nice

# A function to generate the bit of code necessary to format *one* of the workshops
def latexFormat(fl,n):
	w = wshopSched["Number"][n]


	fl.write("\\begin{center}\n")
	fl.write("\\section*{" + str(wshopSched["Number"][n]) + " " + wshopSched["Workshop Running"][n] + "}\n")
	fl.write("\\end{center}\r\n")

	fl.write("\\begin{center}\n")
	fl.write("\\textit{Location: " + str(wshopSched["Location"][n]) + "}\n")
	fl.write("\\end{center}\r\n")

	fl.write("\\setlength{\\tabcolsep}{60pt}\n")
	fl.write("\\centering\n")
	fl.write("\\begin{tabular}{c c c}\n")

	for c in worToCamp[w]:
		cr = prefs.loc[prefs['Camper Name'] == c]
		fl.write(c + " & " + cr.iloc[0]["Letter"] + " \\" + "\\" + "\n")

	fl.write("\\end{tabular}\r\n")

def latexFormat2(fl,let):
	team = prefs.loc[prefs['Letter'] == let]

	fl.write("\\section*{" + let + "}\n")

	fl.write("\\setlength{\\tabcolsep}{60pt}\n")
	fl.write("\\begin{tabular}{c c}\n")

	for c in team["Camper Name"]:
		wsh = campToWor[c]
		fl.write(c + " & " + wsh + " \\" + "\\" + "\n")

	fl.write("\\end{tabular}\r\n")

#Where the latex file will be printed
fname = "worTest.tex"
fname2 = "worTest2.tex"

f = open(fname,"w")

#Separate latexsetup document
latexSetup.stdSetup(f)
latexSetup.title(f,"Workshop Assignments")

for i_w in range(nwshops):
	latexFormat(f,i_w)
	if (i_w+1) % 3 == 0:
		f.write("\\pagebreak\r\n")

f.write("\\end{document}\n")
f.close()

f2 = open(fname2,"w")
latexSetup.stdSetup(f2)
latexSetup.title(f2,"WorkShop Assignments by Camper")

f2.write("\\centering\n")

lets = prefs["Letter"].unique()

for let in lets:
	latexFormat2(f2,let)

f2.write("\\end{document}\n")
f2.close()


#Sends a command to the os to compile the tex document we just made into a pdf
os.system("pdflatex " + fname)
os.system("pdflatex " + fname2)
