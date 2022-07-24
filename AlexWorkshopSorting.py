import numpy as np, scipy as sp, itertools as it
from pulp import *
import pandas as pd
import os, sys, csv, time
from scipy import optimize as spo
import multiprocessing as mp
import latexSetup

def sanitizePrefs(prs):
	return None

def sanitizeWshops(sched):
	return None


# set coefficients of minimization for the objective function
default = 10000
pref2score = {0:1,1:2,2:4,3:7,4:12}
score2pref = {1:0,2:1,4:2,7:3,12:4}

#Reads off the workshop numbers running that day - only those numbers are allowed preferences.
allowedInput = pd.read_csv('CWPsday4.csv',nrows=1)

#Reads off camper preferences and workshop schedules. The header is the above list of running workshops.
prefs = pd.read_csv('CWPsday4.csv',header=1)
wshopSched = pd.read_csv('WSchedDay4.csv')
print(wshopSched)

# Get the lists of campers' names, and the list of workshop numbers (we don't care about workshop name))
wshops = sorted(list(wshopSched["Number"]))
campers = list(prefs["Camper Name"])


ncampers = len(campers)
nwshops = len(wshops)

#Order gives the position of the workshop in the ordered list. E.g. in the list 2, 6, 14,... order(2) = 0, order(6) = 1, order(14) = 2, etc.
order = dict(zip(range(nwshops),wshops))
invorder = dict(zip(wshops,range(nwshops)))

#Team names
Camper_letters = dict(zip(campers,prefs["Letter"]))

prefs_only = prefs[[
    'pref ' + str(i) 
    for i in np.arange(1,6)
]]

#Workshop capacities
caps = dict(zip(wshops,wshopSched["Capacity"]))


'''The following block defines the preference table. At the intersection of camper and workshop, it tells you
how bad it would be if that camper was assigned to that workshop (from the perspective of the objective function)'''
pref_table = default*np.ones([ncampers, nwshops])

for i in range(prefs_only.shape[0]):
	for j in range(prefs_only.shape[1]):
		p = prefs_only['pref ' + str(j+1)][i]
		try:
			p = int(p)
			if p in wshops:
				pref_table[i,invorder[p]] = pref2score[j]
		except ValueError:
			continue

#Define a linear programming optimization problem.
prob = LpProblem("Workshop_Assignments",LpMinimize)

#Create variables for each camper - these are the variables that will be minimized.
assign_variables = [
    LpVariable.dicts(
        "assign_"+str(camper), 
        list(range(nwshops)), 
        0, 1, cat=LpInteger
    )
    for camper in range(ncampers)
]

for i_w in range(nwshops):
        
    '''upper and lower bounds for each semilab'''
    
    to_sum = []
    for i_c in range(ncampers):
        to_sum.append(assign_variables[i_c][i_w])
    prob += np.sum(to_sum) <= caps[order[i_w]]
    prob += np.sum(to_sum) >= 0

for i_c in range(ncampers):
    to_sum = []
    for i_w in range(nwshops):
        to_sum.append(assign_variables[i_c][i_w])
    prob += np.sum(to_sum) == 1

#List of addends in the objective function, in terms of the camper variables defined above
to_sum_objective = []

for i_w in range(nwshops):

    '''summing over all assignments*preferences'''
    
    for i_c in range(ncampers):
    
        to_sum_objective.append(
            assign_variables[i_c][i_w]*pref_table[i_c][i_w]
        )

#Sum everything into the objective function        
prob += np.sum(to_sum_objective)
solved = prob.solve()

#Some debugging booleans - plist1 will print out what preferences each camper got.
plist1 = False
plist2 = True

if (plist1):
	for i_c in range(ncampers):
		toprint = prefs["Camper Name"][i_c]
		for i_w in range(nwshops):
			if assign_variables[i_c][i_w].varValue > 0:
				toprint = toprint + " " + str(order[i_w]) + " " + str(pref_table[i_c][i_w])
		print(toprint)

#Dictionary between workshops and campers assigned to them
worToCamp = {}
for i_w in range(nwshops):
	camps = []
	for i_c in range(ncampers):
		if assign_variables[i_c][i_w].varValue > 0:
			camps.append(prefs["Camper Name"][i_c])
	worToCamp[order[i_w]] = camps

# The below generates a tex file, which will be compiled to make everything looks nice

# A function to generate the bit of code necessary to format *one* of the workshops
def latexFormat(fl,n):
	w = int(wshopSched["Number"][n])


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
		fl.write(c + " & " + "sigma" + " \\" + "\\" + "\n")

	fl.write("\\end{tabular}\r\n")

#Where the latex file will be printed
fname = "worTest.tex"

f = open(fname,"w")

#Separate latexsetup document
latexSetup.stdSetup(f)
latexSetup.title(f,"Workshop Assignments")

f.write("\\begin{document}\r\n")
f.write("\\maketitle\n")

for i_w in range(nwshops):
	latexFormat(f,i_w)
	if (i_w+1) % 3 == 0:
		f.write("\\pagebreak\r\n")

f.write("\\end{document}\n")
f.close()

#Sends a command to the os to compile the tex document we just made into a pdf
os.system("pdflatex " + fname)

#very simple Latex for workshop signup
def latexSignUp(fl, wshopList):
	fl.write("\\Name: \hrulefill \n")
	fl.write("\\Team: \hrulefill \n")
	fl.write("\\Today's workshops: ")
	for wshop in wshopList:
		fl.write(str(wshop)+" ")
	fl.write("\\Rank in order of preference: ")
	fl.write("\\1: \hrulefill \n")
	fl.write("\\2: \hrulefill \n")
	fl.write("\\3: \hrulefill \n")
	fl.write("\\4: \hrulefill \n")
	fl.write("\\5: \hrulefill \n")

#Creates file named wshopPref for the compiled Latex
fname = "wshopPref.tex"
file = open(fname,"w")

#Sets up file with Title
latexSetup.stdSetup(file)
latexSetup.title(file,"Workshop Preference")
f.write("\\begin{document}\r\n")
f.write("\\maketitle\n")

#creates the file using the preferred destination and list of workshops
latexSignUp(file,wshops)

#closes and compiles file
f.write("\\end{document}\n")
f.close()
os.system("pdflatex " + fname)