import feedparser
def sanitize_html(html):
    """ santise_html(html) returns some sanitized html.
          It can be used to try and avoid basic html insertion attacks.

        >>> sanitize_html("<p>hello</p>")
        '<p>hello</p>'
        >>> sanitize_html("<script>alert('what')</script>")
        ''
    """
    return feedparser._sanitizeHTML(html, "utf-8", "text/html")
