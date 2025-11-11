"""The system shall categorize customers into three types: Regular, Premium, and VIP,
with Premium customers receiving an additional 10% discount and VIP customers
receiving an additional 15% discount on their total."""

from ShoppingCart import ShoppingCart
from CartItem import CartItem
from Product import Product
from Customer import Customer
from DiscountService import DiscountService
from CustomerType import CustomerType


def test_regular_customer_no_additional_discount():
    # ARRANGE: Regular customer with simple cart below all tiered thresholds
    mouse = Product("Mouse", 500.00, 20)
    customer = Customer("John", CustomerType.REGULAR)
    cart = ShoppingCart(customer, DiscountService())

    # ACT
    cart.add_item(CartItem(mouse, 1))

    # ASSERT: Regular customer gets no additional discount
    assert cart.calculate_total() == 500.00
    assert cart.calculate_final_price() == 500.00


def test_premium_customer_gets_10_percent_discount():
    # ARRANGE: Premium customer with simple cart below tiered thresholds
    mouse = Product("Mouse", 500.00, 20)
    customer = Customer("Jane", CustomerType.PREMIUM)
    cart = ShoppingCart(customer, DiscountService())

    # ACT
    cart.add_item(CartItem(mouse, 1))

    # ASSERT: Premium customer should get additional 10% discount
    # Expected: 500 * 0.90 = 450.00
    assert cart.calculate_total() == 500.00
    assert cart.calculate_final_price() == 450.00


def test_vip_customer_gets_15_percent_discount():
    # ARRANGE: VIP customer with simple cart below tiered thresholds
    mouse = Product("Mouse", 500.00, 20)
    customer = Customer("Alice", CustomerType.VIP)
    cart = ShoppingCart(customer, DiscountService())

    # ACT
    cart.add_item(CartItem(mouse, 1))

    # ASSERT: VIP customer should get additional 15% discount
    # Expected: 500 * 0.85 = 425.00
    assert cart.calculate_total() == 500.00
    assert cart.calculate_final_price() == 425.00


def test_regular_customer_with_multiple_items():
    # ARRANGE: Regular customer with multiple items, total below thresholds
    mouse = Product("Mouse", 100.00, 20)
    keyboard = Product("Keyboard", 150.00, 15)
    customer = Customer("Bob", CustomerType.REGULAR)
    cart = ShoppingCart(customer, DiscountService())

    # ACT
    cart.add_item(CartItem(mouse, 2))
    cart.add_item(CartItem(keyboard, 1))

    # ASSERT: Regular customer gets no discount
    # Total: 100*2 + 150 = 350
    assert cart.calculate_total() == 350.00
    assert cart.calculate_final_price() == 350.00


def test_premium_customer_with_multiple_items():
    # ARRANGE: Premium customer with multiple items, total below thresholds
    mouse = Product("Mouse", 100.00, 20)
    keyboard = Product("Keyboard", 150.00, 15)
    customer = Customer("Charlie", CustomerType.PREMIUM)
    cart = ShoppingCart(customer, DiscountService())

    # ACT
    cart.add_item(CartItem(mouse, 2))
    cart.add_item(CartItem(keyboard, 1))

    # ASSERT: Premium customer gets 10% discount
    # Total: 100*2 + 150 = 350
    # Expected: 350 * 0.90 = 315.00
    assert cart.calculate_total() == 350.00
    assert cart.calculate_final_price() == 315.00


def test_vip_customer_with_multiple_items():
    # ARRANGE: VIP customer with multiple items, total below thresholds
    mouse = Product("Mouse", 100.00, 20)
    keyboard = Product("Keyboard", 150.00, 15)
    customer = Customer("David", CustomerType.VIP)
    cart = ShoppingCart(customer, DiscountService())

    # ACT
    cart.add_item(CartItem(mouse, 2))
    cart.add_item(CartItem(keyboard, 1))

    # ASSERT: VIP customer gets 15% discount
    # Total: 100*2 + 150 = 350
    # Expected: 350 * 0.85 = 297.50
    assert cart.calculate_total() == 350.00
    assert cart.calculate_final_price() == 297.50
