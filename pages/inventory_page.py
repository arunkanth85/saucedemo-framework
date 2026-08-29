from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class InventoryPage(BasePage):
    ADD_BACKPACK_BUTTON = (By.ID, "add-to-cart-sauce-labs-backpack")
    CART_ICON = (By.CSS_SELECTOR, ".shopping_cart_link")
    CART_BADGE = (By.CSS_SELECTOR, ".shopping_cart_badge")

    def add_backpack_to_cart(self):
        self.click(self.ADD_BACKPACK_BUTTON)

    def get_cart_count(self):
        return self.get_text(self.CART_BADGE)

    def go_to_cart(self):
        self.click(self.CART_ICON)
