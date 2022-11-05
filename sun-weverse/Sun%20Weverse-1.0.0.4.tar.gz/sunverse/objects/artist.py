class Artist:
    """Represents a Weverse Artist.

    .. container:: operations

        .. describe:: x == y

            Checks if two artists are equal.

        .. describe:: x != y

            Checks if two artists are not equal.

        .. describe:: hash(x)

            Returns the artist's hash.

        .. describe:: str(x)

            Returns the artist's name.

    Attributes
    ----------
    data: :class:`str`
        The raw data directly taken from the response generated by Weverse's API.
    id: :class:`str`
        The ID of the artist.
    image_url: :class:`str`
        The URL of the official image of the artist.
    name: :class:`str`
        The name of the artist.
    birthday: :class:`int`
        The artist's birthday, in epoch time.
    is_birthday: :class:`bool`
        Whether it's the artist's birthday.
    joined_date: :class:`int`
        The date the artist joined the community on, in epoch.
    nickname: :class:`str`
        The nickname of the artist.
    profile_image_url: :class:`str`
        The URL of the profile image of the artist.
    profile_banner_url: :class:`str`
        The URL of the profile banner of the artist.
    profile_comment: :class:`str` | :class:`None`
        The profile comment of the artist, if any.
    community_id: :class:`int`
        The community ID of the community the artist belongs to. This
        can be used to fetch the actual :class:`sunverse.objects.community.Community`
        object if needed using the :class:`sunverse.sunverse.SunverseClient.fetch_community()`
        method.
    """

    __slots__ = (
        "data",
        "id",
        "image_url",
        "name",
        "birthday",
        "is_birthday",
        "joined_date",
        "nickname",
        "profile_image_url",
        "profile_banner_url",
        "profile_comment",
        "community_id",
    )

    def __init__(self, data: dict):
        self.data: dict = data
        self.id: str = data["memberId"]
        self.image_url: str = data["artistOfficialProfile"]["officialImageUrl"]
        self.name: str = data["artistOfficialProfile"]["officialName"]
        self.birthday: int = data["artistOfficialProfile"]["birthday"]["date"]
        self.is_birthday: bool = data["artistOfficialProfile"]["birthday"]["bday"]
        self.joined_date: int = data["joinedDate"]
        self.nickname: str = data["profileName"]
        self.profile_image_url: str = data["profileImageUrl"]
        self.profile_banner_url: str = data["profileCoverImageUrl"]
        self.profile_comment: str | None = data.get("profileComment")
        self.community_id: int = data["communityId"]

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.id == other.id

        raise NotImplementedError

    def __repr__(self):
        return f"Artist artist_id={self.id}, name={self.name}"

    def __str__(self):
        return self.name

    def __hash__(self):
        return hash(self.id)
