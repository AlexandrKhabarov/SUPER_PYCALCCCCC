from console_app.parser import ArgumentParser

if __name__ == "__main__":
    math_expr, module = ArgumentParser.parse_arguments()
    print(math_expr, module)