import hashlib

f = 'клименко'


result = hashlib.md5(f.encode())

print(result.hexdigest())