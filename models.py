import datetime

class User:
    def __init__(self, firstname, lastname, email, birth_year):
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


class Job():
    def __init__(self, name, description, user_id):
        self.name = name
        self.description = description
        self.user_id = user_id

    def __str__(self):
        return f'{self.name}'

class DBJob(Job):
    def __init__(self, id,  name, description, user_id):
        self.id = id
        self.name = name
        self.description = description
        self.user_id = user_id


class DBUser(User):
    def __init__(self, id, firstname, lastname, email, birth_year):
        self.id = id
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
        self.birth_year = birth_year

        def __str__(self):
            return f'{self.firstname} {self.lastname}'