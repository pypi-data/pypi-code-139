from . import filedgr_nft_pb2 as myNft
from .exceptions.custom_exceptions import SerializationException


def serialize(
        nft_id: str,
        campaign: str,
        uri: str
) -> str:
    """
    Function Serializing a Filedgr NFT URI
    :param nft_id: The ID of the NFT. It is important to be different for each NFT.
    :param campaign: The ID of the campaign or user.
    :param uri: The URI of the NFT
    :return: Returns a Protobuf serialized message
    """
    try:
        nft = myNft.Nft()
        nft.id = nft_id
        nft.campaign = campaign
        nft.uri = uri

        result = nft.SerializeToString()
        return result
    except Exception as exc:
        raise SerializationException(exc)
