import bcrypt

class Encrypt:
    def hash(text):
        salt = bcrypt.gensalt()

        textHashed = bcrypt.hashpw(text.encode(), salt)

        return textHashed
    
    def check(hashedText, text):
        return bcrypt.checkpw(text.encode(), hashedText)