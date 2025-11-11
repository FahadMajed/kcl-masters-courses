"""
1. The system shall allow users to browse and select products to add to a shopping cart. 
2. The  system  shall  calculate  the  total  price  of  items  in  the  shopping  cart  before 
applying any discounts
"""

from Product import Product
from ShoppingCart import ShoppingCart
from CartItem import CartItem
from Customer import Customer
from DiscountService import DiscountService
from CustomerType import CustomerType


def test_browsing_products():
    # ARRANGE A PRODUCT
    productA = Product("Laptop", 999.99, 10)

    assert productA.get_name() == "Laptop"
    assert productA.get_price() == 999.99
    assert productA.get_stock() == 10


def test_add_product_to_cart():

    # ARRANGE A PRODUCT
    laptop = Product("Laptop", 999.99, 10)
    customer = Customer(name='Fahad', customer_type=CustomerType.REGULAR)
    cart = ShoppingCart(customer=customer, discount_service=DiscountService())
    cartItem = CartItem(product=laptop, quantity=1,)
    # ACT: A PRODUCT IS ADDED
    cart.add_item(cartItem)

    # ASSERT: cart now contains the product
    assert cart.get_items()[0].get_product().get_name() == "Laptop"


def test_calculate_total_before_discounts():

    # ARRANGE: Multiple products in cart
    laptop = Product("Laptop", 1000.00, 10)
    mouse = Product("Mouse", 50.00, 20)
    keyboard = Product("Keyboard", 150.00, 15)

    customer = Customer("John", CustomerType.REGULAR)
    cart = ShoppingCart(customer, DiscountService())

    # ACT: Add multiple items with different quantities
    cart.add_item(CartItem(laptop, 2))      # 2 * 1000 = 2000
    cart.add_item(CartItem(mouse, 3))       # 3 * 50 = 150
    cart.add_item(CartItem(keyboard, 1))    # 1 * 150 = 150

    # ASSERT: Total should be sum of all items (before any discounts)
    expected_total = (2 * 1000.00) + (3 * 50.00) + \
        (1 * 150.00)  # 2000 + 150 + 150 = 2300
    assert cart.calculate_total() == expected_total
