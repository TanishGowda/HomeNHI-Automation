"""
Script Name: homehni_architect_services.py

Purpose:
    Automate the Architect Services form on HomeHNI Services page.
    Fills Phone Number, selects City (first option), selects Project Type (random),
    sets Project Location to Bengaluru, and submits the form.

Usage:
    1. pip install selenium
    2. Ensure ChromeDriver is on PATH
    3. Run: python architect.py
    4. Script opens home page; log in if needed and navigate to Services → Architects
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
PROJECT_LOCATION = "Bengaluru"


def wait_for_user_on_architect_form(driver):
    """Open home page and let the user log in and navigate to the Architect Services form."""
    driver.get("https://homehni.in/")
    input(
        "Please log in (if needed), then open Services → Architects so the form is visible.\n"
        "Press Enter here to begin filling the form..."
    )


def _set_value_with_input_event(driver, element, value: str):
    driver.execute_script(
        "arguments[0].focus(); arguments[0].value='';",
        element,
    )
    driver.execute_script(
        "arguments[0].value = arguments[1];"
        "arguments[0].dispatchEvent(new Event('input', {bubbles:true}));"
        "arguments[0].dispatchEvent(new Event('change', {bubbles:true}));",
        element,
        value,
    )
    driver.execute_script("arguments[0].blur();", element)


def _set_value_native(driver, element, value: str):
    """Use the native value setter so React/Vue controlled inputs pick up the change."""
    driver.execute_script(
        "const el=arguments[0], val=arguments[1];\n"
        "const proto=Object.getPrototypeOf(el);\n"
        "const desc=Object.getOwnPropertyDescriptor(proto,'value');\n"
        "desc.set.call(el, val);\n"
        "el.dispatchEvent(new Event('input', {bubbles:true}));\n"
        "el.dispatchEvent(new Event('change', {bubbles:true}));",
        element,
        value,
    )


def _get_value(driver, element) -> str:
    return driver.execute_script("return arguments[0].value;", element) or ""


def fill_phone(driver):
    try:
        # Find all possible phone inputs and pick the first visible, enabled one
        WebDriverWait(driver, 12).until(
            EC.presence_of_all_elements_located((By.XPATH, "//input[@type='tel']"))
        )
        candidates = driver.find_elements(By.XPATH, "//input[@type='tel' and (@id='arch-phone' or contains(@placeholder,'Phone'))]")
        visible = [el for el in candidates if el.is_displayed() and el.get_attribute('disabled') is None]
        phone_input = visible[0] if visible else candidates[0]

        driver.execute_script("arguments[0].scrollIntoView({block:'center'});", phone_input)
        try:
            phone_input.click()
        except Exception:
            driver.execute_script("arguments[0].focus();", phone_input)
        try:
            phone_input.clear()
        except Exception:
            pass
        phone_input.send_keys(PHONE_NUMBER)
        if _get_value(driver, phone_input).strip() != PHONE_NUMBER:
            _set_value_with_input_event(driver, phone_input, PHONE_NUMBER)
        return True
    except Exception:
        return False


def set_project_location(driver):
    try:
        loc_input = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//input[@id='arch-location' and @name='location'] | //input[contains(@placeholder,'Project Location')]"))
        )
        driver.execute_script("arguments[0].scrollIntoView({block:'center'});", loc_input)
        loc_input.click()
        loc_input.clear()
        loc_input.send_keys(PROJECT_LOCATION)
        if _get_value(driver, loc_input).strip() != PROJECT_LOCATION:
            _set_value_with_input_event(driver, loc_input, PROJECT_LOCATION)
        return True
    except Exception:
        return False


def select_city_first_option(driver):
    try:
        # Prefer specific Architect city combobox by id or span text
        try:
            city_cb = WebDriverWait(driver, 8).until(
                EC.element_to_be_clickable((By.XPATH, "//button[@role='combobox' and (@id='arch-city' or .//span[contains(., 'Select City')] or contains(., 'Select City') or contains(., 'City'))]"))
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


def select_project_type_random(driver):
    try:
        # Use button by id arch-project-type or span text Project Type
        try:
            pt_cb = WebDriverWait(driver, 8).until(
                EC.element_to_be_clickable((By.XPATH, "//button[@role='combobox' and (@id='arch-project-type' or .//span[contains(., 'Project Type')] or contains(., 'Project Type'))]"))
            )
        except Exception:
            # Fallback: last visible combobox
            all_cb = WebDriverWait(driver, 8).until(
                EC.presence_of_all_elements_located((By.XPATH, "//button[@role='combobox']"))
            )
            visible = [c for c in all_cb if c.is_displayed()]
            pt_cb = visible[-1]

        driver.execute_script("arguments[0].scrollIntoView({block:'center'});", pt_cb)
        time.sleep(0.2)
        driver.execute_script("arguments[0].click();", pt_cb)
        time.sleep(0.4)

        # Scope the options to this combobox using its aria-controls if present
        try:
            listbox_id = pt_cb.get_attribute('aria-controls')
        except Exception:
            listbox_id = None

        if listbox_id:
            opt_xpath = f"//*[@id='{listbox_id}']//div[@role='option']"
        else:
            opt_xpath = "//div[@role='option']"

        options = WebDriverWait(driver, 6).until(
            EC.presence_of_all_elements_located((By.XPATH, opt_xpath))
        )
        visible_opts = [o for o in options if o.is_displayed()]
        if not visible_opts:
            return False
        # Avoid picking an empty option if present
        non_empty = [o for o in visible_opts if (o.text or '').strip() != ''] or visible_opts
        choice = random.choice(non_empty)
        driver.execute_script("arguments[0].click();", choice)
        return True
    except Exception:
        return False


def click_submit(driver):
    try:
        # Prefer visible "Get Free Consultation!" button
        candidates = driver.find_elements(
            By.XPATH,
            "//button[normalize-space()='Get Free Consultation!' or contains(., 'Get Free Consultation!')]",
        )
        visible = [b for b in candidates if b.is_displayed()]
        if not visible:
            # Fall back to other submit buttons
            candidates = driver.find_elements(
                By.XPATH,
                "//button[contains(., 'Get Professional Support') or contains(., 'Get Project') or @type='submit']",
            )
            visible = [b for b in candidates if b.is_displayed()]
        if not visible:
            # As last resort, wait for any clickable submit-like button
            submit_btn = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']"))
            )
        else:
            submit_btn = visible[0]

        driver.execute_script("arguments[0].scrollIntoView({block:'center'});", submit_btn)
        time.sleep(0.2)
        driver.execute_script("arguments[0].click();", submit_btn)
        return True
    except Exception:
        return False


def wait_for_form_reset(driver, timeout: int = 10):
    try:
        WebDriverWait(driver, timeout).until(
            lambda d: (d.find_element(By.ID, "arch-phone").get_attribute("value") or "") == ""
        )
        return True
    except Exception:
        return False


def main():
    # Ask user for number of requests to submit
    try:
        num_requests = int(input("How many Architect Services requests do you want to submit? Enter a number: "))
        if num_requests <= 0:
            print("Please enter a positive number.")
            return
    except ValueError:
        print("Please enter a valid number.")
        return

    driver = webdriver.Chrome()
    driver.maximize_window()

    try:
        wait_for_user_on_architect_form(driver)

        successful = 0
        failed = 0

        for i in range(1, num_requests + 1):
            ok = True
            ok &= fill_phone(driver)
            ok &= select_project_type_random(driver)
            ok &= set_project_location(driver)
            ok &= select_city_first_option(driver)

            if not ok:
                print(f"✗ Could not prepare form for submission {i}")
                failed += 1
            else:
                if click_submit(driver):
                    print(f"✓ Architect Services request {i} submitted successfully")
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
        print("ARCHITECT SERVICES REQUESTS COMPLETE")
        print("==============================")
        print(f"Requested: {num_requests}")
        print(f"Successful: {successful}")
        print(f"Failed: {failed}")

        input("Press Enter to close the browser...")
    finally:
        driver.quit()


if __name__ == "__main__":
    main()


