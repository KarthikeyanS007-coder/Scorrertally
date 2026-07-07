# mesaages

class Messages:
    """ Messages """
    
    USER_CREATED = "User created successfully."
    USER_ALREADY_EXISTS = "User with this email already exists."
    INVALID_CREDENTIALS = "Invalid email or password."
    USER_NOT_FOUND = "User not found."
    LOGIN_SUCCESSFUL = "Login successful."
    PASSWORD_MISMATCH = "Passwords do not match."
    
for attr in dir(Messages):
    if not attr.startswith("__"):
        value = getattr(Messages, attr)
        if isinstance(value, str):
            setattr(Messages, attr, value.title())