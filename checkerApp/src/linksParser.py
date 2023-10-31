import typing
from urllib.parse import urlparse


def get_unique_domains_from_links(links: typing.List[str]) -> typing.List[str]:
    """
    Getting list of domains
    :param links:
    :return: list of domains
    """
    raise ValueError('hi by')
    # return list({
    #     urlparse(link).netloc
    #     for link in links
    #     if urlparse(link).netloc
    # })
