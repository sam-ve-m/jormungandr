# Third party
from pydantic import BaseModel, constr


class NotificationValidator(BaseModel):
    id: constr(min_length=36, max_length=36)
