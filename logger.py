import logging

# Set up the logger only once
formatter = logging.Formatter(fmt='%(asctime)s - %(levelname)s - %(message)s')
handler = logging.FileHandler('smartCalendar.log')
handler.setFormatter(formatter)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(handler)
