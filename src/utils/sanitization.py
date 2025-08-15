import bleach

ALLOWED_TAGS = [
    "p", "br", "strong", "em", "b", "i", "u", "ul", "ol", "li",
    "blockquote", "a", "h2", "h3", "h4", "hr"
]
ALLOWED_ATTRS = {"a": ["href", "title", "target", "rel"]}
ALLOWED_PROTOCOLS = ["http", "https", "mailto"]


def sanitize_html(html: str) -> str:
    return bleach.clean(
        html or "",
        tags=ALLOWED_TAGS,
        attributes=ALLOWED_ATTRS,
        protocols=ALLOWED_PROTOCOLS,
        strip=True,
    )
