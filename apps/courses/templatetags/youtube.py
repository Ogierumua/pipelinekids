from django import template
from urllib.parse import urlparse, parse_qs

register = template.Library()

@register.filter
def youtube_id(url):
    if not url:
        return ""

    parsed = urlparse(url)

    # youtu.be/<id>?...
    if parsed.netloc in ("youtu.be", "www.youtu.be"):
        return parsed.path.lstrip("/").split("/")[0]

    # youtube.com/watch?v=<id>
    if "youtube.com" in parsed.netloc:
        qs = parse_qs(parsed.query)
        if "v" in qs:
            return qs["v"][0]

        # youtube.com/embed/<id>
        if parsed.path.startswith("/embed/"):
            return parsed.path.split("/embed/")[1].split("/")[0]

    return ""
