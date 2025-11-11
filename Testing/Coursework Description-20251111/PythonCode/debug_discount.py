import sys
sys.path.insert(0, 'src')

from Product import Product
from ShoppingCart import ShoppingCart
from CartItem import CartItem
from Customer import Customer
from DiscountService import DiscountService
from CustomerType import CustomerType

# Test 5: 2 laptops + 2 mice
laptop = Product("Laptop", 150.00, 10)
mouse = Product("Mouse", 100.00, 20)
customer = Customer("David", CustomerType.REGULAR)
cart = ShoppingCart(customer, DiscountService())

cart.add_item(CartItem(laptop, 2))
cart.add_item(CartItem(mouse, 2))

print("=== Test 5: 2 laptops + 2 mice ===")
print(f"Total before discount: £{cart.calculate_total()}")
print(f"Final price: £{cart.calculate_final_price()}")
print(f"Discount applied: £{cart.calculate_total() - cart.calculate_final_price()}")
print()

# What the bug does:
# - Loops through cart_items (2 items: one laptop CartItem, one mouse CartItem)
# - For laptop CartItem: checks if "Laptop" != "mouse" -> TRUE
# - Applies: 150.00 * 0.10 = £15 discount (only ONE laptop price, ignoring quantity!)
# - For mouse CartItem: checks if "Mouse" != "mouse" -> FALSE, skips
# Result: £500 - £15 = £485

print("Expected (correct behavior): £480 (10% off TWO mice = £20 discount)")
print("Bug gives: £485 (10% off ONE laptop = £15 discount)")
print()

# Test 6: 2 laptops + 3 mice
cart2 = ShoppingCart(customer, DiscountService())
cart2.add_item(CartItem(laptop, 2))
cart2.add_item(CartItem(mouse, 3))

print("=== Test 6: 2 laptops + 3 mice ===")
print(f"Total before discount: £{cart2.calculate_total()}")
print(f"Final price: £{cart2.calculate_final_price()}")
print(f"Discount applied: £{cart2.calculate_total() - cart2.calculate_final_price()}")
print()
print("Expected (correct): £580 (10% off TWO mice = £20 discount)")
print("Bug gives: £585 (10% off ONE laptop = £15 discount)")
print()

# Test 7: 3 laptops + 2 mice
cart3 = ShoppingCart(customer, DiscountService())
cart3.add_item(CartItem(laptop, 3))
cart3.add_item(CartItem(mouse, 2))

print("=== Test 7: 3 laptops + 2 mice ===")
print(f"Total before discount: £{cart3.calculate_total()}")
print(f"Final price: £{cart3.calculate_final_price()}")
print(f"Discount applied: £{cart3.calculate_total() - cart3.calculate_final_price()}")
print()
print("Expected (correct): £630 (10% off TWO mice = £20 discount)")
print("Bug gives: £635 (10% off ONE laptop = £15 discount)")
