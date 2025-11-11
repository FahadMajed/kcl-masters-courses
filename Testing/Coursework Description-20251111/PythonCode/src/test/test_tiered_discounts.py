"""
The  system  shall  apply  tiered  discounts  based  on 
the  cart  subtotal  after  bundle 
discounts: 
• 15% off if the subtotal exceeds £2,000 
• 20% off if the subtotal exceeds £7,000 
• 25% off if the subtotal exceeds £15,000
"""

from ShoppingCart import ShoppingCart
from CartItem import CartItem
from Product import Product
from Customer import Customer
from DiscountService import DiscountService
from CustomerType import CustomerType


def test_no_tiered_discount_below_threshold():
    # ARRANGE: Subtotal below £2000, should not trigger any tiered discount
    mouse = Product("Mouse", 500.00, 20)
    customer = Customer("John", CustomerType.REGULAR)
    cart = ShoppingCart(customer, DiscountService())

    # ACT
    cart.add_item(CartItem(mouse, 1))

    # ASSERT: Subtotal is £500, no tiered discount should apply
    assert cart.calculate_total() == 500.00
    assert cart.calculate_final_price() == 500.00


def test_no_discount_at_1999():
    # ARRANGE: Subtotal at £1999, does NOT exceed £2000, should not get discount
    mouse = Product("Mouse", 1999.00, 20)
    customer = Customer("John", CustomerType.REGULAR)
    cart = ShoppingCart(customer, DiscountService())

    # ACT
    cart.add_item(CartItem(mouse, 1))

    # ASSERT: 1999 does NOT exceed 2000, no tiered discount should apply
    assert cart.calculate_total() == 1999.00
    assert cart.calculate_final_price() == 1999.00


def test_apply_15_without_bundle():
    # ARRANGE: Subtotal above £2000 to trigger 15% discount
    mouse = Product("Mouse", 2001.00, 20)
    customer = Customer("John", CustomerType.REGULAR)
    cart = ShoppingCart(customer, DiscountService())

    # ACT
    cart.add_item(CartItem(mouse, 1))

    # ASSERT: 2001 exceeds 2000, should get 15% off
    assert cart.calculate_total() == 2001.00
    # Expected: 2001 * 0.85 = 1700.85
    assert cart.calculate_final_price() == 1700.85


def test_apply_15_with_bundle():
    # ARRANGE: Test with bundle discount that pushes subtotal above £2000
    laptop = Product("Laptop", 1500.00, 10)
    mouse = Product("Mouse", 600.00, 20)
    customer = Customer("John", CustomerType.REGULAR)
    cart = ShoppingCart(customer, DiscountService())

    # ACT
    cart.add_item(CartItem(laptop, 1))
    cart.add_item(CartItem(mouse, 1))

    # ASSERT
    # Total before any discount: 1500 + 600 = 2100
    # Bundle discount: 10% off mouse = 60
    # Subtotal after bundle: 2100 - 60 = 2040
    # Since 2040 > 2000, apply 15% tiered discount
    # Final: 2040 * 0.85 = 1734
    assert cart.calculate_total() == 2100.00
    assert cart.calculate_final_price() == 1734.00


def test_apply_20_without_bundle():
    # ARRANGE: Subtotal above £7000 to trigger 20% discount
    mouse = Product("Mouse", 7001.00, 20)
    customer = Customer("John", CustomerType.REGULAR)
    cart = ShoppingCart(customer, DiscountService())

    # ACT
    cart.add_item(CartItem(mouse, 1))

    # ASSERT: 7001 exceeds 7000, should get 20% off
    assert cart.calculate_total() == 7001.00
    # Expected: 7001 * 0.80 = 5600.80
    assert cart.calculate_final_price() == 5600.80


def test_apply_20_with_bundle():
    # ARRANGE: Test with bundle discount that pushes subtotal above £7000
    laptop = Product("Laptop", 5000.00, 10)
    mouse = Product("Mouse", 2500.00, 20)
    customer = Customer("John", CustomerType.REGULAR)
    cart = ShoppingCart(customer, DiscountService())

    # ACT
    cart.add_item(CartItem(laptop, 1))
    cart.add_item(CartItem(mouse, 1))

    # ASSERT
    # Total before any discount: 5000 + 2500 = 7500
    # Bundle discount: 10% off mouse = 250
    # Subtotal after bundle: 7500 - 250 = 7250
    # Since 7250 > 7000, apply 20% tiered discount
    # Final: 7250 * 0.80 = 5800
    assert cart.calculate_total() == 7500.00
    assert cart.calculate_final_price() == 5800.00


def test_apply_25_without_bundle():
    # ARRANGE: Subtotal above £15000 to trigger 25% discount
    mouse = Product("Mouse", 15001.00, 20)
    customer = Customer("John", CustomerType.REGULAR)
    cart = ShoppingCart(customer, DiscountService())

    # ACT
    cart.add_item(CartItem(mouse, 1))

    # ASSERT: 15001 exceeds 15000, should get 25% off
    assert cart.calculate_total() == 15001.00
    # Expected: 15001 * 0.75 = 11250.75
    assert cart.calculate_final_price() == 11250.75


def test_apply_25_with_bundle():
    # ARRANGE: Test with bundle discount that pushes subtotal above £15000
    laptop = Product("Laptop", 10000.00, 10)
    mouse = Product("Mouse", 6000.00, 20)
    customer = Customer("John", CustomerType.REGULAR)
    cart = ShoppingCart(customer, DiscountService())

    # ACT
    cart.add_item(CartItem(laptop, 1))
    cart.add_item(CartItem(mouse, 1))

    # ASSERT
    # Total before any discount: 10000 + 6000 = 16000
    # Bundle discount: 10% off mouse = 600
    # Subtotal after bundle: 16000 - 600 = 15400
    # Since 15400 > 15000, apply 25% tiered discount
    # Final: 15400 * 0.75 = 11550
    assert cart.calculate_total() == 16000.00
    assert cart.calculate_final_price() == 11550.00
