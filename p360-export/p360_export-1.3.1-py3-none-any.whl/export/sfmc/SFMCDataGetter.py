from typing import Dict, Any
from p360_export.export.sfmc.FieldNameFixer import FieldNameFixer

from p360_export.export.sfmc.SFMCData import SFMCData
from p360_export.utils.SecretGetterInterface import SecretGetterInterface


class SFMCDataGetter:
    def __init__(self, secret_getter: SecretGetterInterface, field_name_fixer: FieldNameFixer):
        self.__secret_getter = secret_getter
        self.__field_name_fixer = field_name_fixer

    def __fix_fields_names(self, config: Dict[str, Any]):
        config["params"]["export_columns"] = self.__field_name_fixer.fix(config["params"]["export_columns"])
        config["params"]["mapping"]["subscriber_key"] = self.__field_name_fixer.fix(config["params"]["mapping"]["subscriber_key"])

    def get(self, config: Dict[str, Any]):
        self.__fix_fields_names(config)

        return SFMCData(
            client_secret=self.__secret_getter.get(key=config["credentials"]["client_secret_key"]),
            ftp_password=self.__secret_getter.get(key=config["credentials"]["ftp_password_key"]),
            config=config,
        )
