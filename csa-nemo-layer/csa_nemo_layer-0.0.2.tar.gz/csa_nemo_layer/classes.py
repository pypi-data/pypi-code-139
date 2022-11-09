class Finding:
    def __init__(self, **kwargs) -> None:
        """
        Class for CSA Nemo project's findings
        :params:
        id: string
        target: string
        controlId: string
        Reason: list of strings
        Identifier: string
        """
        self.id = kwargs.get('id')
        self.target = kwargs.get('target', '')
        self.controlId = kwargs.get('controlId', '')
        self.Reason = []
        self.Identifier = kwargs.get('identifier', '')

    def json(self) -> dict:
        self.Reason = set(self.Reason)
        return self.__dict__

# TO-DO: Add classes for targets
