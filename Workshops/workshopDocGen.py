import numpy as np, scipy as sp, itertools as it
from pulp import *
import pandas as pd
import os, sys, csv, time
from scipy import optimize as spo
import multiprocessing as mp

#

def wShop(fl,t,au,d,col,im = "None"): #New section in the document
	fl.write("\\section*{" + t + "}\n")
	fl.write("\\begin{center}\n")
	fl.write("\\textit{by " + au + "}\n")
	fl.write("\\end{center}\n")
	if col:
		print(getFigName(im))
		fig = "./images2/" + getFigName(im)
		includeFig(fl,fig)
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


def includeFig(fl,fig): #format for including figures in latex documents
	blSpace(fl,2)
	fl.write("\\begin{figure}[ht]\n")
	fl.write("\\centering\n")
	fl.write("\\includegraphics[width=0.8\\textwidth]{" + fig + "}\n")
	fl.write("\\end{figure}\n")
	blSpace(fl,2)

def latexSignUp(fl, wshopList,jshopList):

	fl.write("\\documentclass{article}\n")

	fl.write("\\usepackage[utf8]{inputenc}\n")
	fl.write("\\usepackage{inputenc}\n")
	fl.write("\\usepackage{graphicx}\n")
	fl.write("\\usepackage{physics}\n")
	fl.write("\\usepackage{mathtools}\n")
	fl.write("\\usepackage{amsmath}\n")
	fl.write("\\usepackage{bbold}\n")
	fl.write("\\usepackage[margin=0.5in]{geometry}\n")
	fl.write("\\usepackage[pdftex,colorlinks=true]{hyperref}\n")
	fl.write("\r\n")

	fl.write("\\begin{document}\r\n")
	fl.write("\\huge \n")

	for i in range(3):

		fl.write("Name: \\hrulefill \n")
		blSpace(fl,1)
		fl.write("Today's workshops: ")
		blSpace(fl,1)
		for wshop in wshopList:
			fl.write(str(int(wshop) + 1) + " ")
		for jshop in jshopList:
			fl.write("J" + str(int(jshop) + 1) + " ")
		fl.write("\n")
		blSpace(fl,1)
		fl.write("Rank in order of preference: \n")
		blSpace(fl,1)
		fl.write("1: \\hrulefill \n")
		blSpace(fl,1)
		fl.write("2: \\hrulefill \n")
		blSpace(fl,1)
		fl.write("3: \\hrulefill \n")
		blSpace(fl,1)
		fl.write("4: \\hrulefill \n")
		blSpace(fl,1)
		fl.write("5: \\hrulefill \n")
		blSpace(fl,1)
		fl.write("\\vspace{1cm} \n")
		blSpace(fl,1)


	fl.write("\\end{document}\r\n")

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
		title(f,t="Sigma Workshops 2022",au="\\textit{presented by Alex Frenkel and Anna Rosner}")

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

latexSignUp(f2,wShopList,jShopList)

f2.close()

os.system("pdflatex " + fname)
os.system("pdflatex " + fname2)