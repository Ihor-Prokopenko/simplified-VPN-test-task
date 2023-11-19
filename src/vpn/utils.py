from django.conf import settings

from bs4 import BeautifulSoup


def make_absolute_url(relative_url, site_name, base_url):
    if relative_url.startswith(('http://', 'https://')):
        return relative_url
    if relative_url.startswith('//'):
        return 'http:' + relative_url
    return f'{settings.BASE_HOST_URL}/{site_name}?url={base_url}/{relative_url.lstrip("/")}'


def replace_links(html_content, site_name, base_url):
    soup = BeautifulSoup(html_content, 'html.parser')

    for a in soup.find_all('a', href=True):
        href_value = a['href']

        link = f"?url={href_value}"

        if not href_value.startswith(('http://', 'https://', '//')) or base_url not in href_value:
            link = make_absolute_url(href_value, site_name, base_url)

        a['href'] = link

    return str(soup)
