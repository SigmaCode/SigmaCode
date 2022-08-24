import numpy as np, scipy as sp, itertools as it
from pulp import *
import pandas as pd
import os, sys, csv, time
from scipy import optimize as spo
import multiprocessing as mp

#

def title(fl,t,au,d=""): #Standard latex title format
	fl.write("\\title{"+ t + "}\n")
	fl.write("\\author{"+ au + "}\n")
	fl.write("\\date{"+ d + "}\r\n")

def package(fl,p,set=None): #Standard format to include latex packages
	towrite = "\\usepackage"
	if(set != None):
		towrite = towrite + "[" + set + "]"
	towrite = towrite + "{" + p + "}\n"
	fl.write(towrite)

def blSpace(fl,num): #adding a couple new lines to make tex code more readable
	for i in range(num):
		fl.write("\n")

def wShop(fl,t,au,d): #New section in the document
	fl.write("\\section{" + t + "}\n")
	fl.write("\\begin{center}\n")
	fl.write("\\textit{by " + au + "}\n")
	fl.write("\\end{center}\n")
	fig = "./images/" + getFigName(au)
	#includeFig(fl,au,fig)
	blSpace(fl,1)
	fl.write(d)
	blSpace(fl,2)

def getFigName(au): #I didn't realize this year how horrible the file images submitted to the google form would be
	for root, dir, files in os.walk(os.path.join(sys.path[0],"images")): #loops over image folder to find correct file name
		for fname in files:
			if au in fname:
				print(fname)
				return fname
		print('blank') #return a blank in case it doesn't find anything so Nones don't throw exceptions
		return 'blank'


def includeFig(fl,au,fig): #format for including figures in latex documents
	blSpace(fl,2)
	fl.write("\\begin{figure}[h]\n")
	fl.write("\\centering\n")
	fl.write("\\includegraphics[width=0.5\\textwidth]{" + fig + "}\n")
	fl.write("\\end{figure}\n")
	blSpace(fl,2)

dats = pd.read_csv('RawData3.csv')

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

title(f,t="Sigma Workshops 2022",au="\\textit{presented by Alex Frenkel and Anna Rosner}")

f.write("\\begin{document}\r\n")

f.write("\\maketitle\r\n")

for ind, row in dats.iterrows():
	wShop(f,row['title'],row['name'],row['desc'])


f.write("\\end{document}")

f.close()

os.system("pdflatex " + fname)
