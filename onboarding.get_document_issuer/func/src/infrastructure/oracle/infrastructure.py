import cx_Oracle

from src.infrastructure.env_config import Configuration


class OracleInfrastructure:
    @classmethod
    def get_connection(cls) -> cx_Oracle.Cursor:
        connection = cls._make_connection()
        return connection.cursor()

    @classmethod
    def _make_connection(cls) -> cx_Oracle.Connection:
        connection = cx_Oracle.connect(
            user=Configuration.config("ORACLE_USER"),
            password=Configuration.config("ORACLE_PASSWORD"),
            dsn=cx_Oracle.makedsn(
                Configuration.config("ORACLE_BASE_DSN"),
                Configuration.config("ORACLE_PORT"),
                service_name=Configuration.config("ORACLE_SERVICE"),
            ),
            encoding=Configuration.config("ORACLE_ENCODING"),
        )
        return connection
