from FilteredLexer import FilteredLexer
import phplex as lex

lexer = None

def run(code):
    lexer = FilteredLexer(lex.get_lexer())

    lexer.input(code)
    
    while True:
        tok = lexer.token(lex.unparsed)
        if not tok:
            break
        print(tok)


def run_on_argv1():
    lex.runmain(lexer)
