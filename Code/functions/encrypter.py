from Crypto.Cipher import AES, ChaCha20

class LockerError(Exception):
    pass
      

def encrypt(x, key, iv, filebytes = None):
    
    if filebytes == None:
        key = key_convert_AES(key)
        cipher = AES.new(key, AES.MODE_CBC, iv = iv)
        
        if '~' in x:
            raise LockerError("Text cannot contain '~'")
            
        x = [x[i:i+16] for i in range(0, len(x), 16)]
        encrypted = []
        for piece in x:
            piece = bytearray(piece, "utf-8")
            
            if len(piece) < 16:
                to_add = 16 - len(piece)
                for i in range(0, to_add):
                    piece += bytearray('~', 'utf-8')
                    
            piece = bytes(piece)
            piece = cipher.encrypt(piece)
            encrypted.append(piece)

    else:
        key = key_convert_ChaCha(key)
        cipher = ChaCha20.new(key = key, nonce = b'This is lock')
        
        encrypted = cipher.encrypt(filebytes)
        
    return encrypted


def decrypt(x, key, iv, filebytes = None):
    
    if filebytes == None:
        key = key_convert_AES(key)
        
        cipher = AES.new(key, AES.MODE_CBC, iv = iv)
        decrypted = ""
        
        for part in x:
            try:
                text = cipher.decrypt(part).decode()
            except:
                return 0
        
            if text.endswith('~'):
                text = text[0:int(text.index('~'))]
                
            decrypted += text
    
    else:
        key = key_convert_ChaCha(key)
        cipher = ChaCha20.new(key = key, nonce = b'This is lock')
        
        decrypted = cipher.decrypt(filebytes)
        
    return decrypted



def key_convert_AES(key):
    
    if len(key) > 32:
        key = key[:32]
        
    if len(key) < 16:
        to_add = 16 - len(key)
        
        pos = -1
        for i in range(0, to_add):
            pos += 1
            try:
                key += key[pos]
            except IndexError:
                pos = 0
                key =+ key[pos]
                
    else:
        # Below calculations are done so that the whole key has contribution in the AES key created
        # even if the key is longer than 16 characters. (AES-128 key is always 16 chars.)
        x = 32 - len(key)
        key = key[:x] + key[x+1::2]
    
    key = bytes(key, "utf-8")
    return key



def key_convert_ChaCha(key):
    
    if len(key) < 32:
        to_add = 32 - len(key)
        
        pos = -1
        for i in range(0, to_add):
            pos += 1
            try:
                key += key[pos]
            except IndexError:
                pos = 0
                key =+ key[pos]
                
    else:
        key = key[:32]
    
    key = bytes(key, "utf-8")
    return key