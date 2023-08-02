import logging
import io
import sys
import time


class CustomFormatter(logging.Formatter):
    def __init__(self, fmt):
        super().__init__(fmt)
        self.start_time = time.time()

    def format(self, record):
        elapsed_time = time.time() - self.start_time
        record.elapsed_time = (
            elapsed_time * 1000
        )  # convert to milliseconds
        return super().format(record)


log_stream = io.StringIO()

# Set formatter
log_format = "%(asctime)s - %(levelname)s - %(message)s - (%(elapsed_time)d ms)"
formatter = CustomFormatter(fmt=log_format)

# Create a logging handler that writes to the log_stream
stream_handler = logging.StreamHandler(log_stream)
stream_handler.setLevel(logging.INFO)
stream_handler.setFormatter(formatter)

# Handler t log to console
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(formatter)

# Create a logger
logger = logging.getLogger("my_shared_logger")
logger.setLevel(logging.INFO)

# Add the stream and console handler to your logger
logger.addHandler(stream_handler)
# logger.addHandler(console_handler)
