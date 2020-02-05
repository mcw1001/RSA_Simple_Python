# Michael CWJ
import math
import string
import utilities

def get_RSAKey():
    name = ''
    p = 27520099
    q = 30783391
    m = 847161967875709 
    n = 847161909572220
    e = 32452999
    d = 394210268405599
    return [name,p,q,m,n,e,d]

#modified binary function to avoid unnecessary 0 padding
def dec_to_bin_RSA(decimal):
    if not isinstance(decimal,int):
        print('Error(dec_to_binary): invalid input')
        return ''
    binary = ''
    q = 1
    r = 0
    while q!=0:
        q = decimal//2
        r = decimal%2
        decimal = q
        binary = str(r)+binary
    return binary

def LRM(b,e,m):
    eBin = dec_to_bin_RSA(e)
    x = 1
    #left-to-right exponentiation
    i = ''
    for bit in eBin:
        if bit=='1':
            x = (x**2)%m
            x = (b*x)%m # b*(x^2), where x^2 is result of prev step
        else: #if bit == 0
            x = (x**2)%m
        i+=bit  #create binary string for testing, not vital
    return x

def encode_mod96(text):
    # for a letters position in the alphabet * 96, gives
    baseString = utilities.get_RSA_baseString()
    num = 0
    length = len(text)
    exp = length-1
    for i in range(length):
        num += baseString.index(text[i])*(96**exp) 
        exp-=1
    return num

def decode_mod96(num,block_size):
    #similar to dec_to_bin, but with 96
    baseString = utilities.get_RSA_baseString()
    text = ''
    q=1
    r=0
    while q!=0:
        q = num//96
        r = num%96
        num = q
        text = baseString[r] + text  #one of these is correct?
        #text+= baseString[r]
    while len(text)<block_size:
        text = 'a'+text
    return text
#LRM(b,e,m) -> b^e mod m

#LRM seems to be the problem here
# everything else should work fine
def e_RSA(plaintext,key):
    m = key[0]
    e = key[1]
# Step 1: divide text into blocks of 6 chars
    blocks = [plaintext[i*6:(i+1)*6] for i in range(math.ceil(len(plaintext)/6))]
    while len(blocks[-1]) < 6:
        blocks[-1]+='q'
##    print('step 1:',blocks)
# Step 2: Convert each block to a number using the encoding scheme
    blocks96 = [encode_mod96(block) for block in blocks]
##    print('step 2:', blocks96)
# Step 3: For each block, compute ciopher block with y = x^e mod m
    blocks96 = [LRM(block,e,m) for block in blocks96]
##    print('step 3:', blocks96)
# Step 4: Convert each block back to character stream, block size 8
# Step 5: Concat blocks to produce ciphertext
    ciphertext = ''
    for block in blocks96:
        ciphertext += decode_mod96(block,8)
    return ciphertext

def d_RSA(ciphertext,key):
    m = key[0]
    d = key[1]
# reverse order of encrypt
# Step 1: split into blocks of 8
    blocks = [ciphertext[i*8:(i+1)*8] for i in range(math.ceil(len(ciphertext)/8))]
# Step 2: Convert each block to mod 96
    blocks96 = [encode_mod96(block) for block in blocks]
# Step 3: Compute plaintext block with y = x^d mod m
    blocks96 = [LRM(block,d,m) for block in blocks96]
# Step 4 & 5: Convert each block to char stream, size 6, concat to plaintext
    plaintext = ''
    for block in blocks96:
        plaintext+=decode_mod96(block,6)
    #strip qs
    while plaintext!='' and plaintext[-1]=='q':
        plaintext = plaintext[:len(plaintext)-1]
    return plaintext
    
