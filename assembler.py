#__initial function definition
def BinaryConverter(n): #use for generating memory addresses
    a=bin(n)[2::]
    if len(a)<7:
        a="0"*(7-len(a))+a
    return a
def halt_error_check(i_set):#checks for any error regarding halt statemnt, like if multiple halt statment or halt isnt at the end
    for i in range(len(i_set)):
        if i_set[i].split()[0][-1]==':':
            if i_set[i].split()[-1]=='hlt':
                if i != (len(i_set)-1):
                    return 1
                else:
                    return 0 
            else:
                continue 
        elif i_set[i]=='hlt':
            if i != (len(i_set)-1):
                return 1 
            else:
                return 0 
    else:
        return 1     
def oth_var_err(i_set,var_lis):#check if a var is declared twice or if it is declared somewhere in middle
    x=list(set(var_lis))
    if len(x)==len(var_lis):
        fl=False
        for i in range(len(i_set)):
            if i_set[i].split()[0]=='var' and fl==False:
                continue
            elif i_set[i].split()[0] != 'var':
                fl=True
            elif i_set[i].split()[0]=='var' and fl==True:
                return 1  
        else:
            return 0
    else:
        return 1               
def typo(i_set):#check if the user made a typo like typing adx instead of add etc..
    for i in i_set:
        if i.split()[0][-1]==":":
            continue 
        elif i.split()[0]=='var':
            continue 
        else:
            if i.split()[0] not in valid_instr:
                return 1 
    else: 
        return 0
def undef_var(i_set):#if user uses an undeclared variable
    for i in range(len(i_set)):
        if i_set[i].split()[0]=='var' or i_set[i].split()[0][-1]==':':
            continue
        elif valid_instr[i_set[i].split()[0]]["type"]=='d':
            if i_set[i].split()[-1] not in variables:
                return 1 
    else: 
        return 0
def variable_error(i_set,var_lis):#combines the two other functions handling error regarding variable declartion
    if oth_var_err(i_set,var_lis)==1 or undef_var(i_set)==1:
        return 1 
    else:
        return 0
def ill_flag(i_set):#illegal usage of flags
    for i in i_set:
        if 'FLAGS' in i.split():
            if i.split()[0] != 'mov':
                return 1 
            else:
                if i.split()[-1] != 'FLAGS' or i.split()[1]=='FLAGS':
                    return 1 
    else:
        return 0 
def A_op_code(cmd):#makes op code of command if it is of type A
    regs=cmd.split()[1::]
    for x in regs:
        if x not in allowed_register:
            print('invalid register')
            return 1
    else:
        opc=valid_instr[cmd.split()[0]]["opcode"]+'00'+allowed_register[regs[0]]+allowed_register[regs[1]]+allowed_register[regs[2]]
        return opc
def B_op_code(cmd):#makes op code of command if it is of type B
    reg=cmd.split()[1]
    if reg not in allowed_register:
        print('invalid register')
        return 1 
    else:
        if cmd.split()[-1]=='FLAGS':
            opc='00011'+'00000'+allowed_register[reg]+allowed_register['FLAGS']
            return opc
        elif int(cmd.split()[-1][1::])>127 or int(cmd.split()[-1][1::])<0:
            print('Invalid Immediate value')
            return 1 
        else:
            opc=valid_instr[cmd.split()[0]]["opcode"]+'0'+allowed_register[reg]+BinaryConverter(int((cmd.split()[-1][1::])))
            return opc
def C_op_code(cmd):#makes op code of command if it is of type C
    regs=[cmd.split()[1],cmd.split()[2]]
    for x in regs:
        if x not in allowed_register:
            return 1
    else:
        opc=valid_instr[cmd.split()[0]]["opcode"]+'00000'+allowed_register[regs[0]]+allowed_register[regs[1]]
        return opc      
def D_op_code(cmd):#makes op code of command if it is of type D
    addr=cmd.split()[-1]
    reg=cmd.split()[1]
    if addr not in mem_set:
        return 1 
    elif reg not in allowed_register:
        return 1
    else:
        opc=valid_instr[cmd.split()[0]]["opcode"]+'0'+allowed_register[reg]+mem_set[addr]
        return opc
def E_op_code(cmd):#makes op code of command if it is of type E
    addr=cmd.split()[-1]+':'
    if addr not in mem_set:
        return 1
    else:
        opc=valid_instr[cmd.split()[0]]["opcode"]+'0000'+mem_set[addr]
        return opc
