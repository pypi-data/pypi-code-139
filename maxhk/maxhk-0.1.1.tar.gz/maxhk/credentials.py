from maxhk import op


class Credentials:
    @staticmethod
    def pypi():
        return op.get_item("pypi.org")

    @staticmethod
    def ha_token():
        return op.get_item("HomeAssistant pyscript")
