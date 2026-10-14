





class UserAlreadyExistsException(Exception):

    def __init__(self, email:str):

        self.email = email 
        self.message = f"Пользователь с таким {email} уже существует"
        super().__init__(self.message)


class WrongLoginOrPassword(Exception):

    def __init__(self):

        self.message = "Неверный логин или пароль"
        super().__init__(self.message)