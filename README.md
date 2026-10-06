# IP URL Disclosure Tool

This project contains a lightweight Python utility that resolves an IP address to its reverse-DNS hostname and labels the result as a website, API, mail server, cloud service, CDN/static host, or unknown.

## Usage

```bash
python ip_url_tool.py 8.8.8.8
```

Example output:

```text
IP Address: 8.8.8.8
Resolved URL: dns.google
URL Type: Website
```

JSON output:

```bash
python ip_url_tool.py 8.8.8.8 --json
```

## Notes

- The tool uses Python's standard `socket.gethostbyaddr()` reverse lookup.
- Some IP addresses will not have a reverse DNS record, in which case the URL is reported as unknown.
