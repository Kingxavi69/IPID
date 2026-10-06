import argparse
import json
import socket
from typing import Any


def classify_url_type(hostname: str | None) -> str:
    """Classify the reverse-DNS hostname returned for an IP address."""
    if not hostname:
        return "Unknown"

    host = hostname.strip().lower().rstrip(".")
    if not host:
        return "Unknown"

    if any(keyword in host for keyword in ["mail", "mx", "smtp", "imap", "pop"]):
        return "Mail server"

    if any(keyword in host for keyword in ["api", "gateway", "service", "rest", "rpc"]):
        return "API"

    if any(keyword in host for keyword in ["cdn", "cache", "static", "assets", "media", "edge", "content"]):
        return "CDN / static content"

    if any(
        keyword in host
        for keyword in [
            "aws",
            "azure",
            "googlecloud",
            "cloudflare",
            "digitalocean",
            "amazonaws",
            "vercel",
            "netlify",
            "heroku",
            "linode",
        ]
    ):
        return "Cloud / hosted service"

    if host.startswith("www") or "." in host:
        return "Website"

    return "Unknown"


def resolve_ip_url(ip_address: str) -> dict[str, Any]:
    """Resolve an IP address to a hostname and classify the host type."""
    ip = ip_address.strip()
    try:
        hostname, _, _ = socket.gethostbyaddr(ip)
        url = hostname.strip().rstrip(".")
        return {
            "ip": ip,
            "url": url,
            "type": classify_url_type(url),
            "status": "resolved",
        }
    except (socket.herror, socket.gaierror, OSError):
        return {
            "ip": ip,
            "url": None,
            "type": "Unknown",
            "status": "unresolved",
        }


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Resolve an IP address to a hostname and identify the URL type."
    )
    parser.add_argument("ip", help="IPv4 or IPv6 address to inspect")
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output the result as JSON instead of a readable summary",
    )
    args = parser.parse_args()

    result = resolve_ip_url(args.ip)

    if args.json:
        print(json.dumps(result, indent=2))
        return

    if result["status"] == "resolved":
        print(f"IP Address: {result['ip']}")
        print(f"Resolved URL: {result['url']}")
        print(f"URL Type: {result['type']}")
    else:
        print(f"IP Address: {result['ip']}")
        print("Resolved URL: None")
        print("URL Type: Unknown")
        print("Status: no reverse DNS record found")


if __name__ == "__main__":
    main()
