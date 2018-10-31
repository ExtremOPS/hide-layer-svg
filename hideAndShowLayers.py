#!/usr/bin/env python
# coding: utf-8

"""A simple python script that creates new SVGs with different layer visibilities in a specified folder based on a custom  XML node at layer level and its information. If this node is not present in a SVG no action will apply. 

This script enables the possibility to maintain ONE SVG and then have it easly duplicated with different layers visible.
"""

import argparse
import os
import xml.etree.ElementTree as ET

def parseArguments():
    # Create argument parser
    parser = argparse.ArgumentParser()

    # # Positional mandatory arguments
    # parser.add_argument("folder", help="PATH/TO/FOLDER/WITH/SVG", type=str)

    # Optional arguments
    parser.add_argument("-d", "--delimiter", help="Specified delimiter in xml", type=str, default=',')
    parser.add_argument("-a", "--attrName", help="Name of the added attribute in the svg file", type=str, default='exercise')
    parser.add_argument("-s", "--suffix", help="suffix that will be added", type=str, default='modLayer')
    parser.add_argument("-o", "--outputFolder", help="folder where files will be stored", type=str, default='./')
    parser.add_argument("-f", "--workingFolder", help="folder where SVG are", type=str, default='./')

    # Print version
    parser.add_argument("--version", action="version", version='%(prog)s - Version 1.0')

    # Parse arguments
    args = parser.parse_args()

    return args

class svgModifier:
    visibleLayer = 'display:inline'
    hiddenLayer = 'display:none'

    def __init__(self,argPaser):
        self.delimiter = argPaser.delimiter
        self.attributeName = argPaser.attrName
        self.outputFolder = os.path.realpath(argPaser.outputFolder)
        self.suffix = argPaser.suffix
        self.workingFolder = os.path.realpath(argPaser.workingFolder)
        self.listOfFiles = []

    def getAllFiles(self):
        for file in os.listdir(self.workingFolder):
            if file.endswith('.svg'):
                if not self.suffix in file:
                    self.listOfFiles.append(file)
    
    def getLayers(self,root,result):
        for child in root:
            if child.tag[-1] == 'g':
                result.append(child)
            self.getLayers(child, result)
        return result

    def checkAndCreateOutputFolder(self):
        if not os.path.isdir(self.outputFolder):
            os.mkdir(self.outputFolder)
    
    def getCombinations(self,layers):
        listOfCombinations = []

        for layerLocation in layers:
            exersice = layerLocation.get(self.attributeName)
            if not exersice is None:
                splitExercises = exersice.split(self.delimiter)
                for split in splitExercises:
                    if split not in listOfCombinations:
                        listOfCombinations.append(split)
        
        if 'Never' in listOfCombinations:
            listOfCombinations.remove('Never')
        if 'never' in listOfCombinations:
            listOfCombinations.remove('never')
        return listOfCombinations

    def iterateOverCombinations(self,combinations,fileName,tree,layers):
        for combination in combinations:
            newTree = tree
            for currentLayer in layers:
                attributeValue = currentLayer.get(self.attributeName)
                if attributeValue is None:
                    setValue = self.visibleLayer
                elif combination in attributeValue.split(self.delimiter):
                    setValue = self.visibleLayer
                else:
                    setValue = self.hiddenLayer

                currentLayer.set('style',setValue)
            
            newFileName = fileName[:-4] + '_' + combination + '_' + self.suffix +fileName[-4:]
            newTree.write(os.path.join(self.outputFolder,newFileName))

    def iterateOverFiles(self):
        for fileName in self.listOfFiles:
            tree = ET.parse(os.path.join(self.workingFolder,fileName))
            root = tree.getroot()
            layers = self.getLayers(root,[])
            combinations = self.getCombinations(layers)
            if combinations is not None:
                self.iterateOverCombinations(combinations,fileName,tree,layers)

    def run(self):
        self.checkAndCreateOutputFolder()
        self.getAllFiles()
        self.iterateOverFiles()

def main():
    # Parse the arguments
    args = parseArguments()

    svgJanitor = svgModifier(args)
    svgJanitor.run()

if __name__ == '__main__':    
    main()