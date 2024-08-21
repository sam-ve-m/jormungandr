# OUTSIDE LIBRARIES
from typing import List

# OUTSIDE LIBRARIES
from etria_logger import Gladsheim

# SOURCE CODE
from func.src.domain.exceptions.exceptions import InternalServerError
from func.src.infrastructure.oracle.infrastructure import OracleInfrastructure


class OracleBaseRepository:

    infra = OracleInfrastructure

    @classmethod
    def query(cls, sql: str) -> list:
        try:
            with cls.infra.get_connection() as cursor:
                cursor.execute(sql)
                rows = cursor.fetchall()
                rows = cls._normalize_encode(rows=rows)
                return rows

        except Exception as e:
            message = f"Exception: {e}. Oracle-Error-Base-Exception Sql: {sql}"
            Gladsheim.error(error=e, message=message)
            raise InternalServerError(
                "common.process_issue::OracleBaseRepository.query"
            )

    @staticmethod
    def _normalize_encode(rows: List[tuple]) -> List[tuple]:
        new_rows = list()
        for row in rows:
            new_row = list()
            for item in row:
                if type(item) == str:
                    item = item.encode().decode("utf-8", "strict")
                new_row.append(item)
            new_rows.append(tuple(new_row))

        return new_rows

    @classmethod
    def execute(cls, sql, values) -> None:
        try:
            with cls.infra.get_connection() as cursor:
                cursor.execute(sql, values)

        except InternalServerError as e:
            (error,) = e.args
            message = (
                f""
                f"Oracle-Error-Code: {error.code}. Oracle-Error-Message: {error.message} - "
                f"Values: {values} - Oracle-ex: {e}"
            )
            Gladsheim.error(error=e, message=message)
            raise InternalServerError(
                "common.process_issue::OracleBaseRepository.execute"
            )
