"""Requirement 7: Time-Limited Promotions
The system shall support time-limited promotions that can be activated or deactivated.
During an active promotion, a flat discount of 25% shall be applied.

Requirement 8: Discount Order
Bundle discounts and fixed-amount coupons are applied first, then all percentage-based
discounts (tiered, customer type, percentage coupons, promotions) are applied.
"""

from ShoppingCart import ShoppingCart
from CartItem import CartItem
from Product import Product
from Customer import Customer
from DiscountService import DiscountService
from CustomerType import CustomerType


def test_no_promotion_active():
    # ARRANGE: Cart without active promotion
    mouse = Product("Mouse", 500.00, 20)
    customer = Customer("John", CustomerType.REGULAR)
    cart = ShoppingCart(customer, DiscountService())

    # ACT
    cart.add_item(CartItem(mouse, 1))
    cart.set_promotion_active(False)

    # ASSERT: No promotion discount
    assert cart.calculate_total() == 500.00
    assert cart.calculate_final_price() == 500.00


def test_promotion_active():
    # ARRANGE: Cart with active promotion (25% off)
    mouse = Product("Mouse", 500.00, 20)
    customer = Customer("Jane", CustomerType.REGULAR)
    cart = ShoppingCart(customer, DiscountService())

    # ACT
    cart.add_item(CartItem(mouse, 1))
    cart.set_promotion_active(True)

    # ASSERT: 25% promotion discount
    # Expected: 500 * 0.75 = 375.00
    assert cart.calculate_total() == 500.00
    assert cart.calculate_final_price() == 375.00


def test_promotion_with_multiple_items():
    # ARRANGE: Multiple items with active promotion
    mouse = Product("Mouse", 100.00, 20)
    keyboard = Product("Keyboard", 150.00, 15)
    customer = Customer("Alice", CustomerType.REGULAR)
    cart = ShoppingCart(customer, DiscountService())

    # ACT
    cart.add_item(CartItem(mouse, 2))
    cart.add_item(CartItem(keyboard, 1))
    cart.set_promotion_active(True)

    # ASSERT: 25% off total
    # Total: 100*2 + 150 = 350
    # Expected: 350 * 0.75 = 262.50
    assert cart.calculate_total() == 350.00
    assert cart.calculate_final_price() == 262.50


def test_promotion_combines_with_tiered_discount():
    # ARRANGE: Test that promotion discount combines with tiered discount
    mouse = Product("Mouse", 2001.00, 20)
    customer = Customer("Bob", CustomerType.REGULAR)
    cart = ShoppingCart(customer, DiscountService())

    # ACT
    cart.add_item(CartItem(mouse, 1))
    cart.set_promotion_active(True)

    # ASSERT: Promotion (25%) should combine with tiered discount (15%)
    # Total percentage: 15% + 25% = 40%
    # Expected: 2001 * (1 - 0.40) = 1200.60
    assert cart.calculate_total() == 2001.00
    assert cart.calculate_final_price() == 1200.60


def test_promotion_toggle_off():
    # ARRANGE: Promotion can be toggled off
    mouse = Product("Mouse", 500.00, 20)
    customer = Customer("Charlie", CustomerType.REGULAR)
    cart = ShoppingCart(customer, DiscountService())

    # ACT
    cart.add_item(CartItem(mouse, 1))
    cart.set_promotion_active(True)
    # Then turn it off
    cart.set_promotion_active(False)

    # ASSERT: No discount when promotion is deactivated
    assert cart.calculate_total() == 500.00
    assert cart.calculate_final_price() == 500.00


def test_discount_order_bundle_then_percentage():
    # ARRANGE: Test Requirement 8 - Bundle discount applied first, then percentage
    laptop = Product("Laptop", 1000.00, 10)
    mouse = Product("Mouse", 500.00, 20)
    customer = Customer("David", CustomerType.REGULAR)
    cart = ShoppingCart(customer, DiscountService())

    # ACT
    cart.add_item(CartItem(laptop, 1))
    cart.add_item(CartItem(mouse, 1))
    cart.set_promotion_active(True)

    # ASSERT: Bundle discount (10% off mouse) applied first
    # Total: 1000 + 500 = 1500
    # Bundle: 10% off mouse = 1500 - 50 = 1450
    # Then promotion: 25% off = 1450 * 0.75 = 1087.50
    assert cart.calculate_total() == 1500.00
    assert cart.calculate_final_price() == 1087.50


def test_discount_order_fixed_coupon_then_percentage():
    # ARRANGE: Test fixed-amount coupon applied first, then percentage
    mouse = Product("Mouse", 500.00, 20)
    customer = Customer("Eve", CustomerType.REGULAR)
    cart = ShoppingCart(customer, DiscountService())

    # ACT
    cart.add_item(CartItem(mouse, 1))
    cart.apply_coupon_code("SAVE50")
    cart.set_promotion_active(True)

    # ASSERT: Fixed coupon (£50) applied first, then promotion (25%)
    # Total: 500
    # Fixed coupon: 500 - 50 = 450
    # Then promotion: 450 * 0.75 = 337.50
    assert cart.calculate_total() == 500.00
    assert cart.calculate_final_price() == 337.50


def test_discount_order_percentage_coupon_with_promotion():
    # ARRANGE: Test percentage coupon with promotion (both are percentage-based)
    mouse = Product("Mouse", 500.00, 20)
    customer = Customer("Frank", CustomerType.REGULAR)
    cart = ShoppingCart(customer, DiscountService())

    # ACT
    cart.add_item(CartItem(mouse, 1))
    cart.apply_coupon_code("DISCOUNT10")
    cart.set_promotion_active(True)

    # ASSERT: Both percentage discounts combine (10% + 25% = 35%)
    # Expected: 500 * (1 - 0.35) = 325.00
    assert cart.calculate_total() == 500.00
    assert cart.calculate_final_price() == 325.00


def test_discount_order_all_types_combined():
    # ARRANGE: VIP customer with laptop + mouse + SAVE50 coupon + promotion
    # This is the example scenario from the requirement specification
    laptop = Product("Laptop", 3000.00, 10)
    mouse = Product("Mouse", 100.00, 20)
    customer = Customer("Grace", CustomerType.VIP)
    cart = ShoppingCart(customer, DiscountService())

    # ACT
    cart.add_item(CartItem(laptop, 1))
    cart.add_item(CartItem(mouse, 1))
    cart.apply_coupon_code("SAVE50")
    cart.set_promotion_active(True)

    # ASSERT: Follow the discount order from Requirement 8
    # Step 1 - Total: 3000 + 100 = 3100
    # Step 2 - Bundle discount (10% off mouse): 3100 - 10 = 3090
    # Step 3 - Fixed coupon (SAVE50): 3090 - 50 = 3040
    # Step 4 - Percentage discounts combine:
    #   - Tiered (subtotal 3090 > 2000): 15%
    #   - VIP customer: 15%
    #   - Promotion: 25%
    #   - Total percentage: 15% + 15% + 25% = 55%
    # Final: 3040 * (1 - 0.55) = 1368.00
    assert cart.calculate_total() == 3100.00
    assert cart.calculate_final_price() == 1368.00
