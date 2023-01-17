from playwright.sync_api import sync_playwright

import string
import random
import tomllib
import logging
import os
import sys


DOORDASH_URL = "https://identity.doordash.com/auth/user/signup?client_id=1666519390426295040&enable_last_social=false&intl=en-US&is_iframe_modal=true&layout=identity_web_iframe&prompt=none&redirect_uri=https%3A%2F%2Fwww.doordash.com%2Fpost-login%2F&response_type=code&scope=%2A&state=%2F"
_LOGGER = logging.getLogger("doordash-generator")
logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "INFO"),
    format="%(levelname)-1.1s %(asctime)23.23s %(name)s: %(message)s",
    stream=sys.stderr,
)


class DoordashGenerator:
    def __init__(self):
        self.play = sync_playwright().start()
        self.config = self.load_config("config.toml")

        headless = self.config.get("headless")
        if headless == None:
            headless = True

        self.browser = self.play.firefox.launch(headless=headless)
        pass

    def run(self):
        self.load_config("config.toml")

        quantity = self.config.get("quantity") or 1

        _LOGGER.info(f"Generating {quantity} account(s)...")

        for i in range(quantity):
            try:
                self.automate_signup()
                _LOGGER.info(f"Successfully created account {i + 1} of {quantity}")
            except Exception as e:
                _LOGGER.error(f"Unable to create account: {e}")

    def automate_signup(self):
        context = self.browser.new_context()

        page = context.new_page()

        email = "{}+{}@{}".format(
            self.config["email_name"],
            self.generate_digits(10),
            self.config["email_domain"],
        )

        phone_number = f"0452{self.generate_digits(6)}"

        password = self.config.get("password")
        if password is None:
            password = self.generate_password(12)

        page.goto(DOORDASH_URL)
        page.locator('css=[data-anchor-id="IdentitySignupFirstNameField"]').fill(
            self.config["first_name"]
        )
        page.locator('css=[data-anchor-id="IdentitySignupLastNameField"]').fill(
            self.config["last_name"]
        )
        page.locator('css=[data-anchor-id="IdentitySignupEmailField"]').fill(email)
        page.locator("#FieldWrapper-3").select_option("AU")
        page.locator('css=[data-anchor-id="IdentitySignupPhoneField"]').fill(
            phone_number
        )
        page.locator('css=[data-anchor-id="IdentitySignupPasswordField"]').fill(
            password
        )
        page.locator("button[data-anchor-id=IdentitySignupSubmitButton]").click()
        page.locator("css=[aria-label='Your delivery address']").fill(
            self.config["address"]
        )
        page.locator("css=[data-anchor-id='AddressAutocompleteSuggestion-0']").click()
        page.wait_for_timeout(3000)

        self.save_to_file(email, password)

        context.close()

    @staticmethod
    def save_to_file(email: str, password: str):
        with open("accounts.txt", "a") as f:
            f.write(f"{email}:{password}\n")

    @staticmethod
    def load_config(path: str):
        with open(path, "rb") as f:
            return tomllib.load(f)

    @staticmethod
    def generate_password(length: int) -> str:
        characters = string.ascii_letters + string.digits + "!@#$%^&*"
        return "".join(random.choices(characters, k=length))

    @staticmethod
    def generate_digits(length: int) -> str:
        return "".join(str(random.randint(0, 9)) for _ in range(length))


if __name__ == "__main__":
    DoordashGenerator().run()
