import sys

x = []
for i in sys.stdin:
    x.append(i)

mem = []

def ieee_754(op_code):
    req_num=op_code.split()[-1][1::]
    req_num=float(req_num)
    int_part=int(req_num)
    frac_part=req_num-int_part
    binary=''
    precision=5
    while (precision):
        frac_part *= 2
        bit = int(frac_part)
        if (bit == 1) :   
            frac_part -= bit  
            binary += '1'
        else : 
            binary += '0'
        precision -= 1
    binary=bin(int_part)[2::]+'.'+binary
    point_index=binary.index('.')
    exp=bin(point_index+2)[2::]
    exp=exp[0:3]
    if len(exp)<3:
        exp=(3-len(exp))*'0'+exp
    binary=(binary[0:point_index]+binary[point_index+1::])[0:5]
    ans=exp+binary
    return ans
# print(ieee_754('mov r1 $54.766'))
for j in range(len(mem), 128):
    mem.append("0"*16)

#opcode
A = ['00000','00001','00110','01010','01011','01100'],
B = ['00010', '01000', '01001']
C = ['00011', '00111', '01110', '01101']
D = ['00100', '00101']
E = ['01111','11100','11101','11111']
F = ['11010']
str_mem=[]
# Registers
reg = {"000": "0000000000000000", "001": "0000000000000000", "010": "0000000000000000", "011": "0000000000000000", "100": "0000000000000000", "101": "0000000000000000", "110": "0000000000000000" ,"111":"0000000000000000"}

i = 0

