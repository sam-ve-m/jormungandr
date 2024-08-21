# STANDARD IMPORTS
import cx_Oracle
from decouple import config


class OracleInfrastructure:
    @classmethod
    def get_connection(cls) -> cx_Oracle.Cursor:
        connection = cls._make_connection()
        return connection.cursor()

    @classmethod
    def _make_connection(cls) -> cx_Oracle.Connection:
        connection = cx_Oracle.connect(
            dsn=config("ORACLE_CONNECTION_STRING"),
            user=config("ORACLE_USER"),
            password=config("ORACLE_PASSWORD")
        )
        return connection
