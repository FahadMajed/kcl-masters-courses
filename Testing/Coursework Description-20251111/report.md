# Software Testing Report: Shopping Cart System

**Student Name:** Fahad Alhssan - KNUMBER

**Course:** 6CCS3SMT Software Measurement and Testing

## Introduction

This report documents my approach to testing the Shopping Cart system, a software application designed to handle online shopping with various discount mechanisms. The system includes features like bundle discounts, tiered pricing, customer-specific discounts, and promotional offers.

The main goal of this coursework was to write comprehensive test cases that effectively identify faults in the provided codebase and document the testing process and decisions made along the way.

## 2. Testing Approach

I used a requirements-based testing approach, creating test cases directly from the system requirements to ensure all specified functionality is validated.

For the more complex requirements, I applied **equivalence partitioning** to systematically identify different input scenarios. For example, in Requirement 3 (bundle discount), I identified different classes based on the number of laptops and mice in the cart: cases with no laptops, no mice, equal quantities, more mice than laptops, and more laptops than mice. This technique helped me create a comprehensive set of test cases that cover all logical scenarios without redundant tests.

I organized tests by requirement, creating separate test files for different features:

- `test_browsing_and_adding.py` - Basic cart functionality (Requirements 1-2)
- `test_bundle_discount.py` - Bundle discount logic (Requirement 3)

This organization makes it easier to maintain tests and understand which requirements are being validated.

for the framework, I chose **pytest** for Python testing because it provides clear output, simple assertions, and good test organization capabilities.

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

This requirement was more complex to understand. After clarification from the Q&A forum, I learned that each laptop can discount only one mouse, following a min(laptops, mice) pairing system.

**Test Cases Designed:**

I created 8 test cases to systematically verify the bundle discount logic and cover each possible logical combinations of input:

1. `test_no_bundle_discount_without_laptop` - No laptop in cart, no discount should apply (PASSED)
2. `test_no_bundle_discount_without_mouse` - No mouse in cart, no discount should apply (FAILED)
3. `test_one_laptop_one_mouse` - 1:1 pairing, 1 mouse should get 10% off (FAILED)
4. `test_one_laptop_multiple_mice` - 1 laptop + 3 mice, only 1 mouse should get discount (FAILED)
5. `test_two_laptops_two_mice` - Perfect 2:2 pairing, both mice should get discount (FAILED)
6. `test_two_laptops_three_mice` - 2 laptops + 3 mice, only 2 mice should get discount (FAILED)
7. `test_three_laptops_two_mice` - More laptops than mice, both mice should get discount (FAILED)
8. `test_bundle_discount_with_zero_price_mouse` - Edge case with free mouse (FAILED)

The tests used carefully chosen prices (£200 laptops, £150 laptops for tests 5-7, and £100 mice) to avoid accidentally triggering other discounts and to clearly distinguish between correct behavior and buggy behavior.

**Detected Faults:**

| Class Name      | Line Number(s) | Description of Fault                                                                                                                                                                                                                                                                                                                                                | Test Case(s) That Expose the Fault                                                                                                                                                                                                             |
| --------------- | -------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| DiscountService | Line 18        | **Inverted condition**, The code checks `if item != "mouse"` instead of `if item == "mouse"`. This causes the 10% bundle discount to be applied to laptops (and any other non-mouse products) instead of to mice, completely inverting the intended behavior.                                                                                                       | `test_no_bundle_discount_without_mouse`, `test_one_laptop_one_mouse`, `test_one_laptop_multiple_mice`, `test_two_laptops_two_mice`, `test_two_laptops_three_mice`, `test_three_laptops_two_mice`, `test_bundle_discount_with_zero_price_mouse` |
| DiscountService | Line 23        | **Missing quantity handling**, The code uses `item.get_product().get_price() * 0.10` without multiplying by `item.get_quantity()`. When a CartItem has quantity > 1, only one unit's price gets discounted instead of all units that should be discounted based on the pairing logic. This means the loop processes CartItems rather than individual product units. | `test_two_laptops_two_mice`, `test_two_laptops_three_mice`, `test_three_laptops_two_mice`                                                                                                                                                      |

