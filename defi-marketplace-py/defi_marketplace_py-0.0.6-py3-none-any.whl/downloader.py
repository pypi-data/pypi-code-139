from datetime import datetime

from defi_marketplace_py.cli_wrapper import CliWapper


class Downloader():
    """
    Class to download DeFi data from marketplace
    """

    def __init__(self, protocol: str, event_type: str, chain: str, version: int, network: str):
        self.protocol: str = protocol
        self.chain: str = chain
        self.version: int = version
        self.cli_wrapper: CliWapper = CliWapper(network=network)
        self.network: str = network
        self.event_type: str = event_type

    def download_datasets(self, from_date: str, to_date: str, destination: str, account_index: int = 1):
        datasets = self.cli_wrapper.list_assets(
            search_term=self.protocol
        )

        for dataset in datasets:
            file_name: str = dataset['fileName']
            file_name_split = file_name.split('-')
            date_and_chain = file_name_split[3].split('_')
            date = datetime.strptime(date_and_chain[1], '%Y%m%d').date()
            from_date_obj = datetime.strptime(from_date, '%Y-%m-%d').date()
            to_date_obj = datetime.strptime(to_date, '%Y-%m-%d').date()

            if (
                self.protocol == file_name_split[0] and
                self.version == int(file_name_split[1][1]) and
                self.event_type == file_name_split[2] and
                self.chain == date_and_chain[0] and
                from_date_obj <= date and
                to_date_obj >= date
            ):
                print(f'Downloading file', dataset['fileName'])
                self.download_did(
                    did=dataset['did'],
                    destination=destination,
                    account_index=account_index
                )

    def download_did(self, did, destination: str, account_index: str):
        self.cli_wrapper.download_did(
            did=did,
            destination=destination,
            account_index=account_index
        )
