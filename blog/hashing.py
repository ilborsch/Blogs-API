from passlib.context import CryptContext


class Hash:
    __password_encryptor = CryptContext(schemes=["bcrypt"], deprecated="auto")

    @classmethod
    def bcrypt(cls, password: str):
        return cls.__password_encryptor.hash(password)