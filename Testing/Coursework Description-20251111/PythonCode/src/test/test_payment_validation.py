"""The system shall display an error message if the credit card number does not meet
the 16-digit requirement or if the transaction amount is zero or negative, preventing
the transaction from proceeding."""

from PaymentService import PaymentService
import pytest


def test_valid_payment():
    # ARRANGE: Valid 16-digit card and positive amount
    payment_service = PaymentService()
    card_number = "1234567890123456"
    amount = 100.00

    # ACT & ASSERT: Payment should succeed
    result = payment_service.process_payment(card_number, amount)
    assert result is True


def test_card_less_than_16_digits():
    # ARRANGE: Card number with less than 16 digits
    payment_service = PaymentService()
    card_number = "123456789012345"  # 15 digits
    amount = 100.00

    # ACT & ASSERT: Should raise exception
    with pytest.raises(Exception) as exc_info:
        payment_service.process_payment(card_number, amount)
    assert "Payment failed" in str(exc_info.value) or "Invalid" in str(exc_info.value)


def test_card_more_than_16_digits():
    # ARRANGE: Card number with more than 16 digits
    payment_service = PaymentService()
    card_number = "12345678901234567"  # 17 digits
    amount = 100.00

    # ACT & ASSERT: Should raise exception
    with pytest.raises(Exception) as exc_info:
        payment_service.process_payment(card_number, amount)
    assert "Payment failed" in str(exc_info.value) or "Invalid" in str(exc_info.value)


def test_zero_amount():
    # ARRANGE: Valid card but zero amount
    payment_service = PaymentService()
    card_number = "1234567890123456"
    amount = 0.0

    # ACT & ASSERT: Should raise exception
    with pytest.raises(Exception) as exc_info:
        payment_service.process_payment(card_number, amount)
    assert "Payment failed" in str(exc_info.value) or "Invalid" in str(exc_info.value)


def test_negative_amount():
    # ARRANGE: Valid card but negative amount
    payment_service = PaymentService()
    card_number = "1234567890123456"
    amount = -50.00

    # ACT & ASSERT: Should raise exception
    with pytest.raises(Exception) as exc_info:
        payment_service.process_payment(card_number, amount)
    assert "Payment failed" in str(exc_info.value) or "Invalid" in str(exc_info.value)


def test_invalid_card_and_zero_amount():
    # ARRANGE: Both invalid card (15 digits) and zero amount
    payment_service = PaymentService()
    card_number = "123456789012345"  # 15 digits
    amount = 0.0

    # ACT & ASSERT: Should raise exception
    with pytest.raises(Exception) as exc_info:
        payment_service.process_payment(card_number, amount)
    assert "Payment failed" in str(exc_info.value) or "Invalid" in str(exc_info.value)


def test_invalid_card_and_negative_amount():
    # ARRANGE: Both invalid card (17 digits) and negative amount
    payment_service = PaymentService()
    card_number = "12345678901234567"  # 17 digits
    amount = -10.00

    # ACT & ASSERT: Should raise exception
    with pytest.raises(Exception) as exc_info:
        payment_service.process_payment(card_number, amount)
    assert "Payment failed" in str(exc_info.value) or "Invalid" in str(exc_info.value)


def test_empty_card_number():
    # ARRANGE: Empty card number
    payment_service = PaymentService()
    card_number = ""
    amount = 100.00

    # ACT & ASSERT: Should raise exception
    with pytest.raises(Exception) as exc_info:
        payment_service.process_payment(card_number, amount)
    assert "Payment failed" in str(exc_info.value) or "Invalid" in str(exc_info.value)


def test_very_small_positive_amount():
    # ARRANGE: Valid card with very small positive amount (edge case)
    payment_service = PaymentService()
    card_number = "1234567890123456"
    amount = 0.01

    # ACT & ASSERT: Payment should succeed
    result = payment_service.process_payment(card_number, amount)
    assert result is True


def test_large_amount():
    # ARRANGE: Valid card with large amount
    payment_service = PaymentService()
    card_number = "1234567890123456"
    amount = 999999.99

    # ACT & ASSERT: Payment should succeed
    result = payment_service.process_payment(card_number, amount)
    assert result is True
