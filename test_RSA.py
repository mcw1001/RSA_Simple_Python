# Michael CWJ
import RSA_encrypt

def test_RSA():
    print('Key Information:')
    key = RSA_encrypt.get_RSAKey()
    #print('name = ',key[0])
    msg = input("Enter a message to encrypt: ")
    while msg=="":
        print("Invalid input, try again.")
        msg = input("Enter a message to encrypt: ")
    p=key[1]
    print('p = ',p)
    q=key[2]
    print('q = ',q)
    m=key[3]
    print('m = ',m)
    n=key[4]
    print('n = ',n)
    e=key[5]
    print('e = ',e)
    d=key[6]
    print('d = ',d)
    print()

    plaintext = msg
    key = (m,e) # this is the public key
    ciphertext = RSA_encrypt.e_RSA(plaintext,key)
    print('Encryption using public key (m,e): ',key)
    print('-------------------------------------------------------------')
    print('Plaintext: ',plaintext)
    print('Encrypted Ciphertext: ',ciphertext)
    print()
    print()
    key = (m,d) # this is the private key
    print('Decryption using private key (m,d): ',key)
    print('-------------------------------------------------------------')
    plaintext2 = RSA_encrypt.d_RSA(ciphertext,key)
    print('Ciphertext: ', ciphertext)
    print()
    print('Decrypted Plaintext: ',plaintext2)
    print()

    return
