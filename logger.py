import logging

COLORS = {
    'DEBUG': '\033[36m',      
    'INFO': '\033[32m',      
    'WARNING': '\033[33m',   
    'ERROR': '\033[31m',     
    'CRITICAL': '\033[35m',   
    'RESET': '\033[0m',      
    'BLUE': '\033[34m',      
    'MAGENTA': '\033[35m',    
    'CYAN': '\033[36m',      
    'WHITE': '\033[37m',     
    'YELLOW': '\033[93m',   
    'RED': '\033[91m',      
    'GREEN': '\033[92m',     
}

def color_formatter(record):
    original_msg = record.msg
    
    color = COLORS.get(record.levelname, COLORS['INFO'])
    
    if color:
        record.msg = f"{color}{original_msg}{COLORS['RESET']}"
    
    formatter = logging.Formatter(
        '%(asctime)s - %(message)s',
        datefmt='%H:%M:%S'
    )
    return formatter.format(record)

def setup_logger():
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    
    handler = logging.StreamHandler()
    handler.setLevel(logging.INFO)
    
    handler.setFormatter(logging.Formatter('%(asctime)s - %(message)s', datefmt='%H:%M:%S'))
    
    logger.addHandler(handler)
    
    return logger

def success(text):
    return f"{COLORS['GREEN']}{text}{COLORS['RESET']}"

def warning(text):
    return f"{COLORS['YELLOW']}{text}{COLORS['RESET']}"

def error(text):
    return f"{COLORS['RED']}{text}{COLORS['RESET']}"

def info(text):
    return f"{COLORS['BLUE']}{text}{COLORS['RESET']}"

def track(text):
    return f"{COLORS['MAGENTA']}{text}{COLORS['RESET']}"

def debug(text):
    return f"{COLORS['CYAN']}{text}{COLORS['RESET']}"