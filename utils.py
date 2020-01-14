import numpy as np

def get_input(filename):
    with open(filename,'r') as f:
        data=f.read()
    return data

def get_input_as_list(filename):
    with open(filename,'r') as f:
        data=f.read()
    return [data]

def parse_code(code):
    A=int(code/10000)
    B=int((code-A*10000)/1000)
    C=int((code-A*10000-B*1000)/100)
    opcode=int((code-A*10000-B*1000-C*100))
    return(A,B,C,opcode)

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

def Intcode(inn,ic,i,rb):
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

def get_grid(ic_org):
	i=rb=0
	ic=ic_org+[0]*26000
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
		(output,ic,i,rb)=Intcode(inn,ic,i,rb)
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

	return grid

class Acii:
    def __init__(self,ic):
        self.i=0
        self.rb=0
        self.ic=ic+[0]*26000
        self.queue=[]

    def addqueue(self,inn):
        self.queue=self.queue+inn
    
    def update(self):
        k=0
        output=[]
        while self.i<len(self.ic):
            if self.ic[self.i]==99:
                return output+[99]
            else:
                (A,B,C,opcode) = parse_code(self.ic[self.i])
                (b,c) = read_bc(self.ic,self.i,B,C,self.rb)
                if opcode==1:
                    if A==1:
                        self.ic[self.i+3]=c+b
                    elif A==2:
                        self.ic[self.ic[self.i+3]+self.rb]=c+b
                    else:
                        self.ic[self.ic[self.i+3]]=c+b
                elif opcode==2:
                    if A==1:
                        self.ic[self.i+3]=c*b
                    elif A==2:
                        self.ic[self.ic[self.i+3]+self.rb]=c*b
                    else:
                        self.ic[self.ic[self.i+3]]=c*b
                elif opcode==3:
                    if self.queue==[]:
                        
                        return ['give input']            
                    else:
                        inn=self.queue[0]
                        self.queue=self.queue[1:]
                        if C==1:
                            self.ic[self.i+1]=inn
                        elif C==2:
                            self.ic[self.ic[self.i+1]+self.rb]=inn
                        else:
                            self.ic[self.ic[self.i+1]]=inn
                    
                elif opcode==4:
                    if C==1:
                        output.append(self.ic[self.i+1])
                        #self.i+=2
                        #return output
                    elif C==2:
                        output.append(self.ic[self.ic[self.i+1]+self.rb])
                        #self.i+=2
                        #return output
                    else:
                        output.append(self.ic[self.ic[self.i+1]])
                    #k+=1
                        #self.i+=2
                        #return output
                elif opcode==5:
                    if c!=0:
                        self.i=b
                    else:
                        self.i+=3
                elif opcode==6:
                    if c==0:
                        self.i=b
                    else:
                        self.i+=3
                elif opcode==7:
                    if c<b:
                        if A==1:
                            self.ic[self.i+3]=1
                        elif A==2:
                            self.ic[self.ic[self.i+3]+self.rb]=1
                        else:
                            self.ic[self.ic[self.i+3]]=1
                    else: 
                        if A==1:
                            self.ic[self.i+3]=0
                        elif A==2:
                            self.ic[self.ic[self.i+3]+self.rb]=0
                        else:
                            self.ic[self.ic[self.i+3]]=0
                elif opcode==8:
                    if c==b:
                        if A==1:
                            self.ic[self.i+3]=1
                        elif A==2:
                            self.ic[self.ic[self.i+3]+self.rb]=1
                        else:
                            self.ic[self.ic[self.i+3]]=1
                    else: 
                        if A==1:
                            self.ic[self.i+3]=0
                        elif A==2:
                            self.ic[self.ic[self.i+3]+self.rb]=0
                        else:
                            self.ic[self.ic[self.i+3]]=0
                elif opcode==9:
                    self.rb+=c
                else:
                    return 'error'
            if opcode in (1,2,7,8):
                self.i+=4
            elif opcode in (3,4,9):
                self.i+=2 
            if len(output)>0 and output[-1]==10:
                return output
            #print(f'opcode:{opcode},i:{i},inn:{inn},output:{output}')
        return 'error'

def ascii_to_txt(code):
    txt=''
    for x in code:
        txt+=chr(x)
    return txt