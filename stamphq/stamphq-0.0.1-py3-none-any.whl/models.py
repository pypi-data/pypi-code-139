class Attachment:
    """class that hold information about email attachment"""

    def __int__(self, name: str, content_type: str, content: str, content_id: str = None):
        assert (name and content_type and content), "name, content_type and content are mandatory"
        self.name = name
        self.content_type = content_type
        self.content = content
        self.content_id = content_id
