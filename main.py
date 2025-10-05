#!/usr/bin/env python3
"""
Ubiquitous Cube Game - A Minecraft-inspired voxel engine tech demo.

This is the main entry point for the game. It initializes the game engine
and starts the main game loop.
"""

import sys
import logging
from pathlib import Path
from datetime import datetime
from app.game import Game


class StreamToLogger:
    """
    Fake file-like stream object that redirects writes to a logger instance.
    """
    def __init__(self, logger, log_level=logging.INFO):
        self.logger = logger
        self.log_level = log_level
        self.linebuf = ''

    def write(self, buf):
        for line in buf.rstrip().splitlines():
            self.logger.log(self.log_level, line.rstrip())

    def flush(self):
        pass


def setup_logging():
    """
    Configure logging for the application.

    Logs are written to both console and a file in the logs/ directory.
    Log files are named with timestamps for easy identification.
    Redirects all stdout/stderr to be captured in logs.
    """
    # Create logs directory if it doesn't exist
    log_dir = Path('logs')
    log_dir.mkdir(exist_ok=True)

    # Generate log filename with timestamp
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    log_file = log_dir / f'game_{timestamp}.log'

    # Configure logging with both file and console handlers
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler(sys.__stdout__)  # Use original stdout
        ]
    )

    # Redirect stdout and stderr to logger
    stdout_logger = logging.getLogger('STDOUT')
    sys.stdout = StreamToLogger(stdout_logger, logging.INFO)

    stderr_logger = logging.getLogger('STDERR')
    sys.stderr = StreamToLogger(stderr_logger, logging.ERROR)

    return log_file


def main():
    """
    Main entry point for the game.

    Creates the game engine object and starts the game loop.
    Handles graceful shutdown on errors.

    Returns:
        int: Exit code (0 for success, 1 for failure)
    """
    log_file = setup_logging()
    logger = logging.getLogger(__name__)

    try:
        logger.info("Starting Ubiquitous Cube Game...")
        logger.info("Logging to: %s", log_file)
        game = Game()
        game.run()
        logger.info("Game exited normally")
        return 0

    except KeyboardInterrupt:
        logger.info("Game interrupted by user")
        return 0

    except Exception as e:
        logger.exception("Fatal error occurred: %s", e)
        return 1


if __name__ == '__main__':
    sys.exit(main())
