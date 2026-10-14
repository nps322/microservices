

class DocumentNotFoundError(Exception):
    def __init__(self):
        self.message = f"документ не найден"
        super().__init__(self.message)

