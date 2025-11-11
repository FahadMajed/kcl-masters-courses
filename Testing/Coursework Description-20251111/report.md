# Software Testing Report: Shopping Cart System

**Student Name:** Fahad Alhssan - KNUMBER

**Course:** 6CCS3SMT Software Measurement and Testing

## Introduction

This report documents my approach to testing the Shopping Cart system, a software application designed to handle online shopping with various discount mechanisms. The system includes features like bundle discounts, tiered pricing, customer-specific discounts, and promotional offers.

The main goal of this coursework was to write comprehensive test cases that effectively identify faults in the provided codebase and document the testing process and decisions made along the way.

## 2. Testing Approach

### 2.1 Testing Strategy

(add strategy here)

I chose **pytest** for Python testing because

I organized tests by requirement, creating separate test files for different features:

- `test_shopping_cart.py` - Basic cart functionality (Requirements 1-2)
- `test_bundle_discount.py` - Bundle discount logic (Requirement 3)

This organization makes it easier to maintain tests and understand which requirements are being validated.

---

## 3. Test Cases and Coverage

### 3.1 Requirement 1: Browse and Select Products

"The system shall allow users to browse and select products to add to a shopping cart."

I interpreted "browsing" as the ability to view product details (name, price, stock) and "selecting" as adding products to the cart. although there is no dedicated method to "getAllProducts" or "filterProducts", otherwise this will be considered a not implemented function.

**Test Cases:**

1. `test_browsing_products` - Verifies that product details can be accessed
2. `test_add_product_to_cart` - Verifies that products can be added to a cart

These tests validate that the basic Product and ShoppingCart classes work correctly.

### 3.2 Requirement 2: Calculate Total Before Discounts

"The system shall calculate the total price of items in the shopping cart before applying any discounts."

**Test Case:**

- `test_calculate_total_before_discounts` - Adds multiple products with different quantities and verifies the sum is calculated correctly

This test uses:

- 2 laptops at £1000 each = £2000
- 3 mice at £50 each = £150
- 1 keyboard at £150 = £150
- **Expected total: £2300**

The test passed, confirming this requirement is implemented correctly.

### 3.3 Requirement 3: Bundle Discount (Mouse-Laptop Pairs)

"The system shall apply a bundle discount: 10% off the price of each mouse if at least one laptop is in the cart. This discount applies for all mouse-laptop pairs."

This requirement was more complex to understand. After clarification from the Q&A forum, I learned that:

- Each laptop can discount only one mouse
- Examples:
  - laptop + 2 mice, only 1 mouse gets 10% off
  - 2 laptops + 2 mice, both mice get 10% off

**Test 1: `test_no_bundle_discount_without_laptop`** PASSED
Cart contains 2 mice (£200 total) with no laptop. Expected £200, got £200. This test passed because when there's no laptop in the cart, the condition `has_laptop` evaluates to false, so no discount is applied.

**Test 2: `test_no_bundle_discount_without_mouse`** FAILED
Cart contains 1 laptop (£200) with no mouse. Expected £200, got £180. The system incorrectly applied a £20 discount (10% of £200 laptop). This exposed the core bug: in `DiscountService.py` line 18, the code checks `if item != "mouse"` instead of `if item == "mouse"`. This inverted condition means the discount is applied to everything EXCEPT mice, which is backwards.

**Test 3: `test_one_laptop_one_mouse`** FAILED
Cart contains 1 laptop (£200) + 1 mouse (£100) = £300. Expected £290 (after 10% off the mouse = £10 discount), got £280. The system applied 10% to the laptop (£20) instead of 10% to the mouse (£10), resulting in £20 too much discount. Same bug as Test 2.

**Test 4: `test_one_laptop_multiple_mice`** FAILED
Cart contains 1 laptop (£200) + 3 mice (£300) = £500. Expected £490 (10% off one mouse = £10), got £480. The laptop received the £20 discount instead of just one mouse getting £10 discount. Same inverted condition bug.

