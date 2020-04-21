def error(pos, message):
    raise Exception(f"ERROR: At {pos}, Message: {message}")


def parser_error(token, message):
    raise Exception(f"ERROR: {token.pos} at '{token.lexeme}' {message}")


def runtime_error(operator, message):
    raise Exception(f"ERROR: {message}")
