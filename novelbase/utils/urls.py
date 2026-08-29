"""URL 规范化与 Novel.id 生成工具（Novel.id = sha256(canonical_url)[:32]）。"""

import hashlib
from urllib.parse import urlsplit, urlunsplit


def canonical_book_url(url: str, platform: str) -> str:
    """书源完整 URL 规范化：小写 scheme/host、去 query/fragment、去尾斜杠。"""
    parts = urlsplit(url.strip())
    scheme = parts.scheme.lower()
    netloc = parts.netloc.lower()
    path = parts.path
    if path not in ("", "/"):
        path = path.rstrip("/")
    result = urlunsplit((scheme, netloc, path, "", ""))
    return result


def make_novel_id(canonical_url: str) -> str:
    """由 canonical url 生成 32 位 hex 的 Novel.id（sha256 前 32 字符）。"""
    return hashlib.sha256(canonical_url.encode("utf-8")).hexdigest()[:32]
