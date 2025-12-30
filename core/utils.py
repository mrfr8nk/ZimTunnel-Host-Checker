from colorama import Fore, Style

def color(text, rgb):
    return f"\033[38;2;{rgb[0]};{rgb[1]};{rgb[2]}m{text}{Style.RESET_ALL}"
