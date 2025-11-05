"""
Script Name: homehni_loans.py

Purpose:
    Automate submitting loan requests on HomeHNI Services → Loans page.
    For each submission: fill Phone, City (first option), Loan Type (random),
    Loan Amount, then click Get Pre-Approved Now.

Usage:
    1. pip install selenium
    2. Ensure ChromeDriver is on PATH
    3. Run: python loans.py
    4. Manually log in, navigate to Services page → ensure Loans form is reachable
    5. When prompted in terminal, enter N (number of submissions)
"""

import time
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Configuration
LOAN_PHONE = "9902978675"
LOAN_AMOUNT = "1000000"


def login_and_wait_on_services(driver):
    """Open HomeHNI homepage; user will log in and navigate to Loans form."""
    driver.get("https://homehni.in/")
    input(
        "Please log in (if needed), then navigate to Services → Loans in THIS window.\n"
        "Ensure the form is visible, then press Enter to start..."
    )


def click_loans_tab(driver):
    """Click the Loans tab/button on the Services page if present."""
    try:
        loans_btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    "//button[.//span[normalize-space()='Loans'] or contains(normalize-space(.), 'Loans')]",
                )
            )
        )
        driver.execute_script("arguments[0].scrollIntoView({block:'center'});", loans_btn)
        time.sleep(0.2)
        driver.execute_script("arguments[0].click();", loans_btn)
        return True
    except Exception:
        return False


def _set_value_with_input_event(driver, element, value: str):
    driver.execute_script(
        "arguments[0].focus(); arguments[0].value='';", element
    )
    driver.execute_script(
        "arguments[0].value = arguments[1]; arguments[0].dispatchEvent(new Event('input', {bubbles:true}));",
        element,
        value,
    )


def _get_input_value(driver, element) -> str:
    return driver.execute_script("return arguments[0].value;", element) or ""


def fill_phone_number(driver):
    try:
        phone_input = WebDriverWait(driver, 12).until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    "//input[(contains(@placeholder,'Phone') or @type='tel') and (@name='phone' or @id='loan-phone-mobile')]",
                )
            )
        )
        driver.execute_script("arguments[0].scrollIntoView({block:'center'});", phone_input)
        phone_input.click()
        phone_input.clear()
        phone_input.send_keys(LOAN_PHONE)
        # Verify; fallback to JS if not fully populated
        val = _get_input_value(driver, phone_input)
        if val.strip() != LOAN_PHONE:
            _set_value_with_input_event(driver, phone_input, LOAN_PHONE)
        return True
    except Exception:
        return False


def select_city_first_option(driver):
    """Open City combobox and select the first available option."""
    try:
        # Prefer combobox labeled City
        try:
            city_cb = WebDriverWait(driver, 6).until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//button[@role='combobox' and (.//span[contains(., 'City')] or contains(., 'City'))]")
                )
            )
        except Exception:
            # Fallback: choose the second visible combobox (skip country code)
            all_cb = WebDriverWait(driver, 6).until(
                EC.presence_of_all_elements_located((By.XPATH, "//button[@role='combobox']"))
            )
            visible_cb = [c for c in all_cb if c.is_displayed()]
            city_cb = visible_cb[1] if len(visible_cb) >= 2 else visible_cb[0]
        driver.execute_script("arguments[0].scrollIntoView({block:'center'});", city_cb)
        time.sleep(0.2)
        driver.execute_script("arguments[0].click();", city_cb)
        time.sleep(0.5)
        first_option = WebDriverWait(driver, 6).until(
            EC.element_to_be_clickable((By.XPATH, "(//div[@role='option'] | //li[@role='option'])[1]"))
        )
        driver.execute_script("arguments[0].click();", first_option)
        return True
    except Exception:
        return False


