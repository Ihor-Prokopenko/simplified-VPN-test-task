from urllib.parse import urljoin, urlparse
from django.conf import settings

from bs4 import BeautifulSoup


def make_absolute_url(relative_url, site_name, base_site_url, base_site_domain, path):
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


def replace_links(html_content, site_name, base_site_url, base_site_domain, path):
    soup = BeautifulSoup(html_content, 'html.parser')

    for a in soup.find_all('a', href=True):
        href_value = a['href']

        a['href'] = make_absolute_url(href_value, site_name, base_site_url, base_site_domain, path)

    for tag in soup(['link'], href=True):
        tag['href'] = make_absolute_url(tag['href'], site_name, base_site_url, base_site_domain, path)

    for img in soup.find_all('img'):
        img['src'] = make_absolute_url(img['src'], site_name, base_site_url, base_site_domain, path)

    return str(soup)
