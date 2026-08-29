import re

from novelbase.utils.urls import canonical_book_url, make_novel_id


def test_make_novel_id_consistent():
    url = "https://fanqienovel.com/page/7123456789012345678"
    assert make_novel_id(url) == make_novel_id(url)


def test_make_novel_id_different_urls_differ():
    assert make_novel_id("https://fanqienovel.com/page/1") != make_novel_id("https://fanqienovel.com/page/2")


def test_make_novel_id_format_32hex():
    assert re.fullmatch(r"[0-9a-f]{32}", make_novel_id("https://x.com/y"))


def test_canonical_lowercase_and_drop_query_fragment():
    assert canonical_book_url("https://FanqieNovel.com/page/123?a=1#frag", "fanqie") \
        == "https://fanqienovel.com/page/123"


def test_canonical_trailing_slash_removed():
    assert canonical_book_url("https://fanqienovel.com/page/123/", "fanqie") \
        == "https://fanqienovel.com/page/123"
