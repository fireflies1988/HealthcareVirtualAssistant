import signin_form
import signup_form


class Readfile:
    pass


class main():

    def Writefile(key):
        try:
            with open("key.txt", 'w', encoding='utf-8') as f:
                f.write(key)
        finally:
            f.close()

    def Readfile(self):
        f = open("key.txt", 'r', encoding='utf-8')
        a = f.readline()

    def Checkfile(self):
        a = Readfile()
        if a and a.strip():
            # myString is not None AND myString is not empty or blank
            return False
            # myString is None OR myString is empty or blank
        return True
