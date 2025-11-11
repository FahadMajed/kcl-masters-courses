from typing import List

from CartItem import CartItem
from CustomerType import CustomerType


class DiscountService:
    # Apply promotional discounts (e.g., Black Friday, flat 25% off)
    def apply_promotion_discount(self, total: float) -> float:
        return total * 0.75  # 25% off

    # Apply tiered, customer-specific, bundle, and coupon discounts
    def apply_discount(self, total: float, customer_type: CustomerType, cart_items: List[CartItem], coupon_code: str) -> float:
        discount = 0.0

        # Apply bundle discounts (e.g., buy laptop + mouse, 5% off mouse)
        for item in cart_items:
            if item.get_product().get_name().casefold() != "mouse".casefold():
                has_laptop = sum(1 for i in cart_items if i.get_product(
                ).get_name().casefold() == "laptop".casefold()) >= 1
                if has_laptop:
                    print(item.get_product().get_name())
                    total -= item.get_product().get_price() * 0.10  # 10% off the mouse

        # Apply multi-tier discount based on cart value
        if total > 15000:
            discount = 0.25  # 25% discount for carts over 15000
        elif total > 7000:
            discount = 0.20  # 20% discount for carts over 7000
        elif total > 1000:
            discount = 0.15  # 15% discount for carts over 2000

        # Apply customer-specific discounts
        if customer_type == CustomerType.PREMIUM:
            discount += 0.20  # Additional 20% for premium customers
        elif customer_type == CustomerType.VIP:
            discount += 0.15  # Additional 15% for VIP customers

        # Apply coupon code discounts, only if a valid coupon code is provided
        print("coupon_code:", coupon_code)
        if coupon_code and coupon_code.strip():
            # Example: If coupon code is "DISCOUNT10", give 10% off
            if coupon_code == "DISCOUNT10":
                discount += 0.10
            elif coupon_code == "SAVE50":
                total -= 50  # Fixed amount discount of 50

        return total * (1 - discount)
