

class MovieAlreadyExistsError(Exception):

    def __init__(self, title:str):

        self.title = title
        self.message = f"фильм с таким {title} уже существует"
        super().__init__(self.message)


class DirectorNotFoundError(Exception):
    def __init__(self):
        self.message = f"такого режисёра не существует"
        super().__init__(self.message)

