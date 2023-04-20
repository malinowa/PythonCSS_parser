import re
from typing import List

from utils import tokens as tk
from utils.exceptions import invalid_token_exception, token_not_defined_exception
from utils.regex import Regexes


class Parser:
    _tokens: List[str]
    _lineNumber: int

    def __init__(self, tokens: List[str]):
        self._tokens = tokens
        self._lineNumber = 1

    def parse(self):
        i = 0
        # print(self._tokens)
        while i < len(self._tokens):
            token = self._tokens[i]
            if token == tk.Tokens.NewLineCharacter:
                self._lineNumber += 1
            elif token == tk.Tokens.CommentBeginning:
                i += 1
                i = self._parse_comment(i)
            elif Regexes.Identifier.match(token):
                i += 1
                i = self._parse_clause(i)
            else:
                raise token_not_defined_exception.TokenNotDefinedException(self._format_error_message(i,
                    f"Analizowany token nie został uwzględniony w gramatyce: \"{token}\"\n"))
            i += 1

    def _parse_comment(self, current_token_index: int) -> int:
        while current_token_index < len(self._tokens) - 1:
            if self._tokens[current_token_index] == tk.Tokens.NewLineCharacter:
                self._lineNumber += 1
                return current_token_index
            current_token_index += 1
        return current_token_index

    def _parse_clause(self, current_token_index: int) -> int:
        current_token_index = self._parse_clause_header(current_token_index)
        current_token_index = self._parse_clause_body(current_token_index)
        return current_token_index

    def _parse_clause_header(self, current_token_index: int) -> int:
        while (self._tokens[current_token_index] != tk.Tokens.NewLineCharacter and
               self._tokens[current_token_index] != tk.Tokens.CommentBeginning):
            is_combinator = self._tokens[current_token_index] in tk.Tokens.Combinators
            if is_combinator:
                current_token_index += 1
                if self._tokens[current_token_index] == tk.Tokens.NewLineCharacter:
                    current_token_index += 1
                    self._lineNumber += 1
                elif self._tokens[current_token_index] == tk.Tokens.CommentBeginning:
                    current_token_index += 1
                    current_token_index = self._parse_comment(current_token_index)
            if not Regexes.Identifier.match(self._tokens[current_token_index]):
                current_token_index += 1
                raise invalid_token_exception.InvalidTokenException(self._format_error_message(current_token_index,
                    f"Identyfikator powinien być zgodny z następującym wyrażeniem regularnym:\n {Regexes.Identifier} \n"))
            current_token_index += 1
        if self._tokens[current_token_index] == tk.Tokens.CommentBeginning:
            current_token_index += 1
            current_token_index = self._parse_comment(current_token_index)
            current_token_index += 1
            return current_token_index
        self._lineNumber += 1
        current_token_index += 1
        return current_token_index

    def _parse_clause_body(self, current_token_index: int) -> int:
        while current_token_index < len(self._tokens) - 1:
            if self._tokens[current_token_index] != tk.Tokens.Indent:
                raise invalid_token_exception.InvalidTokenException(self._format_error_message(current_token_index,
                    "Brakujące wcięcie (oczekiwana tabulacja) w ciele wyrażenia.\n"));
            
            current_token_index += 1
            current_token_index = self._parse_expression(current_token_index)

            if self._tokens[current_token_index] == ';':
                current_token_index += 1
            elif self._tokens[current_token_index] == '\n' and self._tokens[current_token_index + 1] != '\n':
                error_msg = f"Wyrażenia muszą kończyć się średnikiem.\n"
                raise invalid_token_exception.InvalidTokenException(self._format_error_message(current_token_index - 1, error_msg))

            if self._tokens[current_token_index] == '\n':
                current_token_index += 1
                self._lineNumber += 1

            if self._tokens[current_token_index] != '\n':
                continue

            self._lineNumber += 1
            return current_token_index

        return current_token_index
    
    def _parse_expression(self, current_token_index):
        if not Regexes.ExpressionLabel.match(self._tokens[current_token_index]):
            raise invalid_token_exception.InvalidTokenException(self._format_error_message(current_token_index, "Niepoprawna etykieta wyrażenia.\n"))

        current_token_index += 1

        if self._tokens[current_token_index] != tk.Tokens.DeclarationLabelSeparator:
            raise invalid_token_exception.InvalidTokenException(self._format_error_message(current_token_index, f"Niepoprawny token oddzielający etykietę wyrażenia od wartości\n. Oczekiwany token to {tk.Tokens.DeclarationLabelSeparator}\n"))

        current_token_index += 1

        while self._tokens[current_token_index] != tk.Tokens.DeclarationEnding and self._tokens[current_token_index] != tk.Tokens.NewLineCharacter:
            if self._tokens[current_token_index] == tk.Tokens.Keyword:
                current_token_index += 1
            elif Regexes.UnitValue.match(self._tokens[current_token_index]):
                current_token_index += 1
            elif Regexes.ColorHexValue.match(self._tokens[current_token_index]):
                current_token_index += 1
            elif Regexes.UrlValue.match(self._tokens[current_token_index]):
                current_token_index += 1
            elif Regexes.StringValue.match(self._tokens[current_token_index]):
                current_token_index += 1
            elif Regexes.TextValue.match(self._tokens[current_token_index]):
                current_token_index += 1
            elif Regexes.NumberValue.match(self._tokens[current_token_index]):
                current_token_index += 1
            elif self._tokens[current_token_index] == tk.Tokens.CommentBeginning:
                current_token_index = self._parse_comment(current_token_index)
            else:
                raise invalid_token_exception.InvalidTokenException(self._format_error_message(current_token_index, "Niepoprawna wartość wyrażenia. Wartość może być: \n" +
                    "- słowem kluczowym !important\n" +
                    "- liczbą z jednostką (np. 10rem lub 7.5in)\n" +
                    "- liczbą całkowitą\n" +
                    "- kolorem zapisanym w formacie heksadecymalnym (np. #fff lub #a01212)\n" +
                    "- adresem url (np. watch?v=Ct6BUPvE2sM)\n" +
                    "- napisem (np. \"see below\")\n" +
                    "- tekstem (np. avoid)\n"))

        return current_token_index

    def _format_error_message(self, current_token_index: int, error_message: str) -> str:
        search_forward_index = current_token_index
        while search_forward_index < len(self._tokens) and self._tokens[search_forward_index] != '\n':
            search_forward_index += 1

        search_backward_index = current_token_index if current_token_index == 0 else current_token_index
        while search_backward_index > 0 and self._tokens[search_backward_index] != '\n':
            search_backward_index -= 1

        current_line_tokens = self._tokens[search_backward_index:search_forward_index]
        number_of_spaces = sum(len(s) if s != '\t' else 8 for s in self._tokens[search_backward_index + 1:current_token_index])

        number_of_separators = sum(1 for s in self._tokens[search_backward_index:current_token_index] if s not in {'\t', '\n'})

        string_builder = []
        string_builder.append(f"Linia nr.{self._lineNumber}: \n")
        string_builder.append(' '.join(current_line_tokens))

        string_builder.append('\n')
        string_builder.append(' ' * (number_of_spaces + number_of_separators))
        current_token_length = 8 if self._tokens[current_token_index] == '\t' else len(self._tokens[current_token_index])
        string_builder.append('^' * current_token_length)

        string_builder.append('\n')
        string_builder.append(error_message)

        return ''.join(string_builder)