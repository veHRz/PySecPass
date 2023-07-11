from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import hashlib, json, secrets
from DBerrors import *
class DataBase:
    def __init__(self, __filePath: str = "database.db", __password: str = "password"):
        self.__defaultData = {"infos": {"APIversion": "1.0.0"}, "accounts": [], "password": self.toSha256(__password, True)}
        self.__filePath: str = __filePath
        self.__cipherType = AES.MODE_CBC
        self.__datas: dict = {}
        self.__key: str = self.toSha256(__password, True)
        self.__verifyPassword()
    def createNewDatabase(self, __filePath: str, __password: str | None = "password"):
        self.__data = self.__defaultData
        if __password is not None:
            self.__key =self.toSha256(__password, True)
        self.saveDatabase()
    def __preLoad(self) -> None:
        try:
            self.__loadDatabase()
        except FileNotFoundError:
            self.createNewDatabase(self.__filePath, None)
        except Exception:
            raise PasswordError(f"""Error: The password is wrong.""")
    def __verifyPassword(self) -> None:
        self.__preLoad()
        if not secrets.compare_digest(self.__key, self.__password) :
            raise PasswordError(f"""Error: The password is wrong.""")
    @staticmethod
    def __verifyIfIsType(__value, __type: type) -> None:
        if not isinstance(__value, __type):
            raise TypeError(f"Error: {__value} should be a {__type}.")
    @property
    def __data(self) -> dict:
        return self.__datas
    @__data.setter
    def __data(self, __value: dict) -> None:
        self.__datas = __value
        #self.saveDatabase()
    @property
    def infos(self) -> dict:
        return self.__data["infos"]
    @infos.setter
    def infos(self, __info: tuple) -> None:
        __infoName, __infoData = __info
        self.__data["infos"][__infoName] = __infoData
        self.saveDatabase()
    @property
    def __password(self) -> str:
        return self.__data["password"]
    @__password.setter
    def __password(self, __pasword: str) -> None:
        self.__data["password"] = self.toSha256(__pasword, True)
        self.__key = self.toSha256(__pasword, True)
        self.saveDatabase()
    @property
    def currentAccounts(self) -> list:
        return self.__data["accounts"]
    def addAccount(self, newTitle: str = None, newUsername: str = None, newPassword: str = None, newUrl: str = None, newNote: str = None) -> bool:
        self.currentAccounts.append([newTitle, newUsername, newPassword, newUrl, newNote])
        return True
    def modifyAccount(self, idAccount: int, newTitle: str = None, newUsername: str = None, newPassword: str = None, newUrl: str = None, newNote: str = None) -> bool:
        if len(self.currentAccounts) <= idAccount:
            return False
        if newTitle is not None:
            self.currentAccounts[idAccount][0] = newTitle
        if newUsername is not None:
            self.currentAccounts[idAccount][1] = newUsername
        if newPassword is not None:
            self.currentAccounts[idAccount][2] = newPassword
        if newUrl is not None:
            self.currentAccounts[idAccount][3] = newUrl
        if newNote is not None:
            self.currentAccounts[idAccount][4] = newNote
        return True
    def removeAccount(self, __idAccount: int) -> bool:
        if len(self.currentAccounts) <= __idAccount:
            return False
        self.currentAccounts.pop(__idAccount)
        return True
    def getAccount(self, __idAccount: int) -> list:
        if len(self.currentAccounts) <= __idAccount:
            raise ValueError(f"Error: The account '{__idAccount}' doesn't exist.")
        return self.currentAccounts[__idAccount]
    def __loadDatabase(self) -> None:
        with open(self.__filePath, 'rb') as __file:
            __iv = __file.read(16)
            __decrypt_data = __file.read()
        __tempKey = "".join([self.__key[i] for i in range(0, len(self.__key), 2)]).encode("utf-8")
        __cipher = AES.new(__tempKey, self.__cipherType, iv=__iv)
        self.__data = json.loads(unpad(__cipher.decrypt(__decrypt_data), AES.block_size).decode("utf-8"))
    def saveDatabase(self) -> None: 
        __dataStr = json.dumps(self.__data).encode("utf-8")
        __tempKey = "".join([self.__key[i] for i in range(0, len(self.__key), 2)]).encode("utf-8")
        __cipher = AES.new(__tempKey, self.__cipherType)
        with open(self.__filePath, 'wb') as __file:
            __file.write(__cipher.iv)
            __file.write(__cipher.encrypt(pad(__dataStr, AES.block_size)))
    @staticmethod
    def toSha256(__string: str, __convert_return_to_string: bool = False) -> bytes | str:
        """
        This function encrypt with the sha256 algorithm the string given in parameters.
        :param __string: A string to encrypt using sha256 algorithm.
        :param __convert_return_to_string: True or False that the return will be convert to string.
        :return: Return the encrypted string.
        """
        if __convert_return_to_string:
            return hashlib.sha256(__string.encode('utf-8')).hexdigest()
        return hashlib.sha256(__string.encode('utf-8')).hexdigest().encode('utf-8')
    def changePassword(self, __oldPassword: str, __newPassword: str) -> None:
        if secrets.compare_digest(self.toSha256(__oldPassword, True), self.__password):
            self.__password = __newPassword
        else:
            raise PasswordError(f"""Error: The password is wrong.""")

if __name__ == "__main__":
    try:
        db = DataBase("database.db", "password")
        print(db.currentAccounts)
        #db.addAccount("google.com", "google", "password")
        #db.modifyAccount(0, newSite="google.com",newPassword="idk")
        #print(db.currentAccounts)
        db.saveDatabase()
    except Exception as e:
        print(e)
