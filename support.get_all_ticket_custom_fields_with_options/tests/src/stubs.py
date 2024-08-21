ticket_custom_fields = {
    "ticket_fields": [
        {
            "url": "https://sigame.zendesk.com/api/v2/ticket_fields/360048721032.json",
            "id": 360048721032,
            "type": "tagger",
            "title": "Categoria",
            "raw_title": "Categoria",
            "description": "",
            "raw_description": "",
            "position": 9999,
            "active": True,
            "required": True,
            "collapsed_for_agents": False,
            "regexp_for_validation": None,
            "title_in_portal": "Categoria da solicitação",
            "raw_title_in_portal": "Categoria da solicitação",
            "visible_in_portal": True,
            "editable_in_portal": True,
            "required_in_portal": True,
            "tag": None,
            "created_at": "2021-10-29T17:42:04Z",
            "updated_at": "2021-11-09T19:36:13Z",
            "removable": True,
            "agent_description": "Campo utilizado para determinar o tipo de solicitação nos formulários.",
            "custom_field_options": [
                {
                    "id": 360093384932,
                    "name": "Dúvida",
                    "raw_name": "Dúvida",
                    "value": "dúvida",
                    "default": False,
                },
                {
                    "id": 360093384972,
                    "name": "Elogio",
                    "raw_name": "Elogio",
                    "value": "elogio",
                    "default": False,
                },
                {
                    "id": 360093510652,
                    "name": "Sugestão",
                    "raw_name": "Sugestão",
                    "value": "sugestão",
                    "default": False,
                },
                {
                    "id": 360093384952,
                    "name": "Reclamação",
                    "raw_name": "Reclamação",
                    "value": "reclamação",
                    "default": False,
                },
            ],
        }
    ]
}


treatment_ticket_custom_fields = {
    "custom_fields": [
        {
            "id": 360048721032,
            "title": "Categoria",
            "custom_field_options": [
                {"id": 360093384932, "name": "Dúvida", "value": "dúvida"},
                {"id": 360093384972, "name": "Elogio", "value": "elogio"},
                {"id": 360093510652, "name": "Sugestão", "value": "sugestão"},
                {"id": 360093384952, "name": "Reclamação", "value": "reclamação"},
            ],
        }
    ]
}


class StubRequestObj:
    def __init__(self, status_code=None):
        self.status_code = status_code

    @staticmethod
    def json():
        return ticket_custom_fields
