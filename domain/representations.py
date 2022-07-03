class BadRequestResponse:
    def __init__(self, message: str):
        self.message = message


class ErrorResponse:
    def __init__(self, message: str):
        self.message = message


class SuccessResponse:
    pass