**Test 5: `test_two_laptops_two_mice`** FAILED
Cart contains 2 laptops (£150 each = £300) + 2 mice (£100 each = £200) = £500. Expected £480 (10% off two mice = £20 total), got £485. The actual discount applied was only £15 (10% of ONE laptop at £150), revealing a second bug: the code applies the discount once per CartItem without considering quantity. Since we have one CartItem with quantity=2 laptops, it only discounts one laptop's price rather than both.

**Test 6: `test_two_laptops_three_mice`** FAILED
Cart contains 2 laptops (£300) + 3 mice (£300) = £600. Expected £580 (10% off two mice = £20 total), got £585. Again, only £15 was discounted (10% of ONE laptop). This confirms the quantity bug: the loop processes CartItems, not individual product units, so it only applies `item.get_product().get_price() * 0.10` without multiplying by quantity.

**Test 7: `test_three_laptops_two_mice`** FAILED
Cart contains 3 laptops (£450) + 2 mice (£200) = £650. Expected £630 (10% off two mice = £20 total), got £635. Consistent with Tests 5 and 6, only £15 was discounted. Even with 3 laptops in the cart, the buggy code only discounts one laptop's price because it processes the single laptop CartItem once, ignoring that quantity=3.

**Test 8: `test_bundle_discount_with_zero_price_mouse`** FAILED
Cart contains 1 laptop (£200) + 1 free mouse (£0) = £200. Expected £200 (10% of £0 is £0), got £180. This edge case confirms the bug: even with a free mouse, the laptop still receives 10% discount. This definitively proves the inverted condition bug in line 18.

The implementation has clear defects in `DiscountService.py` lines 17-23:

the Inverted condition (line 18), `if item != "mouse"` should be `== "mouse"`. This causes the discount to apply to laptops instead of mice, completely inverting the intended behavior.

And the Missing quantity handling (line 23), The code uses `item.get_product().get_price() * 0.10` but doesn't multiply by `item.get_quantity()`. This means when a CartItem has quantity > 1, only oen unit's price gets discounted instead of all units that should be discounted based on the pairing logic.

These bugs compound each other, the wrong product type gets discounted, and only one unit is discounted regardless of how many pairs exist.

---

## 4. Testing Challenges and Trade-offs

### 4.1 Challenges Faced

**1. Understanding the Pairing Logic**

Initially, I misunderstood the requirement "applies for all mouse-laptop pairs." I thought ALL mice would get discounts if at least one laptop was present. After clarification, I learned it's a min(laptops, mice) pairing system. This required me to redesign several test cases.

**2. Test Isolation vs. Real-World Scenarios**

I had to balance between:

- Testing components in isolation (unit tests)
- Testing realistic shopping scenarios (integration tests)

I chose to focus on unit tests with realistic data, which helped identify bugs more precisely.

**3. Handling Interdependent Discounts**

The system has multiple discount types (bundle, tier, customer type, promotions) that interact with each other. I had to carefully calculate expected values by understanding the order in which discounts are applied.

I even thought there was a bug in some requirements from discount calculation, but this was due to another discount being triggered.

### 4.2 Trade-offs

**Coverage vs. Time:**
I prioritized testing critical requirements (discounts, price calculations) over less critical ones (receipt printing). This was necessary given time constraints but means some edge cases may remain untested.

**Test Readability vs. DRY Principle:**
I repeated setup code in each test rather than using complex fixtures. This makes tests more verbose but easier to understand and maintain.

---

## 6. Code Coverage

_(Coverage report will be added here once generated)_

---

## 7. Mocking Strategy

_(To be completed as we progress)_

---

## 8. Conclusion

Through systematic requirements-based testing, I successfully identified a critical bug in the bundle discount implementation that affects the majority of test scenarios. The bug involves applying discounts to the wrong product type, demonstrating how well-designed test cases can effectively expose fundamental flaws in software logic.

The testing process highlighted the importance of:

1. Clearly understanding requirements before writing tests
2. Testing both positive and negative scenarios
3. Using descriptive test names and clear assertions
4. Covering edge cases and boundary conditions

---

**Word Count:** ~1,200 words
_(Target: 2000 words max)_
