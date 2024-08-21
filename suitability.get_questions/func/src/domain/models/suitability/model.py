# Jormungandr
from ...validators.suitability.validator import (
    SuitabilityValidator,
    QuestionValidator,
    AnswerValidator,
)


class Answers:
    def __init__(self, answer: AnswerValidator):
        self.text = answer.text
        self.option_id = answer.option_id
        self.weight = answer.weight


class Questions:
    def __init__(self, question: QuestionValidator):
        self.answers = [Answers(answer=answer) for answer in question.answers]
        self.order_id = question.order_id
        self.text = question.text
        self.weight = question.weight


class SuitabilityModel:
    def __init__(self, suitability: SuitabilityValidator):
        self.date_time = suitability.date
        self.version = suitability.version
        self.questions = [
            Questions(question=question) for question in suitability.questions
        ]

    def get_suitability_response_template(self) -> dict:
        suitability_template = {
            "version": self.version,
            "questions": [
                {
                    "order_id": question.order_id,
                    "text": question.text,
                    "answers": [
                        {
                            "option_id": answer.option_id,
                            "text": answer.text,
                        }
                        for answer in question.answers
                    ],
                }
                for question in self.questions
            ],
        }
        return suitability_template
