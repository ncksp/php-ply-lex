class FilteredLexer(object):
    def __init__(self, lexer):
        self.lexer = lexer
        self.last_token = None

    @property
    def lineno(self):
        return self.lexer.lineno

    @lineno.setter
    def lineno(self, value):
        self.lexer.lineno = value

    @property
    def lexpos(self):
        return self.lexer.lexpos

    @lexpos.setter
    def lexpos(self, value):
        self.lexer.lexpos = value

    def clone(self):
        return FilteredLexer(self.lexer.clone())

    def current_state(self):
        return self.lexer.current_state()

    def input(self, input):
        self.lexer.input(input)

    def next_lexer_token(self):
        """Return next lexer token.
        Can be useful to customize parser behavior without need to touch
        parser code in the token method."""
        return self.lexer.token()

    def token(self, unparsed):
        t = self.next_lexer_token()

        # Filter out tokens that the parser is not expecting.
        while t and t.type in unparsed:

            # Skip over open tags, but keep track of when we see them.
            if t.type == 'OPEN_TAG':
                if self.last_token and self.last_token.type == 'SEMI':
                    # Rewrite ?><?php as a semicolon.
                    t.type = 'SEMI'
                    t.value = ';'
                    break
                self.last_token = t
                t = self.next_lexer_token()
                continue

            # Rewrite <?= to yield an "echo" statement.
            if t.type == 'OPEN_TAG_WITH_ECHO':
                t.type = 'ECHO'
                break

            # Insert semicolons in place of close tags where necessary.
            if t.type == 'CLOSE_TAG':
                if self.last_token and \
                    self.last_token.type in ('OPEN_TAG', 'SEMI', 'COLON',
                                             'LBRACE', 'RBRACE'):
                    # Dont insert semicolons after these tokens.
                    pass
                else:
                    # Rewrite close tag as a semicolon.
                    t.type = 'SEMI'
                    break

            t = self.next_lexer_token()

        self.last_token = t
        return t

    # Iterator interface
    def __iter__(self):
        return self

    def __next__(self):
        t = self.token()
        if t is None:
            raise StopIteration
        return t

    __next__ = next