while(i < len(x)):
    c=x[i][0:5]
    if c in A :
        p = x[i][7:10]
        q = x[i][10:13]
        r = x[i][13:16]
        if c=="00000":
            p1 = int(p,2)
            q1 = int(q,2)
            r1 = int(r,2)
            p1 = q1 + r1
            if p1 > (2 ** 7 - 1):
                p1 = 65535
                reg[111] = '0000000000001000'
            p1 = bin(p1).replace("0b","")
            p1 = p1.zfill(16)
            reg[x[i][7:10]] = p1
        if (c == '00001'):
            p1 = int(p,2)
            q1 = int(q,2)
            r1 = int(r,2)
            p1 = q1 - r1
            if (r1 > q1):
                p1 = 0
                reg["111"] = '0000000000001000'
            else:
                p1 = q1 - r1
            p1 = bin(p1).replace("0b","")
            p1 = p1.zfill(16)
            reg[x[i][7:10]] = p1
        if (c == '00110'):
            p1 = int(p,2)
            q1 = int(q,2)
            r1 = int(r,2)
            p1 = q1 * r1
            if p1 > (2 ** 7 - 1):
                p1 = 65535
                reg["111"] = '0000000000001000'
            p1 = bin(p1).replace("0b","")
            p1 = p1.zfill(16)
            reg[x[i][7:10]] = p1
        if c == '01010':
            p1 = int(p,2)
            q1 = int(q,2)
            r1 = int(r,2)
            p1 = q1 ^ r1
            if p1 > (2 ** 7 - 1):
                p1 = 65535
                reg["111"] = '0000000000001000'
            p1 = bin(p1).replace("0b","")
            p1 = p1.zfill(16)
            reg[x[i][7:10]] = p1
        if (c == '01011'):
                p1 = int(p,2)
                q1 = int(q,2)
                r1 = int(r,2)
                p1 = q1 | r1
                if p1 > (2 ** 7 - 1):
                    p1 = 65535
                    reg["111"] = '0000000000001000'
                p1 = bin(p1).replace("0b","")
        if (c == '01100'):
            p1 = int(p,2)
            q1 = int(q,2)
            r1 = int(r,2)
            p1 = q1 & r1
            if p1 > (2 ** 7 - 1):
                p1 = 65535
                reg["111"] = '0000000000001000'
            p1 = bin(p1).replace("0b","")
            p1 = p1.zfill(16)
            reg[x[i][7:10]] = p1
    if c in B:
        if (c == "00010"):
            reg[111] = '0000000000000000'
            p = x[i][6:9]
            q=  x[i][9:16]
            q=q.zfill(16)
            reg[p]= q
        if (c == "01000"):
            reg[111] = '0000000000000000'
            p = int(reg[x[i][6:9]])
            p1 = bin(p).replace("0b","")
            r1 = bin(x[i][9:16]).replace("0b","")
            a = p1 >> r1
            a = int(a,2)
            a = a.zfill(16)
            reg[x[i][6:9]]=a
        if (c == "01001"):
            reg[111] = '0000000000000000'
            p = int(reg[x[i][6:9]])
            p1 = bin(p).replace("0b","")
            r1 = bin(x[i][9:16]).replace("0b","")
            a = p1 << r1
            a = int(a,2)
            a = a.zfill(16)
            reg[x[i][6:9]]=a
    if c in C:
        if (c == '00011'):
            if (x[i][13:16] != '111'):
                reg[111] = '0000000000000000'
            p1 = int(reg[x[i][10:13]])
            q1 = int(reg[x[i][13:16]])
            reg[x[i][10:13]] = reg[x[i][13:16]]
        if (c == '00111'):
            reg["111"] = '0000000000000000'
            p2 = bin(int(x[i][10:13])).replace("0b","")
            q2 = bin(int(x[i][13:16])).replace("0b","")
            r = p2 // q2
            y = p2 % q2
            r = int(r,2)
            y = int(y,2)
            y = y.zfill(16)
            reg["000"] = y
            r = r.zfill(16)
            reg["001"] = r
        if (c == '01101'):
            reg["111"] = '0000000000000000'
            q1 = reg[x[i][13:16]]
            q2 = ""
            for i in q1:
                if i == '0':
                    q2 += '1'
                elif i == '1':
                    q2 += '0'
            reg[x[i][10:13]] = q2
        if (c == '01110'):
            reg[111] = '0000000000000000'
            p1 = (reg[x[i][10:13]])
            q1 = (reg[x[i][13:16]])
            p2 = int(p1,2)
            q2 = int(q1,2)
            if (p2 > q2):
                reg["111"] = '0000000000000010'
            elif (p2 < q2):
                reg["111"] = '0000000000000100'
            elif (p2 == q2):
                reg["111"] = '0000000000000001'
    if c in D:
        if (c == '00101'):
            reg["111"] = '0000000000000000'
            q = (x[i][9:16])
            p1 = reg[x[i][6:9]]
            q1 = int(q,2)
            mem[q1-len(x)] = p1
        if (c == '00100'):
            reg["111"] = '0000000000000000'
            p = x[i][9:16]
            p1 = int(p,2)
            reg[x[i][6:9]] = mem[p1]
    if c in E:
        if (c == '01111'):
            p = x[i][9:16]
            p1 = int(p,2)
            p2 = p1
            p2 = bin(p1).replace("0b","")
            p2 = p2.zfill(16)
            i = p1
        elif c == '10000':
            if reg["111"] == '0000000000000100':
                reg["111"] = '0000000000000000'
            p = x[i][9:16]
            p1 = int(p,2)
            p2 = p1
            p2 = bin(p1).replace("0b","")
            p2 = p2.zfill(16)
            i = p1
        else:
            reg["111"] = '0000000000000000'
            i += 1
        if c == '10001':
            if reg["111"] == '0000000000000010':
                reg["111"] = '0000000000000000'
            p = x[i][9:16]
            p1 = int(p,2)
            p2 = p1
            p2 = bin(p2).replace("0b","")
            p2 = p2.zfill(16)
            i = p1
        else:
            reg["111"] = '0000000000000000'
            i += 1
    j=i
    j=bin(j).replace("0b","")
    j=j.zfill(7)
    print(j+"        "+ reg["000"] + " " + reg["001"] + " " + reg["010"] + " "+ reg["011"] + " " + reg["100"] +" " +reg["101"] + " " + reg["110"] + " " + reg["111"] )
    
    i += 1
    if c in F:
        break



for i in x:
    print(i)
for i in range(len(mem)-len(x)):
    print(mem[i])
