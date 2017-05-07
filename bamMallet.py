#!/usr/bin/env python
# -*- coding: utf-8 -*-
# copyright 2017 Ryan Horne, Released under GPLv3
# Version 0.9
# utility to execute mallet given a .mallet file on the command line
# the command is: python bamMallet.py malletFile bamMalletConfig outputDirectory
# malletFile = path to your .mallet file
# bamMalletConfig = path to the config.json file
# outputDirectory = path to the output directory you want
# right now there is no graceful error checking - it just blows up if there is a problem
#

import csv 
import sys
import os
import json
import subprocess


#check to see that we have arguments
if len(sys.argv) > 0:
	#assign the values as needed
	
	malletFileName = sys.argv[1]
	configFileName = sys.argv[2]
	numberOfKeys = sys.argv[3]
	outputDirectoryName = sys.argv[4]
		
	# make the "holder" directory if it is not there. We will overwrite any files in it that were made before
	if not os.path.exists(outputDirectoryName):
		os.makedirs(outputDirectoryName)
		
	with open(configFileName, 'r') as json_data:
		data = json.load(json_data)
		
		mainCommand = ('{0}/./bin/mallet train-topics --num-top-words {1} --input {2}'.format(data["malletInstallDirectory"],numberOfKeys, malletFileName))

		for topicCount in data["topicCounts"]:
			pathForTopic = ('{0}/Topic_count_{1}'.format(outputDirectoryName, topicCount))
			if not os.path.exists(pathForTopic):
				os.makedirs(pathForTopic)
			
			for optNumber in data["optimizationIntervals"]:
				tempCommand = ''
				tempCommand +=(' --num-topics {0}'.format(topicCount))
				tempCommand +=(' --optimize-interval {0}'.format(optNumber))
				pathForOpt =  ('{0}/Optimization_count_{1}'.format(pathForTopic, optNumber))
				if not os.path.exists(pathForOpt):
					os.makedirs(pathForOpt)
					
				for iterationsNum in data["iterations"]:
					tempCommand = ''
					tempCommand +=(' --num-iterations {0}'.format(iterationsNum))
					tempCommand +=(' --num-topics {0}'.format(topicCount))
					tempCommand +=(' --optimize-interval {0}'.format(optNumber))
					pathForIter =  ('{0}/Iterations_{1}'.format(pathForOpt, iterationsNum))
					if not os.path.exists(pathForIter):
						os.makedirs(pathForIter)

					#now fire the commands
					for commandText in data["commands"]:
						tempCommand += (' {0} {1}/{2}'.format(commandText["command"], pathForIter, commandText["output"]))
				
					executeCommand = ('{0}{1}'.format(mainCommand,tempCommand))
					subprocess.call(executeCommand, shell=True)
				
					#Now take these outputs and make what files we need off of them - Gephi input, etc
					commandText =''
					for commandText in data["commands"]:
						#check if the command
						if  commandText["command"] == "--output-topic-keys":
							outCommandName = commandText["output"].split('.')
							outputFileName = ('{0}/{1}_[Edges].csv'.format(pathForIter,outCommandName[0]))
							outputFile = open(outputFileName, 'w')
							outputFile.writelines ("source,target")
							outputFile.writelines('\n')
							with open('{0}/{1}'.format(pathForIter,commandText["output"]), 'rb') as tsv:
								for line in csv.reader(tsv, delimiter="\t"):
									# split the text
									words = line[2].split()
									# for each word in the line:
									for word in words:
										outputFile.writelines('{0},{1}'.format(line[0],word))
										outputFile.writelines('\n')
								#close all the files
								outputFile.close()
								tsv.close()
					
						if  commandText["command"] == "--word-topic-counts-file":
							outCommandName = commandText["output"].split('.')
							allOutputFileName = ('{0}/{1}_All[Edges].csv'.format(pathForIter,outCommandName[0]))
							allOutputFile = open(allOutputFileName, 'w')
							allOutputFile.writelines ("source,target,frequency")
							sharedConnectionsOutputFileName = ('{0}/{1}_Shared[Edges].csv'.format(pathForIter,outCommandName[0]))
							sharedConnectionsOutputFile = open(sharedConnectionsOutputFileName, 'w')
							sharedConnectionsOutputFile.writelines ("source,target,frequency")
						
							with open('{0}/{1}'.format(pathForIter,commandText["output"]), 'rb') as frequencyFile:
								for line in csv.reader(frequencyFile, delimiter=" "):
									#first, add the first entry to the all nodes file. Next we add anything beyond that to the connections only file
										for i in range(2, len(line)):
											allOutputFile.writelines('\n')
											allOutputFile.writelines('{0},"{1}",{2}'.format(line[i].split(':')[0],line[1],line[i].split(':')[1]))
										
											if len(line) > 3:
												sharedConnectionsOutputFile.writelines('\n')
												sharedConnectionsOutputFile.writelines('{0},"{1}",{2}'.format(line[i].split(':')[0],line[1],line[i].split(':')[1]))
											
allOutputFile.close()
sharedConnectionsOutputFile.close()
frequencyFile.close()