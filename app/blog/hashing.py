from passlib.context import CryptContext


class Hash:
    __password_crypt = CryptContext(schemes=["bcrypt"], deprecated="auto")

    @classmethod
    def bcrypt(cls, password: str):
        return cls.__password_crypt.hash(password)

    @classmethod
    def verify(cls, plain_password, hashed_password):
        return cls.__password_crypt.verify(plain_password, hashed_password)
