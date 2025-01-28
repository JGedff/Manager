import bcrypt

class Encrypt:
    def hash(text):
        salt = bcrypt.gensalt()

        return bcrypt.hashpw(text.encode(), salt)
    
    def check(hashed_text, text):
        return bcrypt.checkpw(text.encode(), hashed_text)