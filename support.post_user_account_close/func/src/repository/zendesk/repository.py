# Standards
from typing import Any

# Third part
from etria_logger import Gladsheim
from zenpy.lib.api_objects import User, Ticket, Via, Comment

# Jormungandr
from ...domain.exceptions.exceptions import ErrorWithZendesk
from ...domain.models.user import UserData
from ...infrastructure.zendesk.infrastructure import ZendeskInfrastructure


class ZendeskRepository:
    infra = ZendeskInfrastructure
    method = Via(source="api")

    @classmethod
    def get_user(cls, unique_id: str) -> User:
        zenpy_client = cls.infra.get_connection()
        if user_results := zenpy_client.users(external_id=unique_id):
            user_zenpy = user_results.values[0]
            return user_zenpy

    @classmethod
    def create_user(cls, user_data: UserData) -> User:
        user_obj = User(
            email=user_data.email,
            name=user_data.nick_name,
            external_id=user_data.unique_id
        )
        zenpy_client = cls.infra.get_connection()
        try:
            user = zenpy_client.users.create(user_obj)
            return user
        except Exception as ex:
            Gladsheim.error(
                error=ex,
                message=f"Jormungandr::CreateTicketService::create_user::Failed to create user",
            )
            raise ErrorWithZendesk()

    @staticmethod
    def set_comment(user: User, snapshot: str) -> Comment:
        comment = Comment(
            public=False,
            author_id=user.id,
            html_body=snapshot,
        )
        return comment

    @staticmethod
    def set_ticket(subject: str, user: User, ticket_type: str, comment: Comment) -> Ticket:
        ticket = Ticket(
            comment=comment,
            subject=subject,
            requester_id=user.id,
            ticket_type=ticket_type,
            via=ZendeskRepository.method,
        )
        return ticket

    @classmethod
    def post_ticket(cls, ticket: Ticket) -> Any:
        zenpy_client = cls.infra.get_connection()
        try:
            open_ticket = zenpy_client.tickets.create(ticket)
            return open_ticket
        except Exception as ex:
            Gladsheim.error(
                error=ex,
                message=f"Jormungandr::CreateTicketService::set_tickets::Failed to create ticket",
            )
            raise ErrorWithZendesk()
