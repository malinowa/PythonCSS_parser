import sys

class ConsoleWriter:
    ErrorColor = "31"  # Red color code
    InformationColor = "32"  # Green color code

    @staticmethod
    def write(message, color):
        sys.stdout.write("\033[{}m{}\033[0m\n".format(color, message))

    @staticmethod
    def write_error(message):
        ConsoleWriter.write(message, ConsoleWriter.ErrorColor)

    @staticmethod
    def write_information(message):
        ConsoleWriter.write(message, ConsoleWriter.InformationColor)