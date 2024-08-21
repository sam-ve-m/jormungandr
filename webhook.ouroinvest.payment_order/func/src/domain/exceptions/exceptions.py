class NotSentToBifrost(Exception):
    msg = "Fail to send to Bifrost data"


class ErrorOnSave(Exception):
    msg = "Fail to save payment order"

