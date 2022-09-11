import numpy as np, scipy as sp, itertools as it
from pulp import *
import pandas as pd
import os, sys, csv, time
import latexSetup
import workshopSlipGen #TODO: use this

#

def wShop(fl,t,au,d,col,im = "None"): #New section in the document
	fl.write("\\section*{" + t + "}\n")
	fl.write("\\begin{center}\n")
	fl.write("\\textit{by " + au + "}\n")
	fl.write("\\end{center}\n")
	if col:
		print(getFigName(im))
		fig = "./images2/" + getFigName(im)
		latexSetup.includeFig(fl,fig)
	latexSetup.blSpace(fl,1)
	fl.write(d)
	latexSetup.blSpace(fl,2)
	if col:
		fl.write("\\pagebreak\n")
		latexSetup.blSpace(fl,2)

def getFigName(im): #I didn't realize this year how horrible the file images submitted to the google form would be
	for root, dir, files in os.walk(os.path.join(sys.path[0],"images2")): #loops over image folder to find correct file name
		for fname in files:
			if im in fname:
				print(fname)
				return fname
		print('blank') #return a blank in case it doesn't find anything so Nones don't throw exceptions
		return 'blank'


dats = pd.read_csv('RawData.csv')
dats2 = pd.read_csv('RawDataJIC.csv')

wShopList = range(dats.shape[0])

print(len(sys.argv))

if len(sys.argv) > 1:
	wShopList = []
	jShopList = []
	for i in range(1, len(sys.argv)):
		if sys.argv[i][0].upper() == 'J':
			jShopList.append(int(sys.argv[i][1:]) - 1)
		else:
			wShopList.append(int(sys.argv[i]) - 1)


sdats = dats.loc[dats.index[wShopList]]
sdats2 = dats2.loc[dats2.index[jShopList]]

color = False

fname = "latexTest.tex"

f = open(fname,"w")
f.write("\\documentclass{article}\n")

f.write("\\usepackage[utf8]{inputenc}\n")
f.write("\\usepackage{inputenc}\n")
f.write("\\usepackage{graphicx}\n")
f.write("\\usepackage{physics}\n")
f.write("\\usepackage{mathtools}\n")
f.write("\\usepackage{amsmath}\n")
f.write("\\usepackage{bbold}\n")
f.write("\\usepackage[margin=1in]{geometry}\n")
f.write("\\usepackage[pdftex,colorlinks=true]{hyperref}\n")
f.write("\r\n")

if not color:
		latexSetup.title(f,t="Sigma Workshops 2022",au="\\textit{presented by Alex Frenkel and Anna Rosner}")

f.write("\\begin{document}\r\n")

#f.write("\\maketitle\r\n")

for ind, row in sdats.iterrows():
	print(ind)
	wShop(f,str(ind + 1) + "$\\quad$" + row['title'],row['name'],row['desc'],color,str(ind + 1) + ".")

for ind, row in sdats2.iterrows():
	print(ind)
	wShop(f,"J" + str(ind + 1) + "$\\quad$" + row['title'],row['name'],row['desc'],color,str(ind + 1) + ".")


f.write("\\end{document}")

f.close()

fname2 = "signup.tex"

f2 = open(fname2,"w")

#TODO: make this run the workshopSlipGen code
#latexSignUp(f2,wShopList,jShopList)

f2.close()

os.system("pdflatex " + fname)
os.system("pdflatex " + fname2)