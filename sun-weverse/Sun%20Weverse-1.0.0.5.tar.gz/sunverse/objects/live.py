from sunverse.objects.media import WeverseMedia


class Live(WeverseMedia):
    """Represents a Weverse Live Broadcast.
    Inherits from :class:`objects.media.WeverseMedia`.

    Shares the same attributes with :class:`objects.post.Postlike`,
    :class:`objects.media.Medialike` and :class:`objects.media.WeverseMedia`.

    Attributes
    ----------
    message_count: :class:`int` | :class:`None`
        The number of messages in the live broadcast, if any.
    """

    __slots__ = ("message_count",)

    def __init__(self, data: dict):
        super().__init__(data)
        self.message_count: int | None = (
            data["extension"]["mediaInfo"]["chat"]["messageCount"]
            if data["extension"]["mediaInfo"].get("chat")
            else None
        )

    def __repr__(self):
        return f"Live live_id={self.id}, title={self.title}"
