import utils as u
import numpy as np

'''
Control program:
Input: movement command
north (1), south (2), west (3), and east (4). 
Output: Repair droid status
0: Wall, 1: moved, 2: location of oxygen system

'''

ic_org=u.get_input('day15.txt').split(',')
ic_org=[int(x) for x in ic_org]

i=rb=0
ic=ic_org.copy()+[0]*26000
out=[]
path=0
new_dir=1
move={1:1,2:-1,3:-1,4:1}
output=9
grid=np.empty((100,100),dtype=str)
position={'x':50,'y':50}
grid[position['x'],position['y']]='S'
j=0

for k in range(10000):
#while output != 2:
    inn=new_dir
    (output,ic,i,rb)=u.Intcode(inn,ic,i,rb)
    if output==0:
        if inn==1:
            grid[position['x'],position['y']+1]='#'
            new_dir=4
        elif inn==2:
            grid[position['x'],position['y']-1]='#'
            new_dir=3
        elif inn==3:
            grid[position['x']-1,position['y']]='#'
            new_dir=1
        else:
            grid[position['x']+1,position['y']]='#'
            new_dir=2
        #j+=1

    elif output==1:
        if inn in (3,4):
            position['x']+=move[inn]
        else: 
            position['y']+=move[inn]
        if grid[position['x'],position['y']] not in ('S','O'):
            grid[position['x'],position['y']]='.'
        if inn==1:
            new_dir=3
        elif inn==2:
            new_dir=4
        elif inn==3:
            new_dir=2
        else:
            new_dir=1
        j+=1

    elif output==2:
        if inn in (3,4):
            position['x']+=move[inn]
        else: 
            position['y']+=move[inn]
        grid[position['x'],position['y']]='O'
        if inn==1:
            new_dir=3
        elif inn==2:
            new_dir=4
        elif inn==3:
            new_dir=2
        else:
            new_dir=1
        j+=1
        '''
        if inn in (3,4):
            position['x']+=move[inn]
        else: 
            position['y']+=move[inn]
        grid[position['x'],position['y']]='O'
        print(f'oxigen tank on {position}')
        '''
    else:
        print(output)
    

    out.append([inn,output])
    
np.savetxt('day15_out.csv',grid, delimiter=',', fmt='%s')
print(grid[45:55,45:55])
