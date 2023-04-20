import os.path
from extensions import writer

class ArgumentsValidator:
    ExpectedNumberOfArguments = 2

    @staticmethod
    def AreCorrect(args):
        return ArgumentsValidator.NumberOfArgumentsMatch(len(args)) and ArgumentsValidator.FileExists(args[1])

    @staticmethod
    def NumberOfArgumentsMatch(numberOfArguments):
        if numberOfArguments == ArgumentsValidator.ExpectedNumberOfArguments:
            return True
        writer.ConsoleWriter.write_error(f"Invalid number of arguments. Expected {ArgumentsValidator.ExpectedNumberOfArguments}, received {numberOfArguments}")
        return False

    @staticmethod
    def FileExists(filePath):
        if os.path.isfile(filePath):
            return True
        writer.ConsoleWriter.write_error("File does not exist")
        return False