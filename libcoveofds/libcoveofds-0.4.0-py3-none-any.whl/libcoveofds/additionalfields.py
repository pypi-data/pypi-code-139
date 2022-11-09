from libcove2.common import get_additional_fields_info, get_counts_additional_fields
from libcoveofds.schema import OFDSSchema


class AdditionalFields:
    def __init__(self, schema: OFDSSchema):
        self._schema = schema

    def process(self, json_data: dict) -> list:

        schema_fields = self._schema.get_package_schema_fields()

        additional_fields_all = get_additional_fields_info(json_data, schema_fields)

        additional_fields = sorted(
            get_counts_additional_fields(
                json_data,
                schema_fields,
                additional_fields_info=additional_fields_all,
            )
        )

        return additional_fields
