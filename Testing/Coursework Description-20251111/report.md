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