These two bugs compound each other, not only is the wrong product type being discounted, but only one unit is discounted regardless of how many pairs should exist according to the requirement.

### 3.4 Requirement 4: Tiered Discounts

"The system shall apply tiered discounts based on the cart subtotal after bundle discounts:
• 15% off if the subtotal exceeds £2,000
• 20% off if the subtotal exceeds £7,000
• 25% off if the subtotal exceeds £15,000"

This requirement introduces tiered discounts that should be applied after bundle discounts. The system should select the highest applicable tier based on the subtotal, and the discount should only apply when the subtotal strictly exceeds (is greater than) the threshold.

**Test Cases Designed:**

I created 8 test cases to systematically verify the tiered discount logic with boundary testing and scenarios combining bundle discounts:

1. `test_no_tiered_discount_below_threshold` - £500 subtotal, well below any threshold (PASSED)
2. `test_no_discount_at_1999` - £1999 subtotal, just below £2000 threshold, should get no discount (FAILED)
3. `test_apply_15_without_bundle` - £2001 subtotal exceeds £2000, should get 15% off (PASSED)
4. `test_apply_15_with_bundle` - Bundle discount brings subtotal above £2000 (FAILED)
5. `test_apply_20_without_bundle` - £7001 subtotal exceeds £7000, should get 20% off (PASSED)
6. `test_apply_20_with_bundle` - Bundle discount brings subtotal above £7000 (FAILED)
7. `test_apply_25_without_bundle` - £15001 subtotal exceeds £15000, should get 25% off (PASSED)
8. `test_apply_25_with_bundle` - Bundle discount brings subtotal above £15000 (FAILED)

**Detected Faults:**

| Class Name      | Line Number(s) | Description of Fault                                                                                                                                                                                                                 | Test Case(s) That Expose the Fault |
| --------------- | -------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ---------------------------------- |
| DiscountService | Line 30        | **Incorrect threshold value**, Uses `total > 1000` instead of `total > 2000` for the 15% discount tier. This causes the 15% discount to be incorrectly applied to any subtotal above £1000, affecting the £1001-£2000 price range.   | `test_no_discount_at_1999`         |
| DiscountService | Lines 17-23    | **Bundle discount bug** (from Requirement 3), Applies discount to laptops instead of mice, causing incorrect subtotals to be passed to tiered discount logic. This cascades into all tests that combine bundle and tiered discounts. | All`*_with_bundle` test cases      |

### 3.5 Requirement 5: Customer Categories

"The system shall categorize customers into three types: Regular, Premium, and VIP, with Premium customers receiving an additional 10% discount and VIP customers receiving an additional 15% discount on their total."

**Test Cases Designed:**

I created 6 test cases focused on testing customer category discounts in isolation (avoiding other discount types):

1. `test_regular_customer_no_additional_discount` - Single item, no discount (PASSED)
2. `test_premium_customer_gets_10_percent_discount` - Single item, 10% discount (FAILED)
3. `test_vip_customer_gets_15_percent_discount` - Single item, 15% discount (PASSED)
4. `test_regular_customer_with_multiple_items` - Multiple items, no discount (PASSED)
5. `test_premium_customer_with_multiple_items` - Multiple items, 10% discount (FAILED)
6. `test_vip_customer_with_multiple_items` - Multiple items, 15% discount (PASSED)

**Detected Faults:**

| Class Name      | Line Number(s) | Description of Fault                                                                                                                                                                                                                | Test Case(s) That Expose the Fault                                                            |
| --------------- | -------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------- |
| DiscountService | Line 35        | **Incorrect discount percentage**, Uses `discount += 0.20` (20%) instead of `discount += 0.10` (10%) for Premium customers. This gives Premium customers double the intended discount, contradicting the requirement specification. | `test_premium_customer_gets_10_percent_discount`, `test_premium_customer_with_multiple_items` |

For `test_premium_customer_gets_10_percent_discount`:
- Expected: £500 × 0.90 = £450.00
- Actual: £500 × 0.80 = £400.00 (20% discount instead of 10%)

Regular and VIP customers work correctly, but Premium customers receive 20% discount instead of the required 10%.

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
