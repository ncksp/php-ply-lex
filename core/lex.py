import core.phplex as lex

lexer = None

def run(code):
    lexer = lex.get_lexer()

    lexer.input(code)
    
    while True:
        tok = lexer.token()
        if not tok:
            break
        print(tok)


def run_on_argv1():
    lex.runmain(lexer)