def F_op_code(cmd):#makes op code of command if it is of type F
    return valid_instr[cmd.split()[0]]["opcode"]+'00000000000'
def op_decider(cmd):#Calls different op code makers
    if valid_instr[cmd.split()[0]]["type"]=='a':
        return A_op_code(cmd)
    if valid_instr[cmd.split()[0]]["type"]=='b':
        return B_op_code(cmd)
    if valid_instr[cmd.split()[0]]["type"]=='c':
        return C_op_code(cmd)
    if valid_instr[cmd.split()[0]]["type"]=='d':
        return D_op_code(cmd)
    if valid_instr[cmd.split()[0]]["type"]=='e':
        return E_op_code(cmd)
    if valid_instr[cmd.split()[0]]["type"]=='f':
        return F_op_code(cmd)
#__main__
#valid_instr gives type and opcodes of every valid instruction
valid_instr = {
        "add" : {"opcode" : "00000", "type" : "a"},
        "sub" : {"opcode" : "00001", "type" : "a"},
        "mov" : {"opcode" : "00010", "type" : "b"},
        "ld" : {"opcode" : "00100", "type" : "d"},
        "st" : {"opcode" : "00101", "type" : "d"},
        "mul" : {"opcode" : "00110", "type" : "a"},
        "div" : {"opcode" : "00111", "type" : "c"},
        "rs" : {"opcode" : "01000", "type" : "b"},
        "ls" : {"opcode" : "01001", "type" : "b"},
        "xor" : {"opcode" : "01010", "type" : "a"},
        "or" : {"opcode" : "01011", "type" : "a"},
        "and" : {"opcode" : "01100", "type" : "a"},
        "not" : {"opcode" : "01101", "type" : "c"},
        "cmp" : {"opcode" : "01110", "type" : "c"},
        "jmp" : {"opcode" : "01111", "type" : "e"},
        "jlt" : {"opcode" : "11100", "type" : "e"},
        "jgt" : {"opcode" : "11101", "type" : "e"},
        "je" : {"opcode" : "11111", "type" : "e"},
        "hlt" : {"opcode" : "11010", "type" : "f"}}
allowed_register = {"R0" : "000","R1" : "001", "R2" : "010" , "R3" : "011" , "R4" : "100" , "R5" : "101" , "R6" :"110", "FLAGS" : "111"}#same for registers
f=open("C:\\CO project\\assm_prog.txt","r+")
instr_set=[]#contains every instruction in the file
variables=[] #contains every vairable
mem_set={}#contains every memory address required like that of labels or variable
line_counter=0#algo decided upon is that we convert the line number in binary
opcodes=[]#constains all the opcodes if file is error free
for i in f.readlines():#creates instr_set and mem_set
    if i=="\n":
        continue 
    else:
        if i.split()[0]=='var':
            
            variables.append(i.strip().split()[-1])
            instr_set.append(i.strip())
        else:
            if i.strip().split()[0][-1]==':':
                x=i.strip().split()[1::]
                s=' '
                instr_set.append(s.join(x))
            else:
                instr_set.append(i.strip())
            line_counter+=1
            if i.split()[0][-1]==':':
                if len(i.split())==1:
                    mem_set[i.split()[0]]=BinaryConverter(line_counter+1)
                else:
                    mem_set[i.split()[0]]=BinaryConverter(line_counter)
for i in range(len(variables)):#adds address of variables
    mem_set[variables[i]]=BinaryConverter(line_counter+i+1)
#this turns to 1 when we find an error
error_flag=halt_error_check(instr_set)#now we check for different error
if error_flag==0:
    error_flag=typo(instr_set)
    if error_flag==0:
        error_flag=variable_error(instr_set,variables)
        if error_flag==0:
            error_flag=ill_flag(instr_set)
            if error_flag==0:
                for i in instr_set:
                    if i.split()[0]=='var' or i.split()[0][-1]==':':
                        continue
                    elif op_decider(i)==1:
                        print('error')
                        break
                    else:
                        opcodes.append(op_decider(i))
            else:
                print('Illegal Flag usage')#corresponding messages for errors
        else: 
            print('Variable usage error')
    else:
        print('You made a typo')
else:
    print('hlt statement error')
f.close()
F=open("C:\\CO project\\opc.txt","w+")
for i in opcodes:
    s=f'{i}\n'
    F.write(s)
F.close()