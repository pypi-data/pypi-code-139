from web3cli.core.models.address import Address
from web3cli.core.exceptions import AddressNotFound


def get_address(label: str) -> str:
    """Return the address with the given label; raise error
    if no such address is found"""
    address = Address.get_by_label(label)
    if not address:
        raise AddressNotFound(f"Address '{label}' does not exist")
    return address.address
