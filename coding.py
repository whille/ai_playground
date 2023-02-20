#!/usr/bin/env python
import re
def validate_phone_number(s: str):
    # using regex
    return re.match(r'^\d{10}$', s) is not None
    if len(s) != 10:
        return False


def test_valid_phone_number():
    assert validate_phone_number("1234567890") is True
    assert validate_phone_number("123456789") is False
    assert validate_phone_number("123456789a") is False


def is_parlindrome(n):
    if n < 0:
        return False
    if n < 10:
        return True
    if n % 10 == 0:
        return False
    rev = 0
    while rev < n:
        rev = rev * 10 + n % 10
        n = n // 10
    return rev == n or rev // 10 == n


def test_is_parlindrome():
    assert is_parlindrome(121)
    assert is_parlindrome(1221)
    assert is_parlindrome(12321)
    assert not is_parlindrome(1231)
    assert not is_parlindrome(1234567890)
    assert is_parlindrome(0)
    assert is_parlindrome(1)
    assert not is_parlindrome(-1)
    assert not is_parlindrome(-121)
    assert not is_parlindrome(-1231)


def use_as_dictionary():
    {
        "en": {
            "好": "good",
            "很好": "very good",
            "迁移学习": "transfer learning",
            '忧伤': 'blue',
        },
        "ch": {
            'good': '好',
            'very good': '很好',
            'brilliant': '非常好',
            'evil': '邪恶',
            'blue': '忧伤',
            'transformer': '变形金刚',
            'token': '令牌',
            'lsh': '局部敏感哈希',
            'word2vec': '词向量',
        }
    }
