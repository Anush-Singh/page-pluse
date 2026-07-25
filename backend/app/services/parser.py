from bs4 import BeautifulSoup

def parse_html(html: str) -> dict:
    soup = BeautifulSoup(html, "html.parser")

    # -------------------------
    # Page title
    # -------------------------

    title = None

    if soup.title:
        title_text = soup.title.get_text(strip=True)

        if title_text:
            title = title_text

    # -------------------------
    # Meta description
    # -------------------------

    meta_description = None

    meta_tag = soup.find(
        "meta",
        attrs={
            "name": lambda value:
                value and value.lower() == "description"
        }
    )

    if meta_tag:
        content = meta_tag.get("content")

        if content:
            meta_description = content.strip()

    # -------------------------
    # H1 count
    # -------------------------

    h1_count = len(soup.find_all("h1"))

    # -------------------------
    # Images missing alt text
    # -------------------------

    images = soup.find_all("img")

    images_missing_alt = sum(
        1
        for image in images
        if not image.get("alt", "").strip()
    )

    # -------------------------
    # Approximate word count
    # -------------------------

    # Don't count JavaScript/CSS as visible words.
    for tag in soup(["script", "style", "noscript"]):
        tag.decompose()

    visible_text = soup.get_text(
        separator=" ",
        strip=True
    )

    words = visible_text.split()

    word_count = len(words)

    return {
        "title": title,
        "meta_description": meta_description,
        "h1_count": h1_count,
        "images_missing_alt": images_missing_alt,
        "word_count": word_count,
    }