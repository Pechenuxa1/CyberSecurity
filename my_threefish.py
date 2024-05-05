import time

R = [[14, 16],
     [52, 57],
     [23, 40],
     [5, 37],
     [25, 33],
     [46, 12],
     [58, 22],
     [32, 32]]

max_int = 2 ** 64

C = 0x1BD11BDAA9FC1A22
Nw = 4
Nr = 72
pi = [0,3,2,1]

def MIX(x_0, x_1, d, j):
    y_0 = (x_0 + x_1) % max_int
    y_1 = (((x_1 << R[d % 8][j]) % (1 << 64)) | (x_1 >> (64 - R[d % 8][j]))) ^ y_0
    return y_0, y_1


key = 'key of 32,64 or 128 bytes length'
tweak = 'tweak: 16 bytes '

key_bytes = bytearray(key, 'utf-8')
tweak_bytes = bytearray(tweak, 'utf-8')


file = open('./big_plaintext.txt', 'rb')

start_time = time.time()

plaintext_bytes = bytearray(file.read())
#print(plaintext_bytes)

K = [0,0,0,0,0]
i = 0
for word in range(Nw):
    K[word] = int.from_bytes(key_bytes[i:i+8], 'little', signed=False)
    i += 8
    
T = [0,0,0]
j = 0
for word in range(2):
    T[word] = int.from_bytes(tweak_bytes[j:j+8], 'little', signed=False)
    j += 8
    
K[4] = C
for i in range(Nw):
    K[4] ^= K[i]

for i in range(2):
    T[2] ^= T[i]

Ks = []
for i in range((Nr//4)+1):
    Ks.append([0,0,0,0])    

for s in range((Nr//4)+1):
    for i in range(Nw):
        if i == 0:
            Ks[s][i] = K[(s + i) % 5]
        elif i == 1:
            Ks[s][i] = (K[(s + i) % 5] + T[s % 3]) % max_int
        elif i == 2:
            Ks[s][i] = (K[(s + i) % 5] + T[(s + 1) % 3]) % max_int
        elif i == 3:
            Ks[s][i] = (K[(s + i) % 5] + s) % max_int

c = []

###encrypt###

i = 0
while i < len(plaintext_bytes):
    P = [0,0,0,0]

    for word in range(Nw):
        if i >= len(plaintext_bytes):
            P[word] = 0
        else:
            P[word] = int.from_bytes(plaintext_bytes[i:i+8], 'little', signed=False)
        i += 8
    
    u = []
    e = []
    f = []
    for j in range(Nr + 1):
        u.append([0,0,0,0])
        e.append([0,0,0,0])
        f.append([0,0,0,0])
   
    for j in range(Nw):
        u[0][j] = P[j]
    
    for d in range(Nr):
        for j in range(Nw):
            if d % 4 == 0:
                e[d][j] = (u[d][j] + Ks[d // 4][j]) % max_int
            else:
                e[d][j] = u[d][j]
    
        for j in range(2):
            f[d][2*j], f[d][(2*j)+1] = MIX(e[d][2*j], e[d][(2*j)+1], d, j)
    
        for j in range(Nw):
            u[d+1][j] = f[d][pi[j]]
    
    for j in range(Nw):
        c.append((u[72][j] + Ks[72//4][j]) % max_int)
        
    
    len_c = len(c) 
    #print(c[len_c - 4].to_bytes(8, 'little') + c[len_c - 3].to_bytes(8, 'little') + c[len_c - 2].to_bytes(8, 'little') + c[len_c - 1].to_bytes(8, 'little'))
    

def deMIX(y_0, y_1, d, j):
    y_1 ^= y_0
    x_1 = ( ((y_1 << (64 - R[d % 8][j]))  % (1 << 64)) | ((y_1 >> R[d % 8][j])) )                     
    x_0 = (y_0 - x_1) % max_int
    return x_0, x_1

###decrypt###

k = 0
while k < len(c):
    for i in range(Nw):
        u[72][i] = (c[k] - Ks[72//4][i]) % max_int
        k += 1

    for d in range(Nr, 0, -1):
    
        for i in range(Nw):
            f[d-1][pi[i]] = u[d][i]
    
        for j in range(2):
            e[d-1][2*j], e[d-1][(2*j)+1] = deMIX(f[d-1][2*j], f[d-1][(2*j)+1], d-1, j)
        
        for i in range(Nw):
            if (d-1) % 4 == 0:
                u[d-1][i] = (e[d-1][i] - Ks[(d-1) // 4][i]) % max_int
            else:
                u[d-1][i] = e[d-1][i]

    for i in range(Nw):
        P[i] = u[0][i]
    
    #print(P[0].to_bytes(8, 'little') + P[1].to_bytes(8, 'little') + P[2].to_bytes(8, 'little') + P[3].to_bytes(8, 'little'))

end_time = time.time()

print(str(end_time - start_time) + ' seconds')
