import logging
import sys
from colorlog import ColoredFormatter

STARTUP = 25
logging.addLevelName(STARTUP, "STARTUP")


logger = logging.getLogger(__name__)

color_formatter = ColoredFormatter(
    fmt="%(log_color)s[%(asctime)s] - %(levelname)-7s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    log_colors={"DEBUG": "white", "INFO": "white", "WARNING": "purple", "ERROR": "red", "CRITICAL": "red,bg_white", "STARTUP": "yellow"},
)

handler = logging.StreamHandler(sys.stdout)

handler.setFormatter(color_formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)
