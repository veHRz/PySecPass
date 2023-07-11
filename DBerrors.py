class PasswordError(Exception):
    def __init__(self, error_message: str = "Error: The password is wrong."):
        super().__init__(error_message)

class FatalError(Exception):
    def __init__(self, error_message: str = "Fatal Error: Unknown error message."):
        super().__init__(error_message)