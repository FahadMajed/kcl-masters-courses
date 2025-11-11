"""The system shall allow users to enter a single coupon code per transaction. Available
coupons:
• "DISCOUNT10" for 10% off
• "SAVE50" for £50 off.
"""

from ShoppingCart import ShoppingCart
from CartItem import CartItem
from Product import Product
from Customer import Customer
from DiscountService import DiscountService
from CustomerType import CustomerType


def test_no_coupon_code():
    # ARRANGE: Cart without any coupon code
    mouse = Product("Mouse", 500.00, 20)
    customer = Customer("John", CustomerType.REGULAR)
    cart = ShoppingCart(customer, DiscountService())

    # ACT
    cart.add_item(CartItem(mouse, 1))

    # ASSERT: No coupon, no discount
    assert cart.calculate_total() == 500.00
    assert cart.calculate_final_price() == 500.00


def test_discount10_coupon():
    # ARRANGE: Cart with DISCOUNT10 coupon (10% off)
    mouse = Product("Mouse", 500.00, 20)
    customer = Customer("Jane", CustomerType.REGULAR)
    cart = ShoppingCart(customer, DiscountService())

    # ACT
    cart.add_item(CartItem(mouse, 1))
    cart.apply_coupon_code("DISCOUNT10")

    # ASSERT: 10% discount applied
    # Expected: 500 * 0.90 = 450.00
    assert cart.calculate_total() == 500.00
    assert cart.calculate_final_price() == 450.00


def test_save50_coupon():
    # ARRANGE: Cart with SAVE50 coupon (£50 off)
    mouse = Product("Mouse", 500.00, 20)
    customer = Customer("Alice", CustomerType.REGULAR)
    cart = ShoppingCart(customer, DiscountService())

    # ACT
    cart.add_item(CartItem(mouse, 1))
    cart.apply_coupon_code("SAVE50")

    # ASSERT: £50 flat discount applied
    # Expected: 500 - 50 = 450.00
    assert cart.calculate_total() == 500.00
    assert cart.calculate_final_price() == 450.00


def test_invalid_coupon_code():
    # ARRANGE: Cart with invalid coupon code
    mouse = Product("Mouse", 500.00, 20)
    customer = Customer("Bob", CustomerType.REGULAR)
    cart = ShoppingCart(customer, DiscountService())

    # ACT
    cart.add_item(CartItem(mouse, 1))
    cart.apply_coupon_code("INVALID123")

    # ASSERT: Invalid coupon, no discount applied
    assert cart.calculate_total() == 500.00
    assert cart.calculate_final_price() == 500.00


def test_empty_coupon_code():
    # ARRANGE: Cart with empty string coupon
    mouse = Product("Mouse", 500.00, 20)
    customer = Customer("Charlie", CustomerType.REGULAR)
    cart = ShoppingCart(customer, DiscountService())

    # ACT
    cart.add_item(CartItem(mouse, 1))
    cart.apply_coupon_code("")

    # ASSERT: Empty coupon, no discount applied
    assert cart.calculate_total() == 500.00
    assert cart.calculate_final_price() == 500.00


def test_discount10_with_multiple_items():
    # ARRANGE: Multiple items with DISCOUNT10 coupon
    mouse = Product("Mouse", 100.00, 20)
    keyboard = Product("Keyboard", 150.00, 15)
    customer = Customer("David", CustomerType.REGULAR)
    cart = ShoppingCart(customer, DiscountService())

    # ACT
    cart.add_item(CartItem(mouse, 2))
    cart.add_item(CartItem(keyboard, 1))
    cart.apply_coupon_code("DISCOUNT10")

    # ASSERT: 10% discount on total
    # Total: 100*2 + 150 = 350
    # Expected: 350 * 0.90 = 315.00
    assert cart.calculate_total() == 350.00
    assert cart.calculate_final_price() == 315.00


def test_save50_with_multiple_items():
    # ARRANGE: Multiple items with SAVE50 coupon
    mouse = Product("Mouse", 100.00, 20)
    keyboard = Product("Keyboard", 150.00, 15)
    customer = Customer("Eve", CustomerType.REGULAR)
    cart = ShoppingCart(customer, DiscountService())

    # ACT
    cart.add_item(CartItem(mouse, 2))
    cart.add_item(CartItem(keyboard, 1))
    cart.apply_coupon_code("SAVE50")

    # ASSERT: £50 flat discount
    # Total: 100*2 + 150 = 350
    # Expected: 350 - 50 = 300.00
    assert cart.calculate_total() == 350.00
    assert cart.calculate_final_price() == 300.00


def test_case_sensitivity_discount10():
    # ARRANGE: Test if coupon code is case sensitive
    mouse = Product("Mouse", 500.00, 20)
    customer = Customer("Frank", CustomerType.REGULAR)
    cart = ShoppingCart(customer, DiscountService())

    # ACT
    cart.add_item(CartItem(mouse, 1))
    cart.apply_coupon_code("discount10")  # lowercase

    # ASSERT: Should check if case matters
    # If case-insensitive: 450.00, if case-sensitive: 500.00
    assert cart.calculate_total() == 500.00
    # Expecting no discount if case-sensitive
    assert cart.calculate_final_price() == 500.00


def test_single_coupon_per_transaction():
    # ARRANGE: Test that only ONE coupon can be applied per transaction
    mouse = Product("Mouse", 1000.00, 20)
    customer = Customer("Grace", CustomerType.REGULAR)
    cart = ShoppingCart(customer, DiscountService())

    # ACT: Try to apply two coupons
    cart.add_item(CartItem(mouse, 1))
    cart.apply_coupon_code("DISCOUNT10")  # First coupon: 10% off → 900
    cart.apply_coupon_code("SAVE50")      # Second coupon: £50 off → 950

    # ASSERT: Only ONE coupon should be applied (the last one or first one, depending on implementation)
    # If last one wins: 1000 - 50 = 950
    # If first one wins: 1000 * 0.90 = 900
    # If both applied (BUG): 1000 * 0.90 - 50 = 850 or 1000 - 50 * 0.90 = 955
    assert cart.calculate_total() == 1000.00
    # Expected: Only one coupon should apply
    # Based on ShoppingCart implementation, last coupon should overwrite first
    final_price = cart.calculate_final_price()
    assert final_price == 950.00  # Last coupon (SAVE50) should win
