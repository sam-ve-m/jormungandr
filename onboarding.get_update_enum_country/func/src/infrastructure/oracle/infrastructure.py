import cx_Oracle

from func.src.infrastructure.env_config import Configuration


class OracleInfrastructure:
    @classmethod
    def get_connection(cls) -> cx_Oracle.Cursor:
        connection = cls._make_connection()
        return connection.cursor()

    @classmethod
    def _make_connection(cls) -> cx_Oracle.Connection:
        connection = cx_Oracle.connect(
            dsn=Configuration.config("ORACLE_CONNECTION_STRING"),
            user=Configuration.config("ORACLE_USER"),
            password=Configuration.config("ORACLE_PASSWORD")
        )
        return connection
