# THIRD PART IMPORT
from contextlib import contextmanager
from typing import Generator

import cx_Oracle
from decouple import config
from etria_logger import Gladsheim

from func.src.domain.exceptions.exceptions import FailToFetchData


class OracleInfrastructure:
    connection = None

    @classmethod
    def _get_connection(cls) -> cx_Oracle.Connection:
        if cls.connection is None:
            cls.connection = cx_Oracle.connect(
                dsn=config("ORACLE_CONNECTION_STRING"),
                user=config("ORACLE_USER"),
                password=config("ORACLE_PASSWORD")
            )
        return cls.connection

    @classmethod
    @contextmanager
    def get_cursor(cls) -> Generator[cx_Oracle.Cursor, None, None]:
        try:
            connection = cls._get_connection()
            with connection.cursor() as cursor:
                yield cursor
        except cx_Oracle.DatabaseError as e:
            (error,) = e.args
            message = f"Oracle-Error-Code: {error.code}. Oracle-Error-Message: {error.message} - Oracle-ex: {e}"
            Gladsheim.error(error=e, message=message)
            raise FailToFetchData()
