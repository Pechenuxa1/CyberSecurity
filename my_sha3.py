rate=1088
c=512
b = 1600
n = 24
RC =[0x0000000000000001,
     0x0000000000008082,
     0x800000000000808A,
     0x8000000080008000,
     0x000000000000808B,
     0x0000000080000001,
     0x8000000080008081,
     0x8000000000008009,
     0x000000000000008A,
     0x0000000000000088,
     0x0000000080008009,
     0x000000008000000A,
     0x000000008000808B,
     0x800000000000008B,
     0x8000000000008089,
     0x8000000000008003,
     0x8000000000008002,
     0x8000000000000080,
     0x000000000000800A,
     0x800000008000000A,
     0x8000000080008081,
     0x8000000000008080,
     0x0000000080000001,
     0x8000000080008008]

r = [[0,    36,     3,    41,    18],
      [1,    44,    10,    45,     2],
      [62,    6,    43,    15,    61],
      [28,   55,    25,    21,    56],
      [27,   20,    39,     8,    14]]


def rot(X, offset):
  return (((X << offset) % (1 << 64)) | (X >> (64 - offset)))


def Round(A, RC):

  C = [0,0,0,0,0]
  for x in range(5):
    C[x] = (A[x][0] ^ A[x][1] ^ A[x][2] ^ A[x][3] ^ A[x][4])

  D = [0,0,0,0,0]
  for x in range(0, 5):
    D[x] = C[(x - 1) % 5] ^ rot(C[(x + 1) % 5], 1)
  for x in range(0, 5):
    for y in range(0, 5):
      A[x][y] ^= D[x]

  B = []
  for i in range(5):
    row = [0] * 5
    B.append(row)

  for x in range(5):
    for y in range(5):
      B[y][(2*x+3*y)%5] = rot(A[x][y], r[x][y])

  for x in range(0, 5):
    for y in range(0, 5):
      A[x][y] = B[x][y] ^ ((~B[(x+1)%5][y]) & B[(x+2)%5][y])

  A[0][0] ^= RC

  return A

def Keccak(A):
  for i in range(0, n):
    A = Round(A, RC[i])
  return A

file = open('drive/MyDrive/Colab Notebooks/input.txt', 'rb')
message = bytearray(file.read())

padding = rate - ((len(message) * 8) % rate)

if padding == 8:
  message.append(0x86)
else:
  message.append(0x06)
  while (((len(message) * 8) % rate) != (rate - 8)):
    message.append(0x00)
  message.append(0x80)

n_blocks = int((len(message) * 8) / rate)

S = []
for _ in range(5):
  row = [0] * 5
  S.append(row)

block = []
for _ in range(5):
  row = [0] * 5
  block.append(row)

start = 0
step = 8
for x in range(0, n_blocks):
  start = x * (rate // 8)

  for i in range(5):
    for j in range(5):
      if (start == ((x+1) * (rate // 8))):
        block[j][i] = 0
      else:
        block[j][i] = int.from_bytes(message[start:start+8], "little", signed=False)
        start += 8

  for y in range(5):
    for z in range(5):
      S[y][z] ^= block[y][z]
  S = Keccak(S)

print(str(S[0][0].to_bytes(8,'little').hex()) + str(S[1][0].to_bytes(8,'little').hex()) + str(S[2][0].to_bytes(8,'little').hex()) + str(S[3][0].to_bytes(8,'little').hex()))
