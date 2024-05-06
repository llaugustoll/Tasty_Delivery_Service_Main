import logging

formatter = logging.Formatter('%(asctime)s - Process: %(process)d - %(module)s - %(levelname)s - %(message)s')


# handlers
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)

# loggers
logger = logging.getLogger(__name__)
logger.setLevel('DEBUG')
logger.addHandler(console_handler)
