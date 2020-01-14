import numpy as np
import pandas as pd
import math

def get_astroids(filename: str):
    astroids=[]
    with open(filename, 'r') as fp:
        line = fp.readline()
        y=1
        while line:
            x=1
            for char in line:
                if char=='#':
                    astroids.append({'x':x,'y':y})
                x+=1
            line = fp.readline()
            y+=1
    return astroids

def max_visible(astroids):
    visible={}
    i=0
    for astroid1 in astroids:    
        R=[]
        L=[]
        V=[]
        for astroid2 in astroids:
            if astroid1!=astroid2:
                if astroid2['x']-astroid1['x']<0:
                    R.append((astroid2['y']-astroid1['y'])/(astroid2['x']-astroid1['x']))
                elif astroid2['x']-astroid1['x']>0:
                    L.append((astroid2['y']-astroid1['y'])/(astroid2['x']-astroid1['x']))
                else:
                    V.append((astroid2['y']-astroid1['y'])/abs(astroid2['y']-astroid1['y']))
        visible[i]=len(set(R))+len(set(L))+len(set(V))
        i+=1
    return visible

astroids=get_astroids('day10_ex2.txt')
astroid1 = {'x': 11, 'y': 13}  
#
#astroids=[{'x':1,'y':0},{'x':1,'y':1},{'x':0,'y':1},{'x':-1,'y':1},{'x':-1,'y':0},{'x':-1,'y':-1},{'x':0,'y':-1},{'x':1,'y':-1}]
#astroid1={'x':0,'y':0}
around=pd.DataFrame(columns=['angle','distance'])
for astroid2 in astroids:
    if astroid2!=astroid1:
        dx=astroid2['x']-astroid1['x']
        dy=astroid1['y']-astroid2['y']
        s=math.sqrt((dx*dx)+(dy*dy))
        if dx<0:
            angle=360-math.degrees(math.acos(dy/s))
        else:
            angle=math.degrees(math.acos(dy/s))
        around=around.append({'angle':angle,'distance':s,'x':astroid2['x'],'y':astroid2['y']}, ignore_index=True)
around.sort_values(by='angle',inplace=True)

around['anlge','distance'].groupby('angle').min()

around.to_csv('around.csv')