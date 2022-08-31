import numpy as np, scipy as sp, itertools as it
from pulp import *
import pandas as pd
import os, sys, csv, time
from scipy import optimize as spo
import multiprocessing as mp


def title(fl, t, au="", d="", s=True):
    """
    Standard latex title format, parameters not set will be blank by default. Writes title, and begins document and makes title unless otherwise indicated

    Parameters:
            fl (string): the file path to write to, including the file extension
            t (string): the title of the document to be written in the Latex title
            au (string): the author(s) of the document to be written in the Latex title, defaults to ""
            d (string): the date to be written in the Latex title, no particular format needed, defaults to ""
            s (bool): if false, the document won't be started and the title won't be made, defaults to True
    """

    # writes the title based on parameters to the file
    fl.write("\\title{" + t + "}\n")
    fl.write("\\author{" + au + "}\n")
    fl.write("\\date{" + d + "}\r\n")
    # begins document and makes the title if start is true (default behavior)
    if s:
        fl.write("\\begin{document}\r\n")
        fl.write("\\maketitle\n")


def package(fl, p, set=None):
    """
    Standard format to include latex packages

    TODO: finish docstring, change function name

    :param fl: _description_
    :type fl: _type_
    :param p: _description_
    :type p: _type_
    :param set: _description_, defaults to None
    :type set: _type_, optional
    """

    towrite = "\\usepackage"

    if set != None:
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

    if set != None:
        towrite = towrite + "[" + set + "]"

    towrite = towrite + "{article}\r\n"
    fl.write(towrite)

    package(fl, "inputenc", set="utf8")
    package(fl, "graphicx")
    package(fl, "physics")
    package(fl, "mathtools")
    package(fl, "amsmath")
    package(fl, "bbold")
    package(fl, "geometry")
    package(fl, "hyperref", set="pdftex,colorlinks=true")
