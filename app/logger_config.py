import logging
import io
import sys

log_stream = io.StringIO()

# Set formatter
formatter = logging.Formatter(
    "%(asctime)s - %(levelname)s - %(message)s"
)

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
