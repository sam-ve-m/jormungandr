from typing import List

from func.src.infrastructure.oracle.infrastructure import OracleInfrastructure


class EmployPositionOracleRepository:

    @classmethod
    def get_employ_position(cls) -> List[tuple]:
        sql = """
            SELECT CODE, DESCRIPTION
            FROM USPIXDB001.SINCAD_EXTERNAL_EMPLOY_POSITIONS
        """
        enum_values = cls._query(sql=sql)
        return enum_values

    @classmethod
    def _query(cls, sql: str) -> list:
        with OracleInfrastructure.get_cursor() as cursor:
            cursor.execute(sql)
            rows = cursor.fetchall()
            rows = cls._normalize_encode(rows=rows)
            return rows

    @staticmethod
    def _normalize_encode(rows: List[tuple]) -> List[tuple]:
        new_rows = [tuple((
                item.encode().decode("utf-8", "strict")
                if isinstance(item, str) else
                item
            ) for item in row
        ) for row in rows]
        return new_rows
