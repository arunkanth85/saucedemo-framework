from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage


def test_end_to_end_checkout(driver):
    # 1. Log in
    login_page = LoginPage(driver)
    login_page.open()
    login_page.login("standard_user", "secret_sauce")

    # 2. Add an item to the cart
    inventory_page = InventoryPage(driver)
    inventory_page.add_backpack_to_cart()
    assert inventory_page.get_cart_count() == "1"
    inventory_page.go_to_cart()

    # 3. Proceed to checkout
    cart_page = CartPage(driver)
    cart_page.checkout()

    # 4. Fill customer details and finish the order
    checkout_page = CheckoutPage(driver)
    checkout_page.fill_customer_info("John", "Doe", "12345")
    checkout_page.finish_order()

    # 5. Verify the order completed
    assert checkout_page.get_confirmation_message() == "Thank you for your order!"
