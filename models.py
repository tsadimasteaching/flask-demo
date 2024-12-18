import datetime

class User:
    def __init__(self, id, firstname, lastname, email, birth_year):
        self.id = id
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
        self.birth_year = birth_year
    
    def  __str__(self):
        return f'{self.firstname} {self.lastname}'
    
    def calc_age(self):
        return  datetime.datetime.now().year - self.birth_year
    
    @property
    def age(self):
        return self.calc_age()

