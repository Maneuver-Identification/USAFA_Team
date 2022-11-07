#!/usr/bin/env python
# coding: utf-8

# In[6]:


import sys, os
sys.argv[1]
rootdir = sys.argv[1]
newdir = sys.argv[2]


def stopped(data):
    threshold = 5 #These are good values to mess with!
    #checks x, then y, then z speeds
    if abs(float(data[5])) <= threshold and abs(float(data[6])) <= threshold and abs(float(data[7])) <= threshold:
        return True
    return False

def teleported(prevData, data):
    threshold = 100 #Another good value to change!
    errorX = (float(prevData[2]) + (float(prevData[5]) * .2)) - float(data[2])
    errorY = (float(prevData[3]) + (float(prevData[6]) * .2)) - float(data[3])
    errorZ = (float(prevData[4]) + (float(prevData[7]) * .2)) - float(data[4])
    if errorX >= threshold or errorY >= threshold or errorZ >= threshold:
        return True
    return False

sorties = []
for subdir,dirs, files in os.walk(rootdir):
    for file in files:
        with open("/"+file, "r") as f:
            #reads header
            f.readline()
            #Reads and throws out first line since they do not contain velocities
            f.readline()
            #reads second line
            prevData = f.readline().split('\t')
            #loops through the rest of the lines
            lines = f.readlines()
            inBad = False   #If we are in a bad section of sortie
            lastStep = 1     #The last time step we viewed (boarder timeStep)
            steps = []
            for line in lines:
                #determines if a line contains bad data
                badTime = False
                data = line.split('\t')
                badTime = stopped(data) or teleported(prevData, data)

                #Bad Time
                if badTime:
                    #Good -> bad
                    if not inBad:
                        inBad = True
                        #checks to see if the original data is bad
                        if not int(data[0]) - 1 == 2:
                            steps.append((True, lastStep, int(data[0])))
                            lastStep = int(data[0])
                #Good Time
                else:
                    #bad -> good
                    if inBad:
                        inBad = False

                        steps.append((False, lastStep, int(data[0])))
                        lastStep = int(data[0])

                #updates PreviousData
                prevData = data

            #Finanlize last step
            steps.append((not inBad, lastStep, int(data[0])))

        newSteps = []
        #check for good segments:
        for step in steps:
            if step[0] and (step[2] - step[1]) >= 1000:
                newSteps.append(step)

        if len(newSteps) >= 1:
            sorties.append([file, newSteps])

#attempt to make the new directory for the segmented sorties
if not (os.path.exists(newdir)):
    os.makedirs(newdir)

#gets the name of the sorties to split
sortieNum = [i[0] for i in sorties]

#separate the sorties
for subdir, dirs, files in os.walk(rootdir):
    for sortie in files:
        #Checks to see if sortie is in
        if sortie in sortieNum:
            #allows for easy reference to find split times
            sortieSplitIndex = sortieNum.index(sortie)

            sortieSplits = sorties[sortieSplitIndex][1]

            #open the file
            with open("/"+sortie, "r") as bigFile:
                #Reads the header label
                bigFile.readline()
                #reads line without velocities
                bigFile.readline()
                #reads third line
                line = bigFile.readline()
                currLine = 3
                for split in sortieSplits:
                    startLine = split[1]
                    endLine = split[2]

                    with open(newdir+"/"+(sortie.split(".")[0])+"seg"+str(startLine)+"-"+str(endLine)+".min.tsv", "w+") as smallFile:
                        #continue copying till next timeSplit
                        while (currLine <= endLine):
                            smallFile.write(line)
                            line = bigFile.readline()
                            if not line == '':
                                currLine = currLine + 1
                            else:
                                break


