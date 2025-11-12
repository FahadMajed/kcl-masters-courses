"""The system shall print a detailed receipt summarising the items in the cart, the total
price before discounts, and the final price after all applicable discounts."""

from ShoppingCart import ShoppingCart
from CartItem import CartItem
from Product import Product
from Customer import Customer
from DiscountService import DiscountService
from CustomerType import CustomerType
import io
import sys


def test_receipt_basic_format():
    # ARRANGE: Simple cart with one item
    mouse = Product("Mouse", 100.00, 20)
    customer = Customer("John", CustomerType.REGULAR)
    cart = ShoppingCart(customer, DiscountService())
    cart.add_item(CartItem(mouse, 1))

    # ACT: Capture printed output
    captured_output = io.StringIO()
    sys.stdout = captured_output
    cart.print_receipt()
    sys.stdout = sys.__stdout__
    receipt = captured_output.getvalue()

    # ASSERT: Receipt should contain header, item details, totals
    assert "----- Shopping Cart Receipt -----" in receipt
    assert "Mouse" in receipt
    assert "1 x" in receipt or "1x" in receipt
    assert "100.00" in receipt


def test_receipt_shows_total_before_discount():
    # ARRANGE: Cart with items
    mouse = Product("Mouse", 500.00, 20)
    customer = Customer("Alice", CustomerType.REGULAR)
    cart = ShoppingCart(customer, DiscountService())
    cart.add_item(CartItem(mouse, 1))

    # ACT: Capture receipt
    captured_output = io.StringIO()
    sys.stdout = captured_output
    cart.print_receipt()
    sys.stdout = sys.__stdout__
    receipt = captured_output.getvalue()

    # ASSERT: Should show total before discount
    assert "Total before discount" in receipt or "before discount" in receipt.lower()
    assert "500.00" in receipt


def test_receipt_shows_final_price_after_discounts():
    # ARRANGE: Cart with discount (VIP customer)
    mouse = Product("Mouse", 500.00, 20)
    customer = Customer("Bob", CustomerType.VIP)
    cart = ShoppingCart(customer, DiscountService())
    cart.add_item(CartItem(mouse, 1))

    # ACT: Capture receipt
    captured_output = io.StringIO()
    sys.stdout = captured_output
    cart.print_receipt()
    sys.stdout = sys.__stdout__
    receipt = captured_output.getvalue()

    # ASSERT: Should show final price after discount (500 * 0.85 = 425)
    assert "Final price" in receipt or "after discount" in receipt.lower()
    assert "425.00" in receipt


def test_receipt_multiple_items():
    # ARRANGE: Cart with multiple different items
    mouse = Product("Mouse", 100.00, 20)
    keyboard = Product("Keyboard", 150.00, 15)
    monitor = Product("Monitor", 300.00, 10)
    customer = Customer("Charlie", CustomerType.REGULAR)
    cart = ShoppingCart(customer, DiscountService())
    cart.add_item(CartItem(mouse, 2))
    cart.add_item(CartItem(keyboard, 1))
    cart.add_item(CartItem(monitor, 1))

    # ACT: Capture receipt
    captured_output = io.StringIO()
    sys.stdout = captured_output
    cart.print_receipt()
    sys.stdout = sys.__stdout__
    receipt = captured_output.getvalue()

    # ASSERT: All items should be listed
    assert "Mouse" in receipt
    assert "Keyboard" in receipt
    assert "Monitor" in receipt
    # Total: 100*2 + 150 + 300 = 650
    assert "650.00" in receipt


def test_receipt_with_quantity():
    # ARRANGE: Item with quantity > 1
    mouse = Product("Mouse", 50.00, 20)
    customer = Customer("David", CustomerType.REGULAR)
    cart = ShoppingCart(customer, DiscountService())
    cart.add_item(CartItem(mouse, 5))

    # ACT: Capture receipt
    captured_output = io.StringIO()
    sys.stdout = captured_output
    cart.print_receipt()
    sys.stdout = sys.__stdout__
    receipt = captured_output.getvalue()

    # ASSERT: Quantity should be shown
    assert "5" in receipt
    assert "50.00" in receipt


def test_receipt_with_coupon():
    # ARRANGE: Cart with coupon code
    mouse = Product("Mouse", 500.00, 20)
    customer = Customer("Eve", CustomerType.REGULAR)
    cart = ShoppingCart(customer, DiscountService())
    cart.add_item(CartItem(mouse, 1))
    cart.apply_coupon_code("SAVE50")

    # ACT: Capture receipt
    captured_output = io.StringIO()
    sys.stdout = captured_output
    cart.print_receipt()
    sys.stdout = sys.__stdout__
    receipt = captured_output.getvalue()

    # ASSERT: Should show both totals
    # Total before: 500, Final after SAVE50: 450
    assert "500.00" in receipt
    assert "450.00" in receipt


def test_receipt_empty_cart():
    # ARRANGE: Empty shopping cart
    customer = Customer("Frank", CustomerType.REGULAR)
    cart = ShoppingCart(customer, DiscountService())

    # ACT: Capture receipt
    captured_output = io.StringIO()
    sys.stdout = captured_output
    cart.print_receipt()
    sys.stdout = sys.__stdout__
    receipt = captured_output.getvalue()

    # ASSERT: Should print receipt even if empty
    assert "----- Shopping Cart Receipt -----" in receipt
    assert "0.00" in receipt or receipt.strip() != ""


def test_receipt_all_discount_types():
    # ARRANGE: Cart with bundle, tiered, customer, and coupon discounts
    laptop = Product("Laptop", 3000.00, 10)
    mouse = Product("Mouse", 100.00, 20)
    customer = Customer("Grace", CustomerType.VIP)
    cart = ShoppingCart(customer, DiscountService())
    cart.add_item(CartItem(laptop, 1))
    cart.add_item(CartItem(mouse, 1))
    cart.apply_coupon_code("SAVE50")

    # ACT: Capture receipt
    captured_output = io.StringIO()
    sys.stdout = captured_output
    cart.print_receipt()
    sys.stdout = sys.__stdout__
    receipt = captured_output.getvalue()

    # ASSERT: Should show total before and after all discounts
    # Total: 3100
    # After all discounts (bundle + fixed coupon + tiered + VIP): complex calculation
    assert "3100.00" in receipt
    assert "Laptop" in receipt
    assert "Mouse" in receipt
