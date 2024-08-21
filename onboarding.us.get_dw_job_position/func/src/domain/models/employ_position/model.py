from pydantic import BaseModel


class EmployPositionModel(BaseModel):
    code: str
    value: str

    @classmethod
    def from_database(cls, database_return: tuple) -> dict:
        model = cls(
            code=database_return[0],
            value=database_return[1],
        ).dict()
        return model
