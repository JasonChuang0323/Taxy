import traceback
import logging

class UserException(Exception):
    def __init__(self, message, status_code=500):
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.log_error()

    def log_error(self):
        """Log the exception details."""
        logging.error(f"An error occurred: {self.message}")
        logging.error(traceback.format_exc())

    def to_response(self):
        """Format the exception as a JSON response."""
        return {'error': self.message}, self.status_code
