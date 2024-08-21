class NotSentToPersephone(Exception):
    msg = "UpdateMarketTimeExperience.update_market_time_experience::sent_to_persephone:: the data was not sent to persephone_queue"


class CaronteTransportError(Exception):
    msg = "Jormungandr-OuroInvest:Webhook::CaronteTransport.get_user_register::error on fetching data from Caronte" \
          "Não existe cliente para a inscrição informada"


class UserWasNotFound(Exception):
    msg = "Jormungandr-Onboarding::UserRepository::update_user_and_broker_member - user was not found"


class UserWasNotUpdated(Exception):
    msg = "UpdateOuroInvestInformation::update_ouroinvest_exchange_account - user was not updated"


class StatusSentIsNotValid(Exception):
    msg = "CheckIfEnumStatusIsValid.check_if_enum_is_valid:: this is not a valid enum"

