from typing import List, Optional

from easyclient import (
    ApiAuthNone,
    RestApiClient,
    parameters as parameter_utils,
)


def _process_list(text: str) -> List[str]:
    """
    Process a comma-separated list of strings.

    :param text: The comma-separated list of strings.
    :type text: str
    :return: The list of strings.
    :rtype: List[str]
    """
    return [line.strip() for line in text.splitlines() if line.strip()]


class Client:
    def __init__(self):
        """
        Construct a new newTrackon API client.
        """
        self._client = RestApiClient(base_url="https://newtrackon.com/api",
                                     auth=ApiAuthNone())

    def stable_trackers(self, include_ipv4_only: Optional[bool] = True, include_ipv6_only: Optional[bool] = True):
        """
        Get a list of all trackers that have an uptime of equal or more than 95%

        :param include_ipv4_only: Include IPv4-only trackers only
        :type include_ipv4_only: bool
        :param include_ipv6_only: Include IPv6-only trackers only
        :type include_ipv6_only: bool
        :return: List of all stable trackers
        :rtype: List[str]
        """
        data = self._client.get_text("/stable", params={
            "include_ipv4_only_trackers": include_ipv4_only,
            "include_ipv6_only_trackers": include_ipv6_only})

        return _process_list(data)

    def trackers_with_uptime(self, uptime: int, include_ipv4_only: Optional[bool] = True,
                             include_ipv6_only: Optional[bool] = True):
        """
        Get a list of all trackers that have an uptime of equal or more than the given percentage

        :param uptime: Uptime percentage
        :type uptime: int
        :param include_ipv4_only: Include IPv4-only trackers only
        :type include_ipv4_only: bool
        :param include_ipv6_only: Include IPv6-only trackers only
        :type include_ipv6_only: bool
        :return: List of all trackers with the given uptime
        :rtype: List[str]
        """
        if not parameter_utils.in_range(uptime, 0, 100):
            raise ValueError("Uptime must be between 0 and 100")

        data = self._client.get_text(f"/{uptime}", params={
            "include_ipv4_only_trackers": include_ipv4_only,
            "include_ipv6_only_trackers": include_ipv6_only})

        return _process_list(data)

    def working_trackers(self, include_ipv4_only: Optional[bool] = True, include_ipv6_only: Optional[bool] = True):
        """
        Get a list of all currently active and responding trackers

        :param include_ipv4_only: Include IPv4-only trackers only
        :type include_ipv4_only: bool
        :param include_ipv6_only: Include IPv6-only trackers only
        :type include_ipv6_only: bool
        :return: List of all currently active and responding trackers
        :rtype: List[str]
        """
        data = self._client.get_text("/live", params={
            "include_ipv4_only_trackers": include_ipv4_only,
            "include_ipv6_only_trackers": include_ipv6_only})

        return _process_list(data)

    def udp_trackers(self, include_ipv4_only: Optional[bool] = True, include_ipv6_only: Optional[bool] = True):
        """
        Get a list of all stable UDP trackers

        :param include_ipv4_only: Include IPv4-only trackers only
        :type include_ipv4_only: bool
        :param include_ipv6_only: Include IPv6-only trackers only
        :type include_ipv6_only: bool
        :return: List of all stable UDP trackers
        :rtype: List[str]
        """
        data = self._client.get_text("/udp", params={
            "include_ipv4_only_trackers": include_ipv4_only,
            "include_ipv6_only_trackers": include_ipv6_only})

        return _process_list(data)

    def http_trackers(self, include_ipv4_only: Optional[bool] = True, include_ipv6_only: Optional[bool] = True):
        """
        Get a list of all stable HTTP/HTTPS trackers

        :param include_ipv4_only: Include IPv4-only trackers only
        :type include_ipv4_only: bool
        :param include_ipv6_only: Include IPv6-only trackers only
        :type include_ipv6_only: bool
        :return: List of all stable HTTP/HTTPS trackers
        :rtype: List[str]
        """
        data = self._client.get_text("/http", params={
            "include_ipv4_only_trackers": include_ipv4_only,
            "include_ipv6_only_trackers": include_ipv6_only})

        return _process_list(data)

    def all_trackers(self, include_ipv4_only: Optional[bool] = True, include_ipv6_only: Optional[bool] = True):
        """
        Get a list of all monitored trackers, dead or alive

        :param include_ipv4_only: Include IPv4-only trackers only
        :type include_ipv4_only: bool
        :param include_ipv6_only: Include IPv6-only trackers only
        :type include_ipv6_only: bool
        :return: List of all monitored trackers
        :rtype: List[str]
        """
        data = self._client.get_text("/all", params={
            "include_ipv4_only_trackers": include_ipv4_only,
            "include_ipv6_only_trackers": include_ipv6_only})

        return _process_list(data)

    def add_tracker(self, url: str) -> bool:
        """
        Submit new tracker to be checked and either accepted or discarded

        :param url: Tracker URL to submit
        :type url: str
        :return: True if the submission was successful, False otherwise
        :rtype: bool
        """
        return self.add_trackers([url])

    def add_trackers(self, urls: List[str]) -> bool:
        """
        Submit new trackers to be checked and either accepted or discarded

        :param urls: List of tracker URLs to submit
        :type urls: List[str]
        :return: True if the submission was successful, False otherwise
        :rtype: bool
        """
        if len(urls) == 0:
            raise ValueError("No URLs provided")

        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        data = " ".join(urls)
        res = self._client._request_handler.post("/add", data={'new_trackers': data}, headers=headers)
        if res.status_code != 200:
            raise Exception(f"Failed to add trackers: {res.text}")
        return True
