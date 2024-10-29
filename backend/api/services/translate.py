import Crypto.Cipher.AES
import Crypto.Random
import base64
import binascii

class Cipher_AES:
  pad_default = lambda x, y: x + (y - len(x) % y) * " ".encode("utf-8")
  unpad_default = lambda x: x.rstrip()
  pad_user_defined = lambda x, y, z: x + (y - len(x) % y) * z.encode("utf-8")
  unpad_user_defined = lambda x, z: x.rstrip(z)
  pad_pkcs5 = lambda x, y: x + (y - len(x) % y) * chr(y - len(x) % y).encode("utf-8")
  unpad_pkcs5 = lambda x: x[:-ord(x[-1])]
  
  def __init__(self, key, iv):
    self.__key = key
    self.__iv = iv
    
  def Cipher_MODE_ECB(self):
    self.__x = Crypto.Cipher.AES.new(self.__key.encode("utf-8"), Crypto.Cipher.AES.MODE_ECB)
  
  def Cipher_MODE_CBC(self):
    self.__x = Crypto.Cipher.AES.new(self.__key.encode("utf-8"), Crypto.Cipher.AES.MODE_CBC, self.__iv.encode("utf-8"))
  
  def encrypt(self, text, cipher_method, pad_method="", code_method=""):
    if cipher_method.upper() == "MODE_ECB":
      self.Cipher_MODE_ECB()
    elif cipher_method.upper() == "MODE_CBC":
      self.Cipher_MODE_CBC()
    cipher_text = b"".join([self.__x.encrypt(i) for i in self.text_verify(text.encode("utf-8"), pad_method)])
    if code_method.lower() == "base64":
      return base64.encodebytes(cipher_text).decode("utf-8").rstrip()
    elif code_method.lower() == "hex":
      return binascii.b2a_hex(cipher_text).decode("utf-8").rstrip()
    else:
      return cipher_text.decode("utf-8").rstrip()
  
  def decrypt(self, cipher_text, cipher_method, pad_method="", code_method=""):
    if cipher_method.upper() == "MODE_ECB":
      self.Cipher_MODE_ECB()
    elif cipher_method.upper() == "MODE_CBC":
      self.Cipher_MODE_CBC()
    if code_method.lower() == "base64":
      cipher_text = base64.decodebytes(cipher_text.encode("utf-8"))
    elif code_method.lower() == "hex":
      cipher_text = binascii.a2b_hex(cipher_text.encode("utf-8"))
    else:
      cipher_text = cipher_text.encode("utf-8")
    return self.unpad_method(self.__x.decrypt(cipher_text).decode("utf-8"), pad_method)
  
  def text_verify(self, text, method):
    while len(text) > len(self.__key):
      text_slice = text[:len(self.__key)]
      text = text[len(self.__key):]
      yield text_slice
    else:
      if len(text) == len(self.__key):
        yield text
      else:
        yield self.pad_method(text, method)
  
  def pad_method(self, text, method):
    if method == "":
      return Cipher_AES.pad_default(text, len(self.__key))
    elif method == "PKCS5Padding":
      return Cipher_AES.pad_pkcs5(text, len(self.__key))
    else:
      return Cipher_AES.pad_user_defined(text, len(self.__key), method)
  
  def unpad_method(self, text, method):
    if method == "":
      return Cipher_AES.unpad_default(text)
    elif method == "PKCS5Padding":
      return Cipher_AES.unpad_pkcs5(text)
    else:
      return Cipher_AES.unpad_user_defined(text, method)

def translate(key, text, operation):
    iv = key
    cipher_method = "MODE_CBC"
    pad_method = "PKCS5Padding"
    code_method = "base64"
    try:
      cipher_text = Cipher_AES(key, iv).encrypt(text, cipher_method, pad_method, code_method)
    except:
      return -1
    
    if operation == 'encrypt':
      try:
        encrypt = cipher_text.replace('\n','')
        return ('![' + encrypt + ']')
      except:
        return -1
    else:
      try:
        decrypt = Cipher_AES(key, iv).decrypt(text, cipher_method, pad_method, code_method)
        return (decrypt)
      except:
        return -1