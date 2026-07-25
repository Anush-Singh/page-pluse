import ipaddress
import socket
from urllib.parse import urlparse


class UnsafeURLError(Exception):
    """Raised when a URL targets a non-public network address."""
    pass


def validate_public_url(url: str) -> None:

    parsed = urlparse(url)

    if parsed.scheme not in {"http", "https"}:
        raise UnsafeURLError(
            "Only HTTP and HTTPS URLs are allowed."
        )

    hostname = parsed.hostname

    if not hostname:
        raise UnsafeURLError(
            "The URL must contain a valid hostname."
        )

    try:
        addresses = socket.getaddrinfo(
            hostname,
            None
        )

    except socket.gaierror as exc:
        raise UnsafeURLError(
            "The hostname could not be resolved."
        ) from exc

    for address in addresses:

        ip_string = address[4][0]

        ip = ipaddress.ip_address(
            ip_string
        )

        if not ip.is_global:
            raise UnsafeURLError(
                "URLs pointing to private or "
                "local network addresses are not allowed."
            )