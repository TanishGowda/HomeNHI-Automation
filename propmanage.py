"""
Script Name: homehni_property_management.py

Purpose:
    Automate the Property Management services form on HomeHNI Services page.
    Fills Phone Number, selects City (first option), selects Property Type (random),
    and submits the form.

Usage:
    1. pip install selenium
    2. Ensure ChromeDriver is on PATH
    3. Run: python propmanage.py
    4. Script opens home page; log in if needed and navigate to Services → Property Management
    5. Ensure the form is visible, then press Enter to start
"""

import time
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Configuration
PHONE_NUMBER = "9902978675"


def wait_for_user_on_management_form(driver):
    """Open home page and let the user log in and navigate to the Property Management form."""
    driver.get("https://homehni.in/")
    input(
        "Please log in (if needed), then open Services → Property Management so the form is visible.\n"
        "Press Enter here to begin filling the form..."
    )


def _set_value_with_input_event(driver, element, value: str):
    driver.execute_script(
        "arguments[0].focus(); arguments[0].value='';",
        element,
    )
    driver.execute_script(
        "arguments[0].value = arguments[1]; arguments[0].dispatchEvent(new Event('input', {bubbles:true}));",
        element,
        value,
    )


def _get_value(driver, element) -> str:
    return driver.execute_script("return arguments[0].value;", element) or ""


def fill_phone(driver):
    try:
        phone_input = WebDriverWait(driver, 12).until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    "//input[@id='property-phone-mobile' and @name='phone' and @type='tel'] | "
                    "//input[@type='tel' and contains(@placeholder,'Phone')]",
                )
            )
        )
        driver.execute_script("arguments[0].scrollIntoView({block:'center'});", phone_input)
        phone_input.click()
        phone_input.clear()
        phone_input.send_keys(PHONE_NUMBER)
        if _get_value(driver, phone_input).strip() != PHONE_NUMBER:
            _set_value_with_input_event(driver, phone_input, PHONE_NUMBER)
        return True
    except Exception:
        return False


def select_city_first_option(driver):
    try:
        # Prefer combobox labeled City
        try:
            city_cb = WebDriverWait(driver, 8).until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//button[@role='combobox' and (.//span[contains(., 'City')] or contains(., 'City'))]")
                )
            )
        except Exception:
            # Fallback: choose second visible combobox (skip any country code dropdown)
            all_cb = WebDriverWait(driver, 8).until(
                EC.presence_of_all_elements_located((By.XPATH, "//button[@role='combobox']"))
            )
            visible = [c for c in all_cb if c.is_displayed()]
            city_cb = visible[1] if len(visible) >= 2 else visible[0]

        driver.execute_script("arguments[0].scrollIntoView({block:'center'});", city_cb)
        time.sleep(0.2)
        driver.execute_script("arguments[0].click();", city_cb)
        time.sleep(0.4)
        first_opt = WebDriverWait(driver, 6).until(
            EC.element_to_be_clickable((By.XPATH, "(//div[@role='option'] | //li[@role='option'])[1]"))
        )
        driver.execute_script("arguments[0].click();", first_opt)
        return True
    except Exception:
        return False


def select_property_type_random(driver):
    try:
        # Property Type combobox
        try:
            prop_cb = WebDriverWait(driver, 8).until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//button[@role='combobox' and (.//span[contains(., 'Property Type')] or contains(., 'Property Type'))]")
                )
            )
        except Exception:
            # Fallback: last visible combobox on the form
            all_cb = WebDriverWait(driver, 8).until(
                EC.presence_of_all_elements_located((By.XPATH, "//button[@role='combobox']"))
            )
            visible = [c for c in all_cb if c.is_displayed()]
            prop_cb = visible[-1]

        driver.execute_script("arguments[0].scrollIntoView({block:'center'});", prop_cb)
        time.sleep(0.2)
        driver.execute_script("arguments[0].click();", prop_cb)
        time.sleep(0.4)
        options = WebDriverWait(driver, 6).until(
            EC.presence_of_all_elements_located((By.XPATH, "//div[@role='option']"))
        )
        visible_opts = [o for o in options if o.is_displayed()]
        if not visible_opts:
            return False
        idx = random.randint(0, len(visible_opts) - 1)
        driver.execute_script("arguments[0].click();", visible_opts[idx])
        return True
    except Exception:
        return False


def submit_support(driver):
    try:
        submit_btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    "//button[contains(., 'Get Professional Support') or contains(., 'Get Property') or @type='submit']",
                )
            )
        )
        driver.execute_script("arguments[0].scrollIntoView({block:'center'});", submit_btn)
        time.sleep(0.2)
        driver.execute_script("arguments[0].click();", submit_btn)
        return True
    except Exception:
        return False


def wait_for_form_reset(driver, timeout: int = 10):
    """Wait until the form resets (phone input becomes empty)."""
    try:
        WebDriverWait(driver, timeout).until(
            lambda d: (
                (d.find_element(By.ID, "property-phone-mobile").get_attribute("value") or "") == ""
            )
        )
        return True
    except Exception:
        return False


def main():
    # Ask user for number of requests to submit
    try:
        num_requests = int(input("How many Property Management requests do you want to submit? Enter a number: "))
        if num_requests <= 0:
            print("Please enter a positive number.")
            return
    except ValueError:
        print("Please enter a valid number.")
        return

    driver = webdriver.Chrome()
    driver.maximize_window()

    try:
        wait_for_user_on_management_form(driver)

        successful = 0
        failed = 0

        for i in range(1, num_requests + 1):
            ok = True
            ok &= fill_phone(driver)
            ok &= select_city_first_option(driver)
            ok &= select_property_type_random(driver)

            if not ok:
                print(f"✗ Could not prepare form for submission {i}")
                failed += 1
            else:
                if submit_support(driver):
                    print(f"✓ Property Management request {i} submitted successfully")
                    successful += 1
                else:
                    print(f"✗ Submission click failed for request {i}")
                    failed += 1

            if i < num_requests:
                reset_ok = wait_for_form_reset(driver, timeout=10)
                time.sleep(3)
                if not reset_ok:
                    print(f"⚠️  Form may not have reset for request {i}; continuing anyway...")
                time.sleep(0.5)

        print("\n==============================")
        print("PROPERTY MANAGEMENT REQUESTS COMPLETE")
        print("==============================")
        print(f"Requested: {num_requests}")
        print(f"Successful: {successful}")
        print(f"Failed: {failed}")

        input("Press Enter to close the browser...")
    finally:
        driver.quit()


if __name__ == "__main__":
    main()


