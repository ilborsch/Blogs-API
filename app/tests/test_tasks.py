import pytest
import random
from string import ascii_letters
from app.blog.repository import tasks


def test_validate_email_1():
    valid_email_1 = "test_email@email.com"
    valid_email_2 = "123@gmai.ua"
    valid_email_3 = "t@aa.ac"
    valid_email_4 = "d123d123@123123.12"

    invalid_email_1 = "123.123.123.123:8080"
    invalid_email_2 = "string"
    invalid_email_3 = "invalid_email@gmail"
    invalid_email_4 = "invalid_email2&gmail.com"

    assert tasks.validate_email(valid_email_1) is True
    assert tasks.validate_email(valid_email_2) is True
    assert tasks.validate_email(valid_email_3) is True
    assert tasks.validate_email(valid_email_4) is True

    assert tasks.validate_email(invalid_email_1) is False
    assert tasks.validate_email(invalid_email_2) is False
    assert tasks.validate_email(invalid_email_3) is False
    assert tasks.validate_email(invalid_email_4) is False


def test_validate_email_random():
    chars = ascii_letters + "-."
    for i in range(100):
        email = "".join(random.choices(chars, k=random.randint(1, 40))) + \
                "@" + "".join(random.choices(ascii_letters, k=random.randint(1, 40))) + \
                "." + "".join(random.choices(ascii_letters, k=random.randint(2, 4)))

        assert tasks.validate_email(email) is True



