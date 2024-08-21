class CustomerRegistrationBuilder:
    def __init__(self, user_data: dict):
        self.__user_data = user_data
        self.__buffer = {
            "personal": {},
            "marital": {"spouse": {}},
            "documents": {},
            "address": {},
            "external_exchange_account_us": {},
        }

    def personal_name(self):
        name = self.__user_data.get("name")
        self.__buffer["personal"].update({"name": name})
        return self

    def personal_nick_name(self):
        nick_name = self.__user_data.get("nick_name")
        self.__buffer["personal"].update({"nick_name": nick_name})
        return self

    def personal_birth_date(self):
        birth_date = self.__user_data.get("birth_date")
        self.__buffer["personal"].update({"birth_date": birth_date})
        return self

    def personal_parentage(self):
        father_name = self.__user_data.get("father_name")
        self.__buffer["personal"].update({"father_name": father_name})
        mother_name = self.__user_data.get("mother_name")
        self.__buffer["personal"].update({"mother_name": mother_name})
        return self

    def personal_gender(self):
        gender = self.__user_data.get("gender")
        self.__buffer["personal"].update({"gender": gender})
        return self

    def personal_email(self):
        email = self.__user_data.get("email")
        self.__buffer["personal"].update({"email": email})
        return self

    def personal_phone(self):
        phone = self.__user_data.get("phone")
        self.__buffer["personal"].update({"phone": phone})
        return self

    def personal_nationality(self):
        nationality = self.__user_data.get("nationality")
        self.__buffer["personal"].update({"nationality": nationality})
        return self

    def personal_patrimony(self):
        patrimony = self.__user_data.get("assets", {}).get("patrimony")
        self.__buffer["personal"].update({"patrimony": patrimony})
        return self

    def personal_income(self):
        income = self.__user_data.get("assets", {}).get("income")
        self.__buffer["personal"].update({"income": income})
        return self

    def personal_us_person(self):
        us_person = self.__user_data.get("us_person")
        self.__buffer["personal"].update({"us_person": us_person})
        return self

    def personal_occupation_activity(self):
        occupation_activity = self.__user_data.get("occupation", {}).get("activity")

        self.__buffer["personal"].update({"occupation_activity": occupation_activity})
        return self

    def personal_company_name(self):
        company_name = (
            self.__user_data.get("occupation", {}).get("company", {}).get("name")
        )
        self.__buffer["personal"].update({"company_name": company_name})
        return self

    def personal_company_cnpj(self):
        company_cnpj = (
            self.__user_data.get("occupation", {}).get("company", {}).get("cnpj")
        )
        self.__buffer["personal"].update({"company_cnpj": company_cnpj})
        return self

    def marital_status(self):
        marital_status = self.__user_data.get("marital", {}).get("status")
        self.__buffer["marital"].update({"status": marital_status})
        return self

    def marital_spouse_name(self):
        spouse = self.__user_data.get("marital", {}).get("spouse")
        if spouse:
            spouse_name = spouse.get("name")
            self.__buffer["marital"]["spouse"].update({"spouse_name": spouse_name})
        return self

    def marital_spouse_cpf(self):
        spouse = self.__user_data.get("marital", {}).get("spouse")
        if spouse:
            spouse_cpf = spouse.get("cpf")
            self.__buffer["marital"]["spouse"].update({"spouse_cpf": spouse_cpf})
        return self

    def marital_nationality(self):
        spouse = self.__user_data.get("marital", {}).get("spouse")
        if spouse:
            nationality = spouse.get("nationality")
            self.__buffer["marital"]["spouse"].update({"nationality": nationality})
        return self

    def documents_cpf(self):
        cpf = self.__user_data.get("identifier_document", {}).get("cpf")
        self.__buffer["documents"].update({"cpf": cpf})
        return self

    def documents_identity_type(self):
        identity_type = (
            self.__user_data.get("identifier_document", {})
            .get("document_data", {})
            .get("type")
        )
        self.__buffer["documents"].update({"identity_type": identity_type})
        return self

    def documents_identity_number(self):
        identity_number = (
            self.__user_data.get("identifier_document", {})
            .get("document_data", {})
            .get("number")
        )
        self.__buffer["documents"].update({"identity_number": identity_number})
        return self

    def documents_issuer(self):
        issuer = (
            self.__user_data.get("identifier_document", {})
            .get("document_data", {})
            .get("issuer")
        )
        self.__buffer["documents"].update({"issuer": issuer})
        return self

    def personal_tax_residences(self):
        tax_residences = self.__user_data.get("tax_residences")
        self.__buffer["personal"].update({"tax_residences": tax_residences})
        return self

    def personal_birth_place_country(self):
        birth_place_country = self.__user_data.get("birth_place_country")
        self.__buffer["personal"].update({"birth_place_country": birth_place_country})
        return self

    def personal_birth_place_city(self):
        birth_place_city = self.__user_data.get("birth_place_city")
        self.__buffer["personal"].update({"birth_place_city": birth_place_city})
        return self

    def personal_birth_place_state(self):
        birth_place_state = self.__user_data.get("birth_place_state")
        self.__buffer["personal"].update({"birth_place_state": birth_place_state})
        return self

    def documents_state(self):
        state = (
            self.__user_data.get("identifier_document", {})
            .get("document_data", {})
            .get("state")
        )
        self.__buffer["documents"].update({"state": state})
        return self

    def address_country(self):
        country = self.__user_data.get("address", {}).get("country")
        self.__buffer["address"].update({"country": country})
        return self

    def address_number(self):
        number = self.__user_data.get("address", {}).get("number")
        self.__buffer["address"].update({"number": number})
        return self

    def address_street_name(self):
        street_name = self.__user_data.get("address", {}).get("street_name")
        self.__buffer["address"].update({"street_name": street_name})
        return self

    def address_city(self):
        city = self.__user_data.get("address", {}).get("city")
        self.__buffer["address"].update({"city": city})
        return self

    def address_neighborhood(self):
        neighborhood = self.__user_data.get("address", {}).get("neighborhood")
        self.__buffer["address"].update({"neighborhood": neighborhood})
        return self

    def address_zip_code(self):
        zip_code = self.__user_data.get("address", {}).get("zip_code")
        self.__buffer["address"].update({"zip_code": zip_code})
        return self

    def address_state(self):
        state = self.__user_data.get("address", {}).get("state")
        self.__buffer["address"].update({"state": state})
        return self

    def address_phone(self):
        state = self.__user_data.get("address", {}).get("phone")
        self.__buffer["address"].update({"phone": state})
        return self

    def address_complement(self):
        state = self.__user_data.get("address", {}).get("complement")
        self.__buffer["address"].update({"complement": state})
        return self

    def external_exchange_account_politically_exposed_us(self):
        is_politically_exposed = (
            self.__user_data.get("external_exchange_requirements", {})
            .get("us", {})
            .get("is_politically_exposed")
        )
        if is_politically_exposed is not None:
            self.__buffer["external_exchange_account_us"].update(
                {"is_politically_exposed": is_politically_exposed}
            )
        return self

    def external_exchange_account_exchange_member_us(self):
        is_exchange_member = (
            self.__user_data.get("external_exchange_requirements", {})
            .get("us", {})
            .get("is_exchange_member")
        )
        if is_exchange_member is not None:
            self.__buffer["external_exchange_account_us"].update(
                {"is_exchange_member": is_exchange_member}
            )
        return self

    def external_exchange_account_time_experience_us(self):
        time_experience = (
            self.__user_data.get("external_exchange_requirements", {})
            .get("us", {})
            .get("time_experience")
        )
        if time_experience is not None:
            self.__buffer["external_exchange_account_us"].update(
                {"time_experience": time_experience}
            )
        return self

    def external_exchange_account_company_director_us(self):
        is_company_director = (
            self.__user_data.get("external_exchange_requirements", {})
            .get("us", {})
            .get("is_company_director")
        )
        is_company_director_of = (
            self.__user_data.get("external_exchange_requirements", {})
            .get("us", {})
            .get("is_company_director_of")
        )
        if is_company_director is not None:
            self.__buffer["external_exchange_account_us"].update(
                {"is_company_director": is_company_director}
            )
            self.__buffer["external_exchange_account_us"].update(
                {"is_company_director_of": is_company_director_of}
            )
        return self

    def external_exchange_account_user_employ_company_name_us(self):
        time_experience = (
            self.__user_data.get("external_exchange_requirements", {})
            .get("us", {})
            .get("user_employ_company_name")
        )
        if time_experience is not None:
            self.__buffer["external_exchange_account_us"].update(
                {"user_employ_company_name": time_experience}
            )
        return self

    def external_exchange_account_user_employ_position_us(self):
        time_experience = (
            self.__user_data.get("external_exchange_requirements", {})
            .get("us", {})
            .get("user_employ_position")
        )
        if time_experience is not None:
            self.__buffer["external_exchange_account_us"].update(
                {"user_employ_position": time_experience}
            )
        return self

    def external_exchange_account_user_employ_type_us(self):
        time_experience = (
            self.__user_data.get("external_exchange_requirements", {})
            .get("us", {})
            .get("user_employ_type")
        )
        if time_experience is not None:
            self.__buffer["external_exchange_account_us"].update(
                {"user_employ_type": time_experience}
            )
        return self

    def external_exchange_account_user_employ_status_us(self):
        time_experience = (
            self.__user_data.get("external_exchange_requirements", {})
            .get("us", {})
            .get("user_employ_status")
        )
        if time_experience is not None:
            self.__buffer["external_exchange_account_us"].update(
                {"user_employ_status": time_experience}
            )
        return self

    def build(self) -> dict:
        (
            self.personal_name()
            .personal_nick_name()
            .personal_birth_date()
            .personal_gender()
            .personal_parentage()
            .personal_email()
            .personal_phone()
            .personal_nationality()
            .personal_occupation_activity()
            .personal_company_name()
            .personal_company_cnpj()
            .personal_patrimony()
            .personal_income()
            .personal_us_person()
            .personal_tax_residences()
            .personal_birth_place_country()
            .personal_birth_place_city()
            .personal_birth_place_state()
            .marital_status()
            .marital_spouse_name()
            .marital_spouse_cpf()
            .marital_nationality()
            .documents_cpf()
            .documents_identity_type()
            .documents_identity_number()
            .documents_issuer()
            .documents_state()
            .address_country()
            .address_number()
            .address_street_name()
            .address_city()
            .address_neighborhood()
            .address_zip_code()
            .address_state()
            .address_phone()
            .address_complement()
            .external_exchange_account_politically_exposed_us()
            .external_exchange_account_exchange_member_us()
            .external_exchange_account_time_experience_us()
            .external_exchange_account_company_director_us()
            .external_exchange_account_user_employ_company_name_us()
            .external_exchange_account_user_employ_position_us()
            .external_exchange_account_user_employ_type_us()
            .external_exchange_account_user_employ_status_us()
        )
        return self.__buffer
