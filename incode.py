def parse_code(code):
    A=int(code/10000)
    B=int((code-A*10000)/1000)
    C=int((code-A*10000-B*1000)/100)
    opcode=int((code-A*10000-B*1000-C*100))
    return(A,B,C,opcode)

def read_ab(ic,i,B,C):
    a=ic[i+1] if C==1 else ic[ic[i+1]]
    b=ic[i+2] if B==1 else ic[ic[i+2]]
    return (a,b)

def Incode(ic,inn):
    output=[]
	j=0
    while i<len(ic):
        if ic[i]==99:
            break
        else:
            (A,B,C,opcode)=parse_code(ic[i])
            #print(f'opcode:{opcode},ic[i]:{ic[i]}')
            if opcode==1:
                (a,b)=read_ab(ic,i,B,C)
                if A:
                    ic[i+3]=a+b
                else:
                    ic[ic[i+3]]=a+b
                #print('a:{},b:{},a+b:{}'.format(a,b,a+b))
            elif opcode==2:
                (a,b)=read_ab(ic,i,B,C)
                if A:
                    ic[i+3]=a*b
                else:
                    ic[ic[i+3]]=a*b
                #print('a:{},b:{},a*b:{}'.format(a,b,a*b))
            elif opcode==3:
                if C:
                    ic[i+1]=inn[j]
                else:
                    ic[ic[i+1]]=inn[j]
				j+=1
                #print(f'in:{inn}, immode:{immode1,immode2,immode3},imic:{ic[i+1]},ic:{ic[ic[i+1]]}')
            elif opcode==4:
                if C:
                    output.append(ic[i+1])
                else:
                    output.append(ic[ic[i+1]])
                #print(f'out:{output}, immode:{immode1,immode2,immode3},imic:{ic[i+1]},ic:{ic[ic[i+1]]}')
            elif opcode==5:
                #if the first parameter is non-zero, it sets the instruction pointer to the value from the second parameter. Otherwise, it does nothing.
                (a,b)=read_ab(ic,i,B,C)
                if a!=0:
                    i=b
                else:
                    i+=3
                #print(f'a:{a}b:{b},C:{C},B:{B}')
            elif opcode==6:
                #if the first parameter is zero, it sets the instruction pointer to the value from the second parameter. Otherwise, it does nothing.
                (a,b)=read_ab(ic,i,B,C)
                if a==0:
                    i=b
                else:
                    i+=3
                #print(f'a:{a}b:{b},C:{C},B:{B}')
            elif opcode==7:
                #if the first parameter is less than the second parameter, it stores 1 in the position given by the third parameter. Otherwise, it stores 0.
                (a,b)=read_ab(ic,i,B,C)
                if a<b:
                    if A:
                        ic[i+3]=1
                    else:
                        ic[ic[i+3]]=1
                else: 
                    if A:
                        ic[i+3]=0
                    else:
                        ic[ic[i+3]]=0
                #print(f'a:{a}b:{b},C:{C},B:{B}')
            elif opcode==8:
                #if the first parameter is equal to the second parameter, it stores 1 in the position given by the third parameter. Otherwise, it stores 0.
                (a,b)=read_ab(ic,i,B,C)
                if a==b:
                    if A==1:
                        ic[i+3]=1
                    else:
                        ic[ic[i+3]]=1
                else: 
                    if A==1:
                        ic[i+3]=0
                    else:
                        ic[ic[i+3]]=0  
                #print(f'a:{a}b:{b},C:{C},B:{B}')
            else:
                print('error')
        if opcode in (1,2,7,8):
            i+=4
        elif opcode in (3,4):
            i+=2 
        
        #print(i)
        #print(output)
        #print('-----------------')
    return (output,ic)