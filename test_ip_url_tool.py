import socket

from ip_url_tool import classify_url_type, resolve_ip_url


def test_classify_web_url():
    assert classify_url_type("www.example.com") == "Website"
    assert classify_url_type("api.example.com") == "API"
    assert classify_url_type("mail.example.com") == "Mail server"
    assert classify_url_type("cdn.example.com") == "CDN / static content"
    assert classify_url_type("aws.amazon.com") == "Cloud / hosted service"


def test_resolve_ip_url_success(monkeypatch):
    def fake_gethostbyaddr(ip):
        assert ip == "8.8.8.8"
        return ("dns.google", [], ["8.8.8.8"])

    monkeypatch.setattr(socket, "gethostbyaddr", fake_gethostbyaddr)
    result = resolve_ip_url("8.8.8.8")

    assert result["ip"] == "8.8.8.8"
    assert result["url"] == "dns.google"
    assert result["type"] == "Website"
    assert result["status"] == "resolved"


def test_resolve_ip_url_failure(monkeypatch):
    def fake_gethostbyaddr(ip):
        raise socket.herror("No address associated with hostname")

    monkeypatch.setattr(socket, "gethostbyaddr", fake_gethostbyaddr)
    result = resolve_ip_url("203.0.113.10")

    assert result["ip"] == "203.0.113.10"
    assert result["url"] is None
    assert result["type"] == "Unknown"
    assert result["status"] == "unresolved"
