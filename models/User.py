class User:
    firstname = None
    lastname = None
    address = None
    email = None
    phone = None
    weight = None
    height = None

    def __init__(self):
        pass

    def __int__(self, firstname, lastname, address, email, phone, weight, height):
        self.firstname = firstname
        self.lastname = lastname
        self.address = address
        self.email = email
        self.phone = phone
        self.height = height
        self.weight = weight

