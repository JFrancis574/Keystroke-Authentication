# from cryptography.fernet import Fernet

# # key = Fernet.generate_key()
# # finKey = Fernet(key)
# # print(key)

# # file = open('key.key', 'wb')
# # file.write(key)
# # file.close()

# fileName = 'Test'
# Type = '.json'

# # encFile = fileName.encode()

# # encrypted = finKey.encrypt(encFile)
# # print(str(encrypted)+'.json')

# # file = open(str(encrypted)+'.json', 'w')
# # file.write("HELLO")
# # file.close()

# key = open('key.key', 'rb')
# dtKey = key.read()
# key.close()

# finKey = Fernet(dtKey)

# data = b'gAAAAABiUW37FXeZytVb6KbMnuYHFMYF0q6bVXN2R3jfFHrWkPWaMU4R-lVr2py3A6HP4j_UbletdIQkAuxkkFrMS-IM4uG0Xg=='

# # print(finKey.decrypt(data))

# fileName = fileName.encode()
# enc = finKey.encrypt(fileName)

# file = open(str(enc)+'.json', 'r')
# print(file.read())
# file.close()


start = 2.0001
end = 2.9999
start10x = int(start*10000)
end10x = int(end*10000)+1
print(start, end, start10x, end10x)

for x in range(start10x, end10x+1):
    if x > 29000:
        print(x)

