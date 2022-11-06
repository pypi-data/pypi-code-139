from pydantic_custom_types.base_name import BaseName


class NamespaceName(BaseName):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate_namespace_name

    @classmethod
    def validate_namespace_name(cls, name: str) -> str:
        cls.base_name_validate(name)
        return name

    @classmethod
    def has_to_many_characters(cls, name: str):
        max_length = 64
        if len(name) >= max_length:
            raise ValueError(f"Name cannot be longer than {max_length} characters")

        return name