def select_loan_type_random(driver):
    """Open Loan Type combobox and select a random option from the list."""
    try:
        # Prefer combobox labeled Loan Type / Loan
        try:
            type_cb = WebDriverWait(driver, 6).until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//button[@role='combobox' and (.//span[contains(., 'Loan')] or contains(., 'Loan'))]")
                )
            )
        except Exception:
            # Fallback: pick combobox after city (third visible, skipping country)
            all_cb = WebDriverWait(driver, 6).until(
                EC.presence_of_all_elements_located((By.XPATH, "//button[@role='combobox']"))
            )
            visible_cb = [c for c in all_cb if c.is_displayed()]
            type_cb = visible_cb[2] if len(visible_cb) >= 3 else visible_cb[-1]
        driver.execute_script("arguments[0].scrollIntoView({block:'center'});", type_cb)
        time.sleep(0.2)
        driver.execute_script("arguments[0].click();", type_cb)
        time.sleep(0.5)
        options = WebDriverWait(driver, 6).until(
            EC.presence_of_all_elements_located((By.XPATH, "//div[@role='option']"))
        )
        visible = [o for o in options if o.is_displayed()]
        if not visible:
            return False
        idx = random.randint(0, len(visible) - 1)
        driver.execute_script("arguments[0].click();", visible[idx])
        return True
    except Exception:
        return False


def fill_amount(driver):
    try:
        amt_input = WebDriverWait(driver, 12).until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    "//input[(contains(@placeholder,'Loan Amount') or @type='number') and (@name='amount' or @id='loan-amount-mobile')]",
                )
            )
        )
        driver.execute_script("arguments[0].scrollIntoView({block:'center'});", amt_input)
        amt_input.click()
        amt_input.clear()
        amt_input.send_keys(LOAN_AMOUNT)
        val = _get_input_value(driver, amt_input)
        if val.strip() != LOAN_AMOUNT:
            _set_value_with_input_event(driver, amt_input, LOAN_AMOUNT)
        return True
    except Exception:
        return False


def submit_pre_approval(driver):
    try:
        submit_btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    "//button[normalize-space()='Get Pre-Approved Now!' or contains(., 'Get Pre-Approved Now!')]",
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
    """Wait until the form resets (phone and amount inputs become empty)."""
    try:
        WebDriverWait(driver, timeout).until(
            lambda d: (
                (d.find_element(By.ID, "loan-phone-mobile").get_attribute("value") or "") == ""
                and (d.find_element(By.ID, "loan-amount-mobile").get_attribute("value") or "") == ""
            )
        )
        return True
    except Exception:
        return False


def main():
    try:
        n = int(input("How many loan requests do you want to submit? Enter a number: "))
        if n <= 0:
            print("Please enter a positive number.")
            return
    except ValueError:
        print("Please enter a valid number.")
        return

    driver = webdriver.Chrome()
    driver.maximize_window()

    try:
        login_and_wait_on_services(driver)

        successful = 0
        failed = 0

        for i in range(1, n + 1):
            # Ensure Loans tab is active (in case of navigation)
            click_loans_tab(driver)
            time.sleep(0.3)

            ok = True
            ok &= fill_phone_number(driver)
            ok &= select_city_first_option(driver)
            ok &= select_loan_type_random(driver)
            ok &= fill_amount(driver)

            if not ok:
                print(f"✗ Could not prepare form for submission {i}")
                failed += 1
            else:
                submitted = submit_pre_approval(driver)
                if submitted:
                    print(f"✓ Loan request {i} submitted")
                    successful += 1
                else:
                    print(f"✗ Submission click failed for request {i}")
                    failed += 1

            # Wait for automatic form reset; no refresh required
            if i < n:
                reset_ok = wait_for_form_reset(driver, timeout=10)
                # Additional wait as requested
                time.sleep(3)
                if not reset_ok:
                    # As a fallback, try reactivating Loans tab without page reload
                    click_loans_tab(driver)
                time.sleep(0.5)

        print("\n==============================")
        print("LOAN REQUESTS COMPLETE")
        print("==============================")
        print(f"Requested: {n}")
        print(f"Successful: {successful}")
        print(f"Failed: {failed}")
    finally:
        # Give user a moment to review
        try:
            input("Press Enter to close the browser...")
        except Exception:
            pass
        driver.quit()


if __name__ == "__main__":
    main()


