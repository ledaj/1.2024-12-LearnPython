"""
CSV creates list of dictionnaries where you can query by field on dictionnary like a register. I have not managed to find the way to index a specific item inside. (Vlookup) I have a syntax problem I think.

PANDAS creates lists of lists aka matrices and you can Vlookup via the methods i created based on the index of a specific id. I could get rid of the box_id and use entries id and binary search them, maybe. 

ATTENTION, ne marche qu'avec du CSV US à base de commas (,) . J'ai regex mon export avec Notepad++.
"""



print('---IMPORT CSV')
import csv
csvMatrix = []

with open('Projects/LetterPosting/trash/db-mailboxes.csv', mode ='r', encoding='utf-8-sig') as file:    
     csvFile = csv.DictReader(file)
     for row in csvFile:
         csvMatrix.append(row)

# print('csvMatrix :')
# print(csvMatrix)

csvDict = {'box_id': 'M1', 'box_name': 'Mr.Green', 'box_adress': '1 Main Street', 'box_color': 'green'}
print(csvDict['box_id'])

print(csvMatrix[1]['box_id'])

# for i in csvMatrix:
#     for key in i.keys():
#         print(key)

"""for key in csvMatrix[0].keys():
    print(key)
    if key == 'box_id':
        print(csvMatrix[key])

def find(element, matrix):
    for i in range(len(matrix)):
        for key in matrix[0].keys():
            if matrix[i][key] == element:
                return (i,key)

find('M1',csvMatrix)"""


"""Numpy
print('--- IMPORT NUMPY :')
import numpy as np
npMatrix = np.genfromtxt('Projects/LetterPosting/trash/db-mailboxes.csv', delimiter=',')
print(npMatrix)
"""

"""PandasAndLists
print('--- IMPORT PANDAS :')
import pandas as pd
pdFile = pd.read_csv('Projects/LetterPosting/trash/db-mailboxes.csv')
print('print pandas :')
print(pdFile)
print('print pandaMatrix :') #C'est celle là la bonne manière de faire
pdMatrix = pdFile.values
# print(pdMatrix[1][1])

def find(element, matrix):
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            if matrix[i][j] == element:
                return (i,j)

def findBox_name(box_id, matrix):
    box_id_pos = find(box_id, matrix)[0]
    return matrix[box_id_pos,1]

def findBox_adress(box_id, matrix):
    box_id_pos = find(box_id, matrix)[0]
    return matrix[box_id_pos,2]

def findBox_color(box_id, matrix):
    box_id_pos = find(box_id, matrix)[0]
    return matrix[box_id_pos,3]

def findBox_id(element, matrix):
    box_id_pos = find(element, matrix)[0]
    return matrix[box_id_pos,0]

print('name : '+findBox_name('M2', pdMatrix))
print('adress : '+findBox_adress('M2', pdMatrix))
print('box color : '+findBox_color('M2', pdMatrix))
print('box id : '+findBox_id('Mr.Red', pdMatrix))
"""