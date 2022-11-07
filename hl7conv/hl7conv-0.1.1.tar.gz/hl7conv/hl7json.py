from .util import split_segments


class Hl7Json:
    def __init__(
        self,
        hl7_string: str,
        version: str | None = None,
        validate: bool = True,
        escape_empty_fields: bool = False,
    ):
        """
        Use this method to upload hl7 message from file.
        :param hl7_string: hl7 message represented as single string.
        :param version: Optional. Needed for final hl7 validation.
        :param validate: Optional. Set false if hl7 message is not related to any real version(2.5.1 etc).
        :param escape_empty_fields: Optional. Remove empty segment fields from json.
        """
        self.validate = validate
        self.version = version
        self.escape_empty_fields = escape_empty_fields
        self._hl7_string = self._replace_eof(hl7_string)

    @classmethod
    def from_file(
        cls,
        path: str,
        version: str | None = None,
        validate: bool = True,
        escape_empty_fields: bool = False,
    ):
        """
        Use this method to upload hl7 message from file.
        :param path: path to the file containing hl7 message
        :param version: Optional. Needed for final hl7 validation.
        :param validate: Optional. Set false if hl7 message is not related to any real version(2.5.1 etc).
        :param escape_empty_fields: Optional. Remove empty segment fields from json.
        """
        with open(path, mode="r") as f:
            hl7string = f.read()
        return cls(hl7string, version, validate, escape_empty_fields)

    @classmethod
    def _replace_eof(cls, hl7string) -> str:
        return hl7string.replace("\r\n", "\n").replace("\n\r", "\n").replace("\r", "\n")

    @property
    def hl7_string(self):
        return self._hl7_string

    @property
    def hl7_json(self):
        return self._convert_hl7_to_json()

    def _convert_hl7_to_json(self):
        message_json = list()
        for seg in split_segments(self.hl7_string):
            seg_json = self._split_hl7_seg_to_json(seg)
            message_json.append(seg_json)
        return message_json

    def _split_hl7_seg_to_json(self, seg: str) -> dict:
        list_of_fields = seg.split("|")
        parents_json = dict()
        for key, parent_value in enumerate(list_of_fields):
            if not key:
                key = "segment_name"
            if "^" in parent_value and "^~\\&" not in parent_value:
                children_json = self._split_hl7_parent_field_to_json(key, parent_value)
                parents_json.update(children_json)
            else:
                parents_json[str(key)] = parent_value
        return parents_json

    @staticmethod
    def _split_hl7_parent_field_to_json(parent_key: int, parent_value: str) -> dict:
        list_of_sub_fields: list = parent_value.split("^")
        children_json = dict()
        for key, value in enumerate(list_of_sub_fields, start=1):
            children_json[f"{parent_key}.{key}"] = value
        return children_json
