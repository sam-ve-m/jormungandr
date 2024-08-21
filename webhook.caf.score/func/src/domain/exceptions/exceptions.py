class TransactionNotFound(Exception):
    msg = "BureauTransactionRepository.get_user_unique_id_of_transaction - Transaction was not updated"


class UniqueIdNotFound(Exception):
    msg = "BureauTransactionRepository.get_user_unique_id_of_transaction - Unique Id was not updated"


class ErrorSendingToIaraDatailCpfValidation(Exception):
    msg = "BureauApiTransport::detail_transaction::Error trying to request transaction details, reason: {}"


class UserWasNotUpdated(Exception):
    msg = "UserRepository::update_bureau_validation - user was not updated"


class TransactionWasNotUpdated(Exception):
    msg = "BureauTransactionRepository::update_bureau_transaction - transaction was not updated"


class NotSentToPersephone(Exception):
    msg = "BureauTransactionRepository::update_bureau_transaction::sent_to_persephone:: the data was not sent to persephone_queue"


class InvalidStatusReceived(Exception):
    msg = "Invalid status received: {}"


class InvalidMessageTypeReceived(Exception):
    msg = "Invalid message type received: {}"


class InitializeError(Exception):
    msg = "Unable to connect to mongodb Collection"
