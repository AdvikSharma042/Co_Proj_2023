import sys
#__initial function definition
def is_int(c):
    try:
        int(c)
        return 0
    except:
        return 1
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
                    print('hlt label found but not at end')
                    return 1
                else:
                    return 0 
            else:
                continue 
        elif i_set[i]=='hlt':
            if i != (len(i_set)-1):
                print('hlt cmd found but not at end')
                return 1 
            else:
                return 0 
    else:
        print('No hlt cmd was found')
        return 1     
def typo(cmd):#check if the user made a typo like typing adx instead of add etc..
    ret_val=0
    if cmd.split()[0][-1]==":":
        return ret_val 
    elif cmd.split()[0]=='var':
        return ret_val
    else:
        if cmd.split()[0] not in valid_instr:
            print(f'{cmd}:',end=' ')
            print('Invalid instruction')
            ret_val=1
    return ret_val
def oth_var_err(i_set,var_lis):#check if a var is declared twice or if it is declared somewhere in middle
    ret_val=0
    x=list(set(var_lis))
    if len(x)==len(var_lis):
        fl=False
        for i in range(len(i_set)):
            if i_set[i].split()[0]=='var' and fl==False:
                continue
            elif i_set[i].split()[0] != 'var':
                fl=True
            elif i_set[i].split()[0]=='var' and fl==True:
                   ret_val=1
                   print(f'{i_set[i]}:',end=' ')
                   print('variable was not declared in begining')
    else:
        print('Variable declared more than once')
        ret_val=1
    return ret_val                        
def undef_var(cmd,var_lis):#if user uses an undeclared variable
    ret_val=0
    if cmd.split()[0][-1]==':' or cmd.split()[0]=='var':
        return ret_val
    else:
        if valid_instr[cmd.split()[0]]["type"]=='d' and cmd.split()[-1] not in var_lis:
            print(f'{cmd}:',end=' ')
            print(f'Undefined varibale {cmd.split()[-1]}')
            ret_val=1
    return ret_val
def ill_flag(i_set):#illegal usage of flags
    ret_val=0
    for i in i_set:
        if 'FLAGS' in i.split():
            if i.split()[0] != 'mov':
                print(f'{i}:',end=' ')
                print('FLAGS register was not accessed via mov cmd')
                ret_val=1 
            else:
                if i.split()[-1] != 'FLAGS' or i.split()[1]=='FLAGS':
                    print(f'{i}:',end=' ')
                    print('FLAGS can only be read from not written in')
                    ret_val=1 
    return ret_val 
def A_op_code(cmd):#makes op code of command if it is of type A
    if len(cmd.split()) != 4:
        print(f'{cmd}: must contain 3 parameters')
        return 1 
    regs=cmd.split()[1::]
    for x in regs:
        if x not in allowed_register:
            print('invalid register')
            return 1
    else:
        opc=valid_instr[cmd.split()[0]]["opcode"]+'00'+allowed_register[regs[0]]+allowed_register[regs[1]]+allowed_register[regs[2]]
        return opc
def B_op_code(cmd):#makes op code of command if it is of type B
    if len(cmd.split()) != 3:
        print(f'{cmd}: must contain 2 parameters')
        return 1
    if cmd.split()[2][0]=='$':
        regs=cmd.split()[1]
        if regs not in allowed_register:
            print('Invalid register')
            return 1
        if is_int(cmd.split()[2][1::]):
            print('not a vaild integer')
            return 1
        else:
            if int(cmd.split()[2][1::])>127 or int(cmd.split()[2][1::])<0:
                print('Immmediate value out of range')
                return 1
            else:
                opc='00010'+'0'+allowed_register[regs]+BinaryConverter(int(cmd.split()[2][1::]))
                return opc
    else:
        regs=cmd.split()[1::]
        for x in regs:
            if x not in allowed_register:
                if is_int(cmd.split()[2]):
                    print('invalid register used')
                else:
                    print('Expected $ before immediate')
                    return 1
        else:
            opc='00011'+'00000'+allowed_register[regs[0]]+allowed_register[regs[1]]
        return opc 
def C_op_code(cmd):#makes op code of command if it is of type C
    if len(cmd.split()) != 3:
        print(f'{cmd}: must contain 2 parameters')
    regs=[cmd.split()[1],cmd.split()[2]]
    for x in regs:
        if x not in allowed_register:
            return 1
    else:
        opc=valid_instr[cmd.split()[0]]["opcode"]+'00000'+allowed_register[regs[0]]+allowed_register[regs[1]]
        return opc      
def D_op_code(cmd):#makes op code of command if it is of type D
    if len(cmd.split()) != 3:
        print(f'{cmd}: must contain 2 parameters')
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
    if len(cmd.split()) != 2:
        print(f'{cmd}: must contain 1 parameters')
    addr=cmd.split()[-1]+':'
    if addr not in mem_set:
        print(f'{cmd}: no such memory address exist')
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
f=sys.stdin.readlines()
instr_set=[]#contains every instruction in the file
variables=[] #contains every vairable
mem_set={}#contains every memory address required like that of labels or variable
line_counter=0#algo decided upon is that we convert the line number in binary
opcodes=[]#constains all the opcodes if file is error free
for i in f:#creates instr_set and mem_set
    if i=='\n':
        continue
    read_state=i.strip()
    if read_state.split()[0]=='var':
        instr_set.append(read_state)
        variables.append(read_state.split()[-1])
    else:
        if read_state.split()[0][-1]==':':
            mem_set[read_state.split()[0]]=BinaryConverter(line_counter)
            s=' '
            instr_set.append(s.join(read_state.split()[1::]))
            line_counter+=1
        else:
            instr_set.append(read_state)
            line_counter+=1
for i in range(len(variables)):#adds address of variables
    mem_set[variables[i]]=BinaryConverter(line_counter+i)
#this turns to 1 when we find an error
halt_error_check(instr_set)
flag=0
for j in instr_set:
    #typo(j)
    if typo(j)!=1:
        undef_var(j,variables)
        if undef_var==1:
            flag=1
    else:
        flag=1
oth_var_err(instr_set,variables)
ill_flag(instr_set)
if flag==1 or (halt_error_check(instr_set)+oth_var_err(instr_set,variables)+ill_flag(instr_set))>1:
    exit(0)
wr_fl=False
for cmd in instr_set:
    if cmd.split()[0] not in valid_instr:
        continue
    if op_decider(cmd)==1:
        wr_fl=True
    elif op_decider(cmd) != 1 and wr_fl==False:
        opcodes.append(op_decider(cmd))
if wr_fl==False:
    for i in  opcodes:
        print(f'{i}\n')   
