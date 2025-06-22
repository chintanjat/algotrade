"""
Logging configuration and utilities
"""

import logging
import logging.handlers
from pathlib import Path
from typing import Optional

def setup_logger(
    name: str = "algotrade",
    level: str = "INFO",
    log_file: Optional[str] = None,
    max_size: str = "10MB",
    backup_count: int = 5,
    debug: bool = False
) -> logging.Logger:
    """
    Setup and configure logger for AlgoTrade
    
    Args:
        name: Logger name
        level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file: Path to log file
        max_size: Maximum size for log rotation
        backup_count: Number of backup files to keep
        debug: Enable debug mode
    
    Returns:
        Configured logger instance
    """
    
    # Create logger
    logger = logging.getLogger(name)
    
    # Set level
    if debug:
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(getattr(logging, level.upper(), logging.INFO))
    
    # Clear existing handlers
    logger.handlers.clear()
    
    # Create formatters
    detailed_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s'
    )
    simple_formatter = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(message)s'
    )
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(simple_formatter)
    logger.addHandler(console_handler)
    
    # File handler (if log_file specified)
    if log_file:
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Parse max_size (e.g., "10MB" -> 10 * 1024 * 1024)
        size_parts = max_size.upper().replace('B', '').replace('BYTE', '')
        if size_parts.endswith('K'):
            max_bytes = int(size_parts[:-1]) * 1024
        elif size_parts.endswith('M'):
            max_bytes = int(size_parts[:-1]) * 1024 * 1024
        elif size_parts.endswith('G'):
            max_bytes = int(size_parts[:-1]) * 1024 * 1024 * 1024
        else:
            max_bytes = int(size_parts)
        
        # Rotating file handler
        file_handler = logging.handlers.RotatingFileHandler(
            log_path,
            maxBytes=max_bytes,
            backupCount=backup_count
        )
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(detailed_formatter)
        logger.addHandler(file_handler)
    
    # Error file handler
    error_log_path = Path('logs/error.log')
    error_log_path.parent.mkdir(parents=True, exist_ok=True)
    error_handler = logging.handlers.RotatingFileHandler(
        error_log_path,
        maxBytes=5 * 1024 * 1024, # 5MB
        backupCount=3
    )
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(detailed_formatter)
    logger.addHandler(error_handler)
    
    # Prevent propagation to root logger
    logger.propagate = False
    
    return logger

def get_logger(name: str = "algotrade") -> logging.Logger:
    """
    Get existing logger instance
    
    Args:
        name: Logger name
    
    Returns:
        Logger instance
    """
    return logging.getLogger(name)

class LoggerMixin:
    """Mixin class to add logging capabilities to other classes"""
    
    def __init__(self, logger_name: Optional[str] = None):
        if logger_name is None:
            logger_name = self.__class__.__name__
        self.logger = get_logger(logger_name)
    
    def log_info(self, message: str):
        """Log info message"""
        self.logger.info(message)
    
    def log_warning(self, message: str):
        """Log warning message"""
        self.logger.warning(message)
    
    def log_error(self, message: str):
        """Log error message"""
        self.logger.error(message)
    
    def log_debug(self, message: str):
        """Log debug message"""
        self.logger.debug(message)
    
    def log_critical(self, message: str):
        """Log critical message"""
        self.logger.critical(message) 