class ExternalServiceError(Exception):
    def __init__(self, message: str, status_code: int = 502):
        self.message = message
        self.status_code = status_code
        super().__init__(message)


class BadRequestError(Exception):
    def __init__(self, message: str = "Bad Request"):
        self.message = message
        self.status_code = 400
        super().__init__(message)