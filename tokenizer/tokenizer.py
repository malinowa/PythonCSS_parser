import re
from typing import List

from utils import tokens as tk


class Tokenizer:
    def tokenize_file(self, file_content: str) -> List[str]:
        if not file_content:
            return []

        unified_file_content = file_content.replace("\r\n", tk.Tokens.NewLineCharacter).replace("\n", tk.Tokens.NewLineCharacter)
        unified_file_content = re.sub(r"(\S)?([\,\+\>\<\;])(\S)?", r"\1 \2 \3", unified_file_content)
        unified_file_content = re.sub(r"(\S)?(:)", r"\1 \2", unified_file_content)

        tokens = []
        for result in re.finditer(r"\n|\t|[^\s\"']+|\"[^\"]*\"|'[^']*'", unified_file_content):
            tokens.append(result.group())

        self._pad_file_ending(tokens)
        return tokens

    @staticmethod
    def _pad_file_ending(tokens: List[str]) -> None:
        if tokens[-1] != tk.Tokens.NewLineCharacter:
            tokens.append(tk.Tokens.NewLineCharacter)

        if tokens[-2] != tk.Tokens.NewLineCharacter:
            tokens.append(tk.Tokens.NewLineCharacter)