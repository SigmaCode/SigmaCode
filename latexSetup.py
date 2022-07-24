import numpy as np, scipy as sp, itertools as it
from pulp import *
import pandas as pd
import os, sys, csv, time
from scipy import optimize as spo
import multiprocessing as mp

def title(fl,t,au="",d=""):
	fl.write("\\title{"+ t + "}\n")
	fl.write("\\author{"+ au + "}\n")
	fl.write("\\date{"+ d + "}\r\n")

def package(fl,p,set=None):
	towrite = "\\usepackage"
	if(set != None):
		towrite = towrite + "[" + set + "]"
	towrite = towrite + "{" + p + "}\n"
	fl.write(towrite)

def stdSetup(fl,set=None):
	towrite = "\\documentclass"
	if(set != None):
		towrite = towrite + "[" + set + "]"
	towrite = towrite + "{article}\r\n"
	fl.write(towrite)
	package(fl,"inputenc",set="utf8")
	package(fl,"graphicx")
	package(fl,"physics")
	package(fl,"mathtools")
	package(fl,"amsmath")
	package(fl,"bbold")
	package(fl,"geometry")
	package(fl,"hyperref",set="pdftex,colorlinks=true")