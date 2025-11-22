import logging
import sys
from colorama import init, Fore, Back, Style

init()

COLORS = {
    'DEBUG': Fore.CYAN,
    'INFO': Fore.WHITE, 
    'WARNING': Fore.YELLOW,
    'ERROR': Fore.RED,
    'CRITICAL': Fore.RED + Style.BRIGHT,
    'RESET': Style.RESET_ALL,
    'BLUE': Fore.BLUE,
    'MAGENTA': Fore.MAGENTA,
    'CYAN': Fore.CYAN,
    'WHITE': Fore.WHITE,
    'YELLOW': Fore.YELLOW,
    'RED': Fore.RED,
    'GREEN': Fore.GREEN,
    'GRAY': Fore.WHITE
}

def setup_logger():
    logger = logging.getLogger('YMDownloader')
    logger.setLevel(logging.INFO)
    
    if logger.handlers:
        return logger
    
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.INFO)
    
    handler.setFormatter(logging.Formatter('%(asctime)s - %(message)s', datefmt='%H:%M:%S'))
    
    logger.addHandler(handler)
    logger.propagate = False
    
    return logger

def success(text):
    return f"{COLORS['GREEN']}{text}{COLORS['RESET']}"

def warning(text):
    return f"{COLORS['YELLOW']}{text}{COLORS['RESET']}"

def error(text):
    return f"{COLORS['RED']}{text}{COLORS['RESET']}"

def info(text):
    return f"{COLORS['BLUE']}{text}{COLORS['RESET']}"

def debug(text):
    return f"{COLORS['CYAN']}{text}{COLORS['RESET']}"

def gray(text):
    return f"{COLORS['GRAY']}{text}{COLORS['RESET']}"