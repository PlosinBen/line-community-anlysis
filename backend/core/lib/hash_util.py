import hashlib

class hash_string:
    
    def hash_sha256(self, input_string):
        return hashlib.sha256(input_string.encode()).hexdigest()
    
    def hash_MD5(self, input_string):
        return hashlib.md5(input_string.encode()).hexdigest()