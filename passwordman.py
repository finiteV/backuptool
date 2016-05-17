class PasswordMan:
    def __init__(self,printable):
        self.printable = printable
        
    def keygen(self,salt,a1,q):
        import hashlib
        key = salt
        sha = hashlib.sha1()
        sha.update(key)
        key = sha.hexdigest()

        return self.translate(key,a1,q)
    
    def translate(self,key,a1,q):

        nkey = key
        n = 1 + (len(key)-a1)/q
        if n>len(self.printable):
            n = len(self.printable)

        for i in range(1,n+1):
            ai = a1+q*(i-1)
            nkey = nkey.replace(key[ai-1], self.printable[i-1])
               
        return nkey

if __name__=="__main__":
    key1 = 'aaaaaaaaaaaaaaaaaa'
    printable = '!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!'
    a1 =3
    q=3        
    PwdMan = PasswordMan(printable)
    print key1,'\n',PwdMan.keygen(key1,a1,q)