import numpy as np

def parse_code(code):
    A=int(code/10000)
    B=int((code-A*10000)/1000)
    C=int((code-A*10000-B*1000)/100)
    opcode=int((code-A*10000-B*1000-C*100))
    return(A,B,C,opcode)
def get_input(filename):
    with open(filename,'r') as f:
        data=f.read()
    return data.split(',')        
def read_bc(ic,i,B,C,rb):
    if C==0:
        c=ic[ic[i+1]]
    elif C==1:
        c=ic[i+1]
    else:
        c=ic[ic[i+1]+rb]
    if B==0:
        b=ic[ic[i+2]]
    elif B==1:
        b=ic[i+2]
    else:
        b=ic[ic[i+2]+rb]
    return (b,c)
def Incode(inn,ic,i,rb):
    while i<len(ic):
        
        if ic[i]==99:
            return (99,ic,i,rb)

        else:
            (A,B,C,opcode) = parse_code(ic[i])
            (b,c) = read_bc(ic,i,B,C,rb)
            #print(f'ic[i]:{ic[i]},b:{b},c:{c},i:{i}')
            if opcode==1:
                if A==1:
                    ic[i+3]=c+b
                elif A==2:
                    ic[ic[i+3]+rb]=c+b
                else:
                    ic[ic[i+3]]=c+b
                #print('c:{},b:{},c+b:{}'.format(c,b,c+b))
            elif opcode==2:
                if A==1:
                    ic[i+3]=c*b
                elif A==2:
                    ic[ic[i+3]+rb]=c*b
                else:
                    ic[ic[i+3]]=c*b
                #print('c:{},b:{},c*b:{}'.format(c,b,c*b))
            elif opcode==3:
                if C==1:
                    ic[i+1]=inn
                elif C==2:
                    ic[ic[i+1]+rb]=inn
                else:
                    ic[ic[i+1]]=inn
                #print(f'in:{inn}, immode:{immode1,immode2,immode3},imic:{ic[i+1]},ic:{ic[ic[i+1]]}')
            elif opcode==4:
                if C==1:
                    output = ic[i+1] 
                    i+=2
                    return (output,ic,i,rb)
                elif C==2:
                    output = ic[ic[i+1]+rb]
                    i+=2
                    return (output,ic,i,rb)
                else:
                    output = ic[ic[i+1]]
                    i+=2
                    return (output,ic,i,rb)
                #print(f'out:{output}, immode:{immode1,immode2,immode3},imic:{ic[i+1]},ic:{ic[ic[i+1]]}')
            elif opcode==5:
                #if the first parameter is non-zero, it sets the instruction pointer to the value from the second parameter. Otherwise, it does nothing.
                if c!=0:
                    i=b
                else:
                    i+=3
                #print(f'c:{c}b:{b},C:{C},B:{B}')
            elif opcode==6:
                #if the first parameter is zero, it sets the instruction pointer to the value from the second parameter. Otherwise, it does nothing.
                if c==0:
                    i=b
                else:
                    i+=3
                #print(f'c:{c}b:{b},C:{C},B:{B}')
            elif opcode==7:
                #if the first parameter is less than the second parameter, it stores 1 in the position given by the third parameter. Otherwise, it stores 0.
                if c<b:
                    if A==1:
                        ic[i+3]=1
                    elif A==2:
                        ic[ic[i+3]+rb]=1
                    else:
                        ic[ic[i+3]]=1
                else: 
                    if A==1:
                        ic[i+3]=0
                    elif A==2:
                        ic[ic[i+3]+rb]=0
                    else:
                        ic[ic[i+3]]=0
                #print(f'c:{c}b:{b},C:{C},B:{B}')
            elif opcode==8:
                #if the first parameter is equal to the second parameter, it stores 1 in the position given by the third parameter. Otherwise, it stores 0.
                if c==b:
                    if A==1:
                        ic[i+3]=1
                    elif A==2:
                        ic[ic[i+3]+rb]=1
                    else:
                        ic[ic[i+3]]=1
                else: 
                    if A==1:
                        ic[i+3]=0
                    elif A==2:
                        ic[ic[i+3]+rb]=0
                    else:
                        ic[ic[i+3]]=0
                #print(f'a:{a}b:{b},C:{C},B:{B}')
            elif opcode==9:
                rb+=c
            else:
                print('error')
        if opcode in (1,2,7,8):
            i+=4
        elif opcode in (3,9):
            i+=2 
        
        #print(f'i:{i},rb:{rb}')
        #print(output)
        #print('-----------------')
    return (output,ic,i,rb)

class Robot:
    #Robot actions: 1. input from Intcode. 2. Paints 3. Turns 4. Moves
    #Stops when: input='Done'
    #Input[0]: 0=black, 1=white. Input[1]: 0=turn left, 1=turn right
    def __init__(self,start):
        #0:'up',1:'right',2:'down',3:'left'
        self.dirs={0:1,1:1,2:-1,3:-1}
        self.dir=0
        self.position=start
        return 
    
    def paint(self,inst):
        return '.' if inst==0 else '#'
    
    def move(self,inst):
        #first turn
        if inst==0:
            self.dir-=1
            if self.dir==-1:
                self.dir=3
        elif inst==1:
            self.dir+=1
            if self.dir==4:
                self.dir=0
        else:
            return False
        #then move
        if self.dir in (0,2):
            self.position['y']+=self.dirs[self.dir]
        else:
            self.position['x']+=self.dirs[self.dir]
        return True

class Computer:
    def __init__(self,ic):
        self.ic=ic+[0]*30000
        self.i=0
        self.rb=0
        return
    #Input from robot: 0 Black, 1 White
    #Output for robot: 1. designated color 2. turn left (0) or right (1)
    
    def update(self,inn):    
        (output1,self.ic,self.i,self.rb)=Incode(inn,self.ic,self.i,self.rb)
        (output2,self.ic,self.i,self.rb)=Incode(inn,self.ic,self.i,self.rb)
        return [output1,output2]

    def reset(self,ic):
        self.ic=ic
        self.i=0
        return

rast=np.full((10000,10000),'.')
IC_org=get_input('day11.txt')
IC_org = [ int(x) for x in IC_org ]
start={'x':5000,'y':5000}

robot=Robot(start)
computer=Computer(IC_org.copy())

#Input[0]: 0=black, 1=white
running=True
path=[]
while running:
    #camera reads color
    color=0 if rast[robot.position['x'],robot.position['y']]=='.' else 1
    #color is given to intcode computer to receive instructions
    instruction=computer.update(color)
    #robot paints as instructed
    rast[robot.position['x'],robot.position['y']]= robot.paint(instruction[0])
    #robot turns and moves to new position
    running=robot.move(instruction[1])
    path.append((robot.position['x'],robot.position['y']))
    
print(len(set(path)))



