import numpy as np, scipy as sp, itertools as it
from pulp import *
import pandas as pd
import os, sys, csv, time
from scipy import optimize as spo
import multiprocessing as mp

def title(t,au,d=""):
	f.write("\\title{"+ t + "}\n")
	f.write("\\author{"+ au + "}\n")
	f.write("\\date{"+ d + "}\r\n")

def package(p,set=None):
	towrite = "\\usepackage"
	if(set != None):
		towrite = towrite + "[" + set + "]"
	towrite = towrite + "{" + p + "}\n"
	f.write(towrite)

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

title(t="Leeeeee",au="Hi Lee")

f.write("\\begin{document}\r\n")

f.write("\\maketitle\r\n")

f.write("\\end{document}")

f.close()

os.system("pdflatex " + fname)