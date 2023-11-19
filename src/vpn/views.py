import json
from urllib.parse import urljoin, urlparse

import requests
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

from vpn.models import Site
from vpn.utils import replace_links


@login_required
def proxy(request, site_name):
    url = request.GET.get('url') if request.GET.get('url') else ""
    try:
        site = request.user.sites.get(name=site_name)
    except Site.DoesNotExist:
        return HttpResponse('Site not found')

    if not site or not site.base_url:
        return HttpResponse('Site not found')

    base_url = site.base_url
    if base_url in url:
        url = url.replace(base_url, '')

    base_domain = base_url.split('//')[-1]
    url = url.split('//')[-1]
    url = url.lstrip(f"{base_domain}")
    request_url = f"{base_url.rstrip('/')}/{url.lstrip('/')}"

    try:
        response = requests.get(request_url, headers={'User-Agent': 'Mozilla/5.0'})
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        return HttpResponse(f'Error: {e}')

    content = replace_links(response.content, site_name, site.base_url)

    return HttpResponse(content)
