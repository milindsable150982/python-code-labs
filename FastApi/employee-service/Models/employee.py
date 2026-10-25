class Employee:
    def __init__(self, id, firstname, lastname, address, state, zip, country, position, salary):
        self.__id = id
        self.__firstname = firstname
        self.__lastname = lastname
        self.__address = address
        self.__state = state
        self.__zip = zip
        self.__country = country  
        self.__position = position
        self.__salary = salary


    def get_id(self):
        return self.__id

    def set_id(self, id):
        self.__id = id

    def get_name(self):
        return self.__firstname + " " + self.__lastname

    def set_name(self, firstname, lastname):
        self.__firstname = firstname
        self.__lastname = lastname

    def get_address(self):
        self.__address + ", " + self.__state + " " + self.__zip + ", " + self.__country

    def set_address(self, address, state, zip, country):
        self.__address = address
        self.__state = state
        self.__zip = zip
        self.__country = country

    def get_position(self):
        return self.__position

    def set_position(self, position):
        self.__position = position

    def get_salary(self):
        return self.__salary

    def set_salary(self, salary):
        self.__salary = salary