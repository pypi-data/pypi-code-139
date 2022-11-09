from typing import List, Union


class FieldNameFixer:
    def __init__(self):
        self.__field_name_max_length = 128

    def __fix_field_name(self, field_name: str) -> str:
        return field_name[: self.__field_name_max_length]

    def __fix_field_names(self, field_names: List[str]) -> List[str]:
        return [self.__fix_field_name(field_name) for field_name in field_names]

    def fix(self, field_names: Union[str, List[str]]) -> Union[str, List[str]]:
        if isinstance(field_names, list):
            return self.__fix_field_names(field_names)

        return self.__fix_field_name(field_names)
