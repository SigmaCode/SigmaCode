import numpy as np, scipy as sp, itertools as it
from pulp import *
import pandas as pd
import os, sys, csv, time
from scipy import optimize as spo
import multiprocessing as mp

#Originally written by Alex F, expanded functions and documentation by Anna

def title(file, title, author="", date="", setup=True):
	"""
	Standard latex title format, parameters not set will be blank by default. Writes title, and begins document and makes title unless otherwise indicated

	Parameters:
		file (string): the file path to write to, including the file extension
		title (string): the title of the document to be written in the Latex title
		author (string): the author(s) of the document to be written in the Latex title, defaults to ""
		date (string): the date to be written in the Latex title, no particular format needed, defaults to ""
		setup (bool): if false, the document won't be started and the title won't be made, defaults to True
	"""

	#writes the title based on parameters to the file
	file.write("\\title{"+ title + "}\n")
	file.write("\\author{"+ author + "}\n")
	file.write("\\date{"+ date + "}\r\n")
	#begins document and makes the title if setup is true (default behavior)
	if setup:
		file.write("\\begin{document}\r\n")
		file.write("\\maketitle\n")


def package(fl, p, set=None):
	"""
	Standard format to include latex packages

	:param fl: _description_
	:type fl: _type_
	:param p: _description_
	:type p: _type_
	:param set: _description_, defaults to None
	:type set: _type_, optional
	"""

	towrite = "\\usepackage"

	if(set != None):
		towrite = towrite + "[" + set + "]"
	towrite = towrite + "{" + p + "}\n"
	fl.write(towrite)


def stdSetup(fl, set=None):
	"""
	TODO: Add method description

	TODO: finish docstring, change function name

	:param fl: _description_
	:type fl: _type_
	:param set: _description_, defaults to None
	:type set: _type_, optional
	"""
	
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

def blSpace(fl,num): #adding a couple new lines to make tex code more readable
	for i in range(num):
		fl.write("\n")

def includeFig(fl,fig): #format for including figures in latex documents
	blSpace(fl,2)
	fl.write("\\begin{figure}[ht]\n")
	fl.write("\\centering\n")
	fl.write("\\includegraphics[width=0.8\\textwidth]{" + fig + "}\n")
	fl.write("\\end{figure}\n")
	blSpace(fl,2)
