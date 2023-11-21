from urllib.parse import urljoin, urlparse
from django.conf import settings

from bs4 import BeautifulSoup


def make_absolute_url(relative_url: str, site_name: str, base_site_url: str, base_site_domain: str, path: str) -> str:
    """
    Generates a fully qualified absolute URL based on the provided relative URL and site information.

    Args:
        relative_url (str): The relative URL that needs to be converted to an absolute URL.
        site_name (str): The name of the site.
        base_site_url (str): The base URL of the site.
        base_site_domain (str): The base domain of the site.
        path (str): The path of the current page.

    Returns:
        str: The generated absolute URL.

    Raises:
        None

    Examples:
        >>> make_absolute_url('/about', 'example', 'https://www.example.com', 'example.com', '/home')
        'https://www.example.com/example/about'
    """
    parsed_url = urlparse(relative_url)
    vpn_site_url = settings.BASE_HOST_URL + site_name
    if relative_url.startswith('/static'):
        return urljoin(base_site_url, relative_url)
    elif relative_url.startswith('//') and base_site_domain not in parsed_url.netloc:
        return relative_url
    elif relative_url == '/' or relative_url.startswith('/'):
        query = f"/?{parsed_url.query}" if parsed_url.query else ""
        url = urljoin(settings.BASE_HOST_URL, site_name + parsed_url.path + query)
        return url
    elif 'static' in parsed_url.netloc:
        return relative_url
    elif relative_url.startswith('mailto'):
        return relative_url
    elif relative_url.startswith('javascript'):
        return relative_url
    elif relative_url.startswith('#'):
        url = urljoin(f"{vpn_site_url}/{path.lstrip('/')}", relative_url)
        return url

    elif (base_site_domain == parsed_url.netloc
          or "www." + base_site_domain == parsed_url.netloc
          or not parsed_url.netloc):
        query = f"/?{parsed_url.query}" if parsed_url.query else ""
        url = urljoin(settings.BASE_HOST_URL, site_name + parsed_url.path + query)
        return url
    return relative_url


def replace_links(html_content: str, site_name: str, base_site_url: str, base_site_domain: str, path: str) -> str:
    """
    Replaces relative links in the HTML content with absolute links using the provided site name, base site URL, base site domain, and path.

    :param html_content: The HTML content to be processed.
    :type html_content: str
    :param site_name: The name of the site.
    :type site_name: str
    :param base_site_url: The base URL of the site.
    :type base_site_url: str
    :param base_site_domain: The base domain of the site.
    :type base_site_domain: str
    :param path: The path of the current page.
    :type path: str
    :return: The modified HTML content with replaced links.
    :rtype: str
    """
    soup = BeautifulSoup(html_content, 'html.parser')

    for a in soup.find_all('a', href=True):
        href_value = a['href']

        a['href'] = make_absolute_url(href_value, site_name, base_site_url, base_site_domain, path)

    for tag in soup(['link'], href=True):
        tag['href'] = make_absolute_url(tag['href'], site_name, base_site_url, base_site_domain, path)

    for img in soup.find_all('img'):
        img['src'] = make_absolute_url(img['src'], site_name, base_site_url, base_site_domain, path)

    return str(soup)
