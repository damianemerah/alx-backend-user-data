#!/usr/bin/env python3
"""
 function called filter_datum that returns the log message obfuscated:
"""
import re
from typing import List
import logging
from os import environ
import mysql.connector

PII_FIELDS = ("name", "email", "phone", "ssn", "password")


def get_logger() -> logging.Logger:
    """function that takes no arguments and returns a
    logging.Logger"""
    logger = logging.getLogger('user_data')
    logger.setLevel(logging.INFO)
    logger.propagate = False
    handler = logging.StreamHandler()
    handler.setFormatter(RedactingFormatter(list(PII_FIELDS)))
    logger.addHandler(handler)

    return logger


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """ Returns a log message obfuscated """
    for f in fields:
        message = re.sub(f'{f}=.*?{separator}',
                         f'{f}={redaction}{separator}', message)
    return message


def get_db() -> mysql.connector.connection.MySQLConnection:
    """Return a connection to mysql db"""
    username = environ.get('PERSONAL_DATA_DB_USERNAME', 'root')
    password = environ.get('PERSONAL_DATA_DB_PASSWORD', '')
    host = environ.get('PERSONAL_DATA_DB_HOST', 'localhost')
    database = environ.get('PERSONAL_DATA_DB_NAME')

    cnx = mysql.connector.connection.MySQLConnection(user=username,
                                                     password=password,
                                                     host=host,
                                                     database=database)

    return cnx


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """filter values in incoming log records using filter_datum"""
        message = super().format(record)
        return filter_datum(self.fields, self.REDACTION,
                            message, self.SEPARATOR)


def main() -> None:
    """Retrieves and display user table"""
    db = get_db()
    cursor = db.cursor()

    cursor.execute("SELECT * FROM users;")
    field_names = [i[0] for i in cursor.description]
    logger = get_logger()

    for row in cursor:
        str_row = ''.join(f'{f}={str(r)}; ' for r, f in zip(row, field_names))
        logger.info(str_row.strip())
    cursor.close()
    db.close()


if __name__ == '__main__':
    main()
