import time

import httpx

class FetchError(Exception):
    """Base exception for page fetching failures."""
    pass

class RequestTimeoutError(FetchError):
    """Raised when the target website takes too long to respond."""
    pass

class NonHTMLResponseError(FetchError):
    """Raised when the URL returns something other than HTML."""
    pass

async def fetch_page(url: str) -> dict:

    start_time = time.perf_counter()

    try:

        async with httpx.AsyncClient(
            timeout=10.0,
            follow_redirects=True
        ) as client:

            response = await client.get(
                url,
                headers={
                    "User-Agent":
                        "PagePulse/1.0 Website Audit Tool"
                }
            )

    except httpx.TimeoutException as exc:

        raise RequestTimeoutError(
            "The website took too long to respond."
        ) from exc

    except httpx.RequestError as exc:

        raise FetchError(
            "Unable to connect to the requested website."
        ) from exc

    response_time_ms = round(
        (time.perf_counter() - start_time) * 1000
    )

    content_type = response.headers.get(
        "content-type",
        ""
    ).lower()

    if "text/html" not in content_type:

        raise NonHTMLResponseError(
            "The URL did not return an HTML page."
        )

    return {
        "html": response.text,
        "status_code": response.status_code,
        "response_time_ms": response_time_ms,
        "final_url": str(response.url),
    }