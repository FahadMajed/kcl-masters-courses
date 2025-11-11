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
    cart.apply_coupon("INVALID123")

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
    cart.apply_coupon("")

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
    cart.apply_coupon("discount10")  # lowercase

    # ASSERT: Should check if case matters
    # If case-insensitive: 450.00, if case-sensitive: 500.00
    assert cart.calculate_total() == 500.00
    # Expecting no discount if case-sensitive
    assert cart.calculate_final_price() == 500.00
