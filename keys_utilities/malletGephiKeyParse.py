#!/usr/bin/env python
# -*- coding: utf-8 -*-
# copyright 2017 Ryan Horne, Released under GPLv3
# basic utility to parse the keys generated by Mallet, and format a .csv for use in Gephi

import csv 
import sys

#check to see that we have a file name
if len(sys.argv) > 1:
	outputFileName = "%s[Edges].csv" % (sys.argv[1])
	outputFile = open(outputFileName, 'w')
	outputFile.writelines ("source,target")
	outputFile.writelines('\n')
	with open(sys.argv[1], 'rb') as tsv:
		for line in csv.reader(tsv, delimiter="\t"):
			# split the text
			words = line[2].split()
			# for each word in the line:
    			for word in words:
				#print the word and output to the file
					print(line[0],word)
					outputFile.writelines("%s,%s" %(line[0],word))
					outputFile.writelines('\n')

	#close all the files
	outputFile.close()
	tsv.close()