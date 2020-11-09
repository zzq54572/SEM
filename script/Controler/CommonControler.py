
from urllib.parse import urlparse, urljoin
from flask import render_template, url_for, redirect


def redirect_back( request,default='home', **kwargs):
    for target in request.args.get('next'), request.referrer:
        if not target:
            continue
        if is_safe_url(request,target):
            return redirect(target)
    return redirect(url_for(default, **kwargs))

def is_safe_url(request,target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc