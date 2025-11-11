"""
Bundle Discount Requirement:
- 10% off per mouse-laptop pair
- Each laptop can discount ONE mouse
- min(laptops, mice) mice will get the discount

Examples:
- 1 laptop + 1 mouse, 1 mouse gets 10% off
- 1 laptop + 2 mice, only 1 mouse gets 10% off
- 2 laptops + 2 mice, both mice get 10% off
- 2 laptops + 3 mice, only 2 mice get 10% off
"""

from Product import Product
from ShoppingCart import ShoppingCart
from CartItem import CartItem
from Customer import Customer
from DiscountService import DiscountService
from CustomerType import CustomerType


def test_no_bundle_discount_without_laptop():
    # ARRANGE
    mouse = Product("Mouse", 100.00, 20)
    customer = Customer("John", CustomerType.REGULAR)
    cart = ShoppingCart(customer, DiscountService())

    # ACT
    cart.add_item(CartItem(mouse, 2))

    # ASSERT: No laptop, no discount
    assert cart.calculate_total() == 200.00
    assert cart.calculate_final_price() == 200.00


def test_no_bundle_discount_without_mouse():
    # ARRANGE
    laptop = Product("Laptop", 200.00, 10)
    customer = Customer("Jane", CustomerType.REGULAR)
    cart = ShoppingCart(customer, DiscountService())

    # ACT
    cart.add_item(CartItem(laptop, 1))

    # ASSERT: No mouse, no discount to apply
    assert cart.calculate_total() == 200.00
    assert cart.calculate_final_price() == 200.00


def test_one_laptop_one_mouse():
    # ARRANGE
    laptop = Product("Laptop", 200.00, 10)
    mouse = Product("Mouse", 100.00, 20)
    customer = Customer("Alice", CustomerType.REGULAR)
    cart = ShoppingCart(customer, DiscountService())

    # ACT
    cart.add_item(CartItem(laptop, 1))
    cart.add_item(CartItem(mouse, 1))

    # ASSERT: 1 pair → 1 mouse gets 10% off
    assert cart.calculate_total() == 300.00
    # Expected: 300 - 10 (10% of one mouse) = 290
    assert cart.calculate_final_price() == 290.00


def test_one_laptop_multiple_mice():
    # ARRANGE: 1 laptop + 3 mice
    laptop = Product("Laptop", 200.00, 10)
    mouse = Product("Mouse", 100.00, 20)
    customer = Customer("Bob", CustomerType.REGULAR)
    cart = ShoppingCart(customer, DiscountService())

    # ACT
    cart.add_item(CartItem(laptop, 1))
    cart.add_item(CartItem(mouse, 3))

    # ASSERT: Only 1 mouse gets discount (limited by laptop count)
    assert cart.calculate_total() == 500.00
    # Expected: 500 - 10 (10% of ONE mouse) = 490
    assert cart.calculate_final_price() == 490.00


def test_two_laptops_two_mice():
    # ARRANGE: 2 laptops + 2 mice
    laptop = Product("Laptop", 150.00, 10)
    mouse = Product("Mouse", 100.00, 20)
    customer = Customer("David", CustomerType.REGULAR)
    cart = ShoppingCart(customer, DiscountService())

    # ACT
    cart.add_item(CartItem(laptop, 2))
    cart.add_item(CartItem(mouse, 2))

    # ASSERT: Both mice get discount (2 pairs)
    # Total: 300 + 200 = 500
    assert cart.calculate_total() == 500.00
    # Expected: 500 - 20 (10% of TWO mice at £100 each) = 480
    # Bug would give: 500 - 30 (10% of TWO laptops at £150 each) = 470
    assert cart.calculate_final_price() == 480.00


def test_two_laptops_three_mice():
    # ARRANGE: 2 laptops + 3 mice
    laptop = Product("Laptop", 150.00, 10)
    mouse = Product("Mouse", 100.00, 20)
    customer = Customer("Eve", CustomerType.REGULAR)
    cart = ShoppingCart(customer, DiscountService())

    # ACT
    cart.add_item(CartItem(laptop, 2))
    cart.add_item(CartItem(mouse, 3))

    # ASSERT: Only 2 mice get discount (limited by 2 laptops)
    # Total: 300 + 300 = 600
    assert cart.calculate_total() == 600.00
    # Expected: 600 - 20 (10% of TWO mice) = 580
    # Bug would give: 600 - 30 (10% of TWO laptops) = 570
    assert cart.calculate_final_price() == 580.00


def test_three_laptops_two_mice():
    # ARRANGE: 3 laptops + 2 mice
    laptop = Product("Laptop", 150.00, 10)
    mouse = Product("Mouse", 100.00, 20)
    customer = Customer("Frank", CustomerType.REGULAR)
    cart = ShoppingCart(customer, DiscountService())

    # ACT
    cart.add_item(CartItem(laptop, 3))
    cart.add_item(CartItem(mouse, 2))

    # ASSERT: Both mice get discount (limited by 2 mice)
    # Total: 450 + 200 = 650
    assert cart.calculate_total() == 650.00
    # Expected: 650 - 20 (10% of TWO mice) = 630
    # Bug would give: 650 - 45 (10% of THREE laptops) = 605
    assert cart.calculate_final_price() == 630.00


def test_bundle_discount_with_zero_price_mouse():
    # ARRANGE: Edge case - free mouse
    laptop = Product("Laptop", 200.00, 10)
    free_mouse = Product("Mouse", 0.00, 20)
    customer = Customer("Grace", CustomerType.REGULAR)
    cart = ShoppingCart(customer, DiscountService())

    # ACT
    cart.add_item(CartItem(laptop, 1))
    cart.add_item(CartItem(free_mouse, 1))

    # ASSERT: 10% of £0 is still £0
    assert cart.calculate_total() == 200.00
    assert cart.calculate_final_price() == 200.00
