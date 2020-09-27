from passlib.hash import pbkdf2_sha512


class Utils:
    @staticmethod
    def encrypt_pass(password):
        return pbkdf2_sha512.encrypt(password)

    @staticmethod
    def unencrypt_pass(password, encrypt_password):
        return pbkdf2_sha512.verify(password, encrypt_password)
