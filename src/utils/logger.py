"""CSV logger for training metrics."""

import os
import csv


class CSVLogger:

    def __init__(self, log_dir: str = "logs", filename: str = "train_log.csv"):
        raise NotImplementedError('Implementation removed for public mirror.')

    def log(self, record: dict):
        raise NotImplementedError('Implementation removed for public mirror.')

    def close(self):
        raise NotImplementedError('Implementation removed for public mirror.')
