import sys
from utils.exceptions.invalid_token_exception import InvalidTokenException
from utils.exceptions.token_not_defined_exception import TokenNotDefinedException
from extensions.writer import ConsoleWriter
from parser.parser import Parser
from tokenizer.tokenizer import Tokenizer
from validators.arguments_validator import ArgumentsValidator

if not ArgumentsValidator.AreCorrect(sys.argv):
    sys.exit()

with open(sys.argv[1], 'r') as file:
    fileContent = file.read()

tokenizer = Tokenizer()
tokens = tokenizer.tokenize_file(fileContent)

parser = Parser(tokens)
try:
    parser.parse()
    ConsoleWriter.write_information("Pomyślnie zwalidowano plik wejściowy.")
except TokenNotDefinedException as tokenNotDefined:
    ConsoleWriter.write_error(tokenNotDefined)
except InvalidTokenException as invalidToken:
    ConsoleWriter.write_error(invalidToken)