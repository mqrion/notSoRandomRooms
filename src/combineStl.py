import argparse
from operator import truediv
from tkinter import StringVar
import numpy
import stl
import os
import hashlib
from stl import mesh


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='combining two random stl-files of folder1 and folder 2 ',
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument(
        '-f1', '--folder1',  help='path to first folder of stl-files', required=True)
    parser.add_argument(
        '-f2', '--folder2',  help='path to second folder of stl-files', required=True)
    parser.add_argument(
        '-n', '--ntimes',  help='n files will be generated', required=True, type=int)
    parser.add_argument(
        '-d', '--destination',  help='destination for saving the combined stl', required=True)
    parser.add_argument(
        '-f1n', '--f1name',  help='full name of f1-file in output-file-name', action='store_true')
    parser.add_argument(
        '-f1all', '--allfirst',  help='all the files of the first folder', action='store_true')

    config = vars(parser.parse_args())

    for n in range(config['ntimes']):
        randomFile1 ="";
        
        firstFolder = os.listdir(config['folder1']);
        secondFolder = os.listdir(config['folder2']);
        
        if(config['allfirst']):
            randomFile1 = firstFolder[n%len(firstFolder)]
        else:
            randomFile1 = numpy.random.choice(os.listdir(config['folder1']))
        randomFile2 = numpy.random.choice(secondFolder,replace=True)
        
        mesh1 = mesh.Mesh.from_file(config['folder1']+randomFile1)
        mesh2 = mesh.Mesh.from_file(config['folder2']+randomFile2)

        combinedFileName = randomFile1[len(
        randomFile1)-25:len(randomFile1)-4]+randomFile2[len(randomFile2)-25:len(randomFile2)]
        
        if(config['f1name']):
            combinedFileName = hashlib.shake_128((randomFile1[0:len(randomFile1)-4]+randomFile1[len(randomFile2)-25:len(randomFile2)]).encode('utf-8')).hexdigest(66) +".stl"
            
        combined = mesh.Mesh(numpy.concatenate([mesh1.data, mesh2.data]))
        combined.save(config['destination']+combinedFileName, mode=stl.Mode.ASCII)
