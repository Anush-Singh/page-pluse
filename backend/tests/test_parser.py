from app.services.parser import parse_html


def test_parse_complete_html():
    html = """
    <html>
        <head>
            <title>Page Pulse Test</title>
            <meta
                name="description"
                content="A test webpage."
            >
        </head>

        <body>
            <h1>Main Heading</h1>

            <p>Hello from Page Pulse.</p>

            <img
                src="good.jpg"
                alt="Mountain landscape"
            >

            <img src="bad.jpg">

            <img
                src="empty.jpg"
                alt=""
            >
        </body>
    </html>
    """

    result = parse_html(html)

    assert result["title"] == "Page Pulse Test"
    assert result["meta_description"] == "A test webpage."
    assert result["h1_count"] == 1
    assert result["images_missing_alt"] == 2

def test_missing_title_and_description():
    html = """
    <html>
        <head></head>

        <body>
            <h1>Hello</h1>
            <p>Some page content.</p>
        </body>
    </html>
    """

    result = parse_html(html)

    assert result["title"] is None
    assert result["meta_description"] is None
    assert result["h1_count"] == 1

def test_multiple_h1_elements():
    html = """
    <html>
        <body>
            <h1>First Heading</h1>
            <h1>Second Heading</h1>
            <h1>Third Heading</h1>
            <h2>Not an H1</h2>
        </body>
    </html>
    """

    result = parse_html(html)

    assert result["h1_count"] == 3

def test_images_missing_alt():
    html = """
    <html>
        <body>

            <img
                src="one.jpg"
                alt="A valid description"
            >

            <img src="two.jpg">

            <img
                src="three.jpg"
                alt=""
            >

            <img
                src="four.jpg"
                alt="   "
            >

        </body>
    </html>
    """
    result = parse_html(html)

    assert result["images_missing_alt"] == 3

def test_word_count_ignores_script_and_style():
    html = """
    <html>

        <head>
            <style>
                body display flex hidden words
            </style>
        </head>

        <body>

            <p>
                One two three four five.
            </p>

            <script>
                these javascript words
                should not count
            </script>

        </body>

    </html>
    """

    result = parse_html(html)

    assert result["word_count"] == 5