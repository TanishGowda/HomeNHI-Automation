"""
Script Name: homehni_commercial_rent_property.py

Purpose:
    This script automates filling the Commercial Rent property posting form on HomeHNI.
    It handles the initial contact details and property ad type selection for Commercial Rent properties.

Usage:
    1. Install selenium: pip install selenium
    2. Download ChromeDriver and ensure it's in your PATH
    3. Run: python Commercial_Rent.py
    4. Manually log in and click "Post Property" 
    5. Press Enter in terminal to start automation
"""

import time
import os
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

# Configuration
PRIMARY_NAME = "Tanish"
PRIMARY_MOBILE = "9902978675"

# Property Details Configuration
SUPER_BUILT_UP_AREA = "10000"

# Rental Details Configuration
EXPECTED_RENT = "10000"
EXPECTED_DEPOSIT = "20000"

# Amenities Configuration
DIRECTIONS_TIP = "Come straight from Top in Town and take a left."

# Gallery Configuration
IMAGE_PATH = "try.png"  # Path to the image file to upload

def wait_and_click(driver, by, locator, timeout=20):
    """Wait for an element to be clickable and then click it."""
    element = WebDriverWait(driver, timeout).until(EC.element_to_be_clickable((by, locator)))
    try:
        element.click()
    except:
        # If regular click fails, try JavaScript click
        driver.execute_script("arguments[0].click();", element)

def wait_and_send_keys(driver, by, locator, text, timeout=20):
    """Wait for an input element and send keys to it."""
    element = WebDriverWait(driver, timeout).until(
        EC.visibility_of_element_located((by, locator))
    )
    element.clear()
    element.send_keys(text)

def login_and_wait(driver):
    """
    Navigate to HomeHNI homepage and pause for manual login and navigation.
    Once you are logged in and have clicked on 'Post Property' to reach the
    first page form, press Enter in your terminal to continue.
    """
    driver.get("https://homehni.in")
    input("Please complete the login process, click on 'Post Property', and when you reach the first page form, press Enter here to continue...")

def fill_first_page(driver):
    """Fill the first page form - select city, Commercial option, and submit.
    More robust with retries, scrolling, and JS clicks to avoid interceptions.
    """
    print("Starting to fill first page...")
    print("Note: Name and Mobile are pre-filled automatically")

    def try_fill_once():
        # Mobile Number - Fill with phone number
        try:
            mobile_input = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//input[@id='mobile']"))
            )
            mobile_input.clear()
            mobile_input.send_keys(PRIMARY_MOBILE)
            print(f"✓ Mobile Number filled: {PRIMARY_MOBILE}")
        except Exception as e:
            print("✗ Could not fill Mobile Number field:", str(e))

        # City dropdown - always select first option in the list
        try:
            city_combobox = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[@role='combobox' and contains(., 'Select city')]"))
            )
            driver.execute_script("arguments[0].scrollIntoView({block:'center'});", city_combobox)
            driver.execute_script("arguments[0].click();", city_combobox)
            time.sleep(1)
            try:
                first_opt = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.XPATH, "(//div[@role='option'] | //li[@role='option'])[1]"))
                )
                driver.execute_script("arguments[0].click();", first_opt)
                print("✓ City selected (first option)")
            except:
                # Fallback: type any character and pick first suggestion
                try:
                    city_input = WebDriverWait(driver, 5).until(
                        EC.element_to_be_clickable((By.XPATH, "//input[@type='text' and contains(@placeholder, 'city')]"))
                    )
                    city_input.clear()
                    city_input.send_keys("a")
                    time.sleep(1)
                    first_opt = WebDriverWait(driver, 5).until(
                        EC.element_to_be_clickable((By.XPATH, "(//div[@role='option'] | //li[@role='option'])[1]"))
                    )
                    driver.execute_script("arguments[0].click();", first_opt)
                    print("✓ City selected (typed, first option)")
                except:
                    print("⚠️  Skipping city selection this attempt")
        except Exception as e:
            print("⚠️  City combobox not ready:", str(e))

        # Commercial button (scoped within the same form section as the submit button)
        try:
            commercial_button = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//div[.//button[normalize-space()='Start Posting Your Ad For FREE']]//button[normalize-space()='Commercial']"))
            )
            driver.execute_script("arguments[0].scrollIntoView({block:'center'});", commercial_button)
            time.sleep(0.3)
            driver.execute_script("arguments[0].click();", commercial_button)
            print("✓ Commercial button clicked")
        except Exception as e:
            print("✗ Could not click Commercial:", str(e))

        # Rent button (after clicking Commercial)
        try:
            rent_button = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//button[normalize-space()='Rent']"))
            )
            driver.execute_script("arguments[0].scrollIntoView({block:'center'});", rent_button)
            time.sleep(0.3)
            driver.execute_script("arguments[0].click();", rent_button)
            print("✓ Rent button clicked")
        except Exception as e:
            print("✗ Could not click Rent:", str(e))

        # Submit button: wait until enabled (no disabled attribute), then click
        try:
            submit_button = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//button[normalize-space()='Start Posting Your Ad For FREE']"))
            )
            # wait until button is enabled
            WebDriverWait(driver, 10).until(lambda d: submit_button.get_attribute('disabled') is None)
            driver.execute_script("arguments[0].scrollIntoView({block:'center'});", submit_button)
            time.sleep(0.3)
            driver.execute_script("arguments[0].click();", submit_button)
            print("✓ Submit button clicked - proceeding to next page")
            return True
        except Exception as e:
            print("✗ Could not click Submit:", str(e))
            return False

    # Try once; if fail, reload post page and retry once
    success = try_fill_once()
    if not success:
        try:
            driver.get("https://homehni.in/post-property")
            WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.XPATH, "//button[@role='combobox' and contains(., 'Select city')] | //button[contains(., 'Start Posting Your Ad For FREE')]"))
            )
            print("↻ Retrying first page after reload...")
            try_fill_once()
        except Exception:
            pass

def fill_property_details(driver):
    """Fill the property details page form."""
    print("Starting to fill property details page...")
    
    # Wait for page transition
    time.sleep(3)
    
    # Super Built Up Area - Direct approach
    try:
        all_inputs = driver.find_elements(By.XPATH, "//input[@name='superBuiltUpArea']")
        visible_inputs = [inp for inp in all_inputs if inp.is_displayed()]
        if visible_inputs:
            visible_inputs[0].clear()
            visible_inputs[0].send_keys(SUPER_BUILT_UP_AREA)
            print("✓ Super Built Up Area filled:", SUPER_BUILT_UP_AREA)
    except Exception as e:
        print("✗ Could not fill Super Built Up Area field:", str(e))

    # Dropdowns on this page - target specific dropdowns by their text/label
    try:
        # Close stray popovers
        driver.execute_script("document.body.click();")
        time.sleep(0.3)
        
        # Target specific dropdowns by their unique text
        dropdowns_to_fill = [
            ("Space Type", "//button[@role='combobox' and contains(., 'Select Space Type')]"),
            ("Building Type", "//button[@role='combobox' and contains(., 'Select Building Type')]"),
            ("Age of Property", "//button[@role='combobox' and contains(., 'Select Age')]"),
            ("Facing", "//button[@role='combobox']//div[contains(@class, 'flex items-center gap-2')]//svg[@class='lucide lucide-compass']/ancestor::button"),
            ("Furnishing", "//button[@role='combobox' and contains(., 'Select Furnishing')]")
        ]
        
        for dropdown_name, xpath_selector in dropdowns_to_fill:
            try:
                # Find the specific dropdown by XPath
                combobox = driver.find_element(By.XPATH, xpath_selector)
                
                # Check if it's visible
                if not combobox.is_displayed():
                    print(f"⚠️  {dropdown_name} combobox not visible")
                    continue
                
                # Scroll and click
                driver.execute_script("arguments[0].scrollIntoView({block:'center'});", combobox)
                time.sleep(0.2)
                driver.execute_script("arguments[0].click();", combobox)
                
                # Select first option
                first_option = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.XPATH, "//div[@role='option'][1]"))
                )
                driver.execute_script("arguments[0].click();", first_option)
                print(f"✓ {dropdown_name} selected (first option)")
                time.sleep(0.2)
            except Exception as inner_e:
                print(f"⚠️  {dropdown_name} selection failed:", str(inner_e))
                driver.execute_script("document.body.click();")
                time.sleep(0.2)
    except Exception as e:
        print("✗ Could not process dropdown selections:", str(e))

    # Click Save & Continue button
    try:
        # Try multiple selectors for Save & Continue button
        save_button = None
        selectors = [
            "//button[contains(text(), 'Save & Continue')]",
            "//button[contains(text(), 'Save &amp; Continue')]",
            "//button[contains(@class, 'bg-red-600') and contains(text(), 'Save')]",
            "//button[@type='button' and contains(text(), 'Save')]"
        ]
        
        for selector in selectors:
            try:
                elements = driver.find_elements(By.XPATH, selector)
                visible_elements = [el for el in elements if el.is_displayed()]
                if visible_elements:
                    save_button = visible_elements[0]
                    break
            except:
                continue
        
        if save_button:
            driver.execute_script("arguments[0].click();", save_button)
            print("✓ Save & Continue button clicked - proceeding to next page")
        else:
            print("✗ Could not find Save & Continue button with any selector")
    except Exception as e:
        print("✗ Could not find Save & Continue button:", str(e))

def fill_locality_details_page(driver):
    """Fill the locality details page - city and locality with autocomplete."""
    print("Starting to fill locality details page...")
    
    # Wait for page transition
    time.sleep(3)
    
    # City input - Type "Bangalore" and select first suggestion
    try:
        city_input = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//input[@name='city']"))
        )
        city_input.clear()
        city_input.send_keys("Bangalore")
        time.sleep(1.5)  # Wait for autocomplete suggestions
        
        # Click first suggestion with JavaScript to avoid click interception
        first_suggestion = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, "//div[@class='pac-item'][1]"))
        )
        driver.execute_script("arguments[0].click();", first_suggestion)
        print("✓ City selected: Bangalore")
    except Exception as e:
        print("✗ Could not fill City field:", str(e))
    
    # Locality input - Type "Bellandur" and select first suggestion
    try:
        locality_input = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//input[@name='locality']"))
        )
        locality_input.clear()
        locality_input.send_keys("Bellandur")
        time.sleep(1.5)  # Wait for autocomplete suggestions
        
        # Click first suggestion with JavaScript to avoid click interception
        first_suggestion = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, "//div[@class='pac-item'][1]"))
        )
        driver.execute_script("arguments[0].click();", first_suggestion)
        print("✓ Locality selected: Bellandur")
    except Exception as e:
        print("✗ Could not fill Locality field:", str(e))
    
    # Click Save & Continue button
    try:
        # Try multiple selectors for Save & Continue button
        save_button = None
        selectors = [
            "//button[contains(text(), 'Save & Continue')]",
            "//button[contains(text(), 'Save &amp; Continue')]",
            "//button[contains(@class, 'bg-red-600') and contains(text(), 'Save')]",
            "//button[@type='button' and contains(text(), 'Save')]"
        ]
        
        for selector in selectors:
            try:
                elements = driver.find_elements(By.XPATH, selector)
                visible_elements = [el for el in elements if el.is_displayed()]
                if visible_elements:
                    save_button = visible_elements[0]
                    break
            except:
                continue
        
        if save_button:
            driver.execute_script("arguments[0].click();", save_button)
            print("✓ Save & Continue button clicked - proceeding to next page")
        else:
            print("✗ Could not find Save & Continue button with any selector")
    except Exception as e:
        print("✗ Could not find Save & Continue button:", str(e))

def fill_rental_details_page(driver):
    """Fill the rental details page - rent, deposit, lease duration, lock-in period, and amenities."""
    print("Starting to fill rental details page...")
    
    # Wait for page transition
    time.sleep(3)
    
    # Expected Rent - Direct approach using placeholder
    try:
        all_inputs = driver.find_elements(By.XPATH, "//input[@placeholder='Enter Amount']")
        # Get all inputs with type='number'
        number_inputs = [inp for inp in all_inputs if inp.get_attribute('type') == 'number' and inp.is_displayed()]
        
        if len(number_inputs) >= 1:
            number_inputs[0].clear()
            number_inputs[0].send_keys(EXPECTED_RENT)
            print("✓ Expected Rent filled:", EXPECTED_RENT)
    except Exception as e:
        print("✗ Could not fill Expected Rent field:", str(e))
    
    # Expected Deposit - Second input with type='number'
    try:
        all_inputs = driver.find_elements(By.XPATH, "//input[@placeholder='Enter Amount']")
        number_inputs = [inp for inp in all_inputs if inp.get_attribute('type') == 'number' and inp.is_displayed()]
        
        if len(number_inputs) >= 2:
            number_inputs[1].clear()
            number_inputs[1].send_keys(EXPECTED_DEPOSIT)
            print("✓ Expected Deposit filled:", EXPECTED_DEPOSIT)
    except Exception as e:
        print("✗ Could not fill Expected Deposit field:", str(e))
    
    # Lease Duration and Lock-in Period dropdowns
    try:
        # Close any stray popovers
        driver.execute_script("document.body.click();")
        time.sleep(0.3)
        
        # Target specific dropdowns by their text
        dropdowns_to_fill = [
            ("Lease Duration", "//button[@role='combobox' and contains(., 'Lease Duration')]"),
            ("Lock-in Period", "//button[@role='combobox' and contains(., 'Lock-in Period')]")
        ]
        
        for dropdown_name, xpath_selector in dropdowns_to_fill:
            try:
                combobox = driver.find_element(By.XPATH, xpath_selector)
                
                if not combobox.is_displayed():
                    print(f"⚠️  {dropdown_name} combobox not visible")
                    continue
                
                driver.execute_script("arguments[0].scrollIntoView({block:'center'});", combobox)
                time.sleep(0.2)
                driver.execute_script("arguments[0].click();", combobox)
                
                first_option = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.XPATH, "//div[@role='option'][1]"))
                )
                driver.execute_script("arguments[0].click();", first_option)
                print(f"✓ {dropdown_name} selected (first option)")
                time.sleep(0.2)
            except Exception as inner_e:
                print(f"⚠️  {dropdown_name} selection failed:", str(inner_e))
                driver.execute_script("document.body.click();")
                time.sleep(0.2)
    except Exception as e:
        print("✗ Could not process dropdown selections:", str(e))
    
    # Select checkboxes: Bank and ATM
    checkbox_ids = ["Bank", "ATM"]
    
    for checkbox_id in checkbox_ids:
        try:
            checkbox = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, f"//button[@id='{checkbox_id}']"))
            )
            driver.execute_script("arguments[0].click();", checkbox)
            print(f"✓ {checkbox_id} selected")
        except Exception as e:
            print(f"✗ Could not select {checkbox_id}:", str(e))
    
    # Click Save & Continue button
    try:
        # Try multiple selectors for Save & Continue button
        save_button = None
        selectors = [
            "//button[contains(text(), 'Save & Continue')]",
            "//button[contains(text(), 'Save &amp; Continue')]",
            "//button[contains(@class, 'bg-red-600') and contains(text(), 'Save')]",
            "//button[@type='button' and contains(text(), 'Save')]"
        ]
        
        for selector in selectors:
            try:
                elements = driver.find_elements(By.XPATH, selector)
                visible_elements = [el for el in elements if el.is_displayed()]
                if visible_elements:
                    save_button = visible_elements[0]
                    break
            except:
                continue
        
        if save_button:
            driver.execute_script("arguments[0].click();", save_button)
            print("✓ Save & Continue button clicked - proceeding to next page")
        else:
            print("✗ Could not find Save & Continue button with any selector")
    except Exception as e:
        print("✗ Could not find Save & Continue button:", str(e))

def fill_amenities_page(driver):
    """Fill the amenities page - dropdowns and directions."""
    print("Starting to fill amenities page...")
    
    # Wait for page transition
    time.sleep(3)
    
    # Handle all dropdowns - select first option for each
    try:
        # Close any stray popovers
        driver.execute_script("document.body.click();")
        time.sleep(0.3)
        
        # Target specific dropdowns by their unique placeholder text
        dropdowns_to_fill = [
            ("Power Backup", "//button[@role='combobox' and contains(., 'Select power backup')]"),
            ("Lift", "//button[@role='combobox' and contains(., 'Select lift availability')]"),
            ("Parking", "//button[@role='combobox' and contains(., 'Select parking')]"),
            ("Water Storage Facility", "//button[@role='combobox' and contains(., 'Select water storage')]"),
            ("Security", "//button[@role='combobox' and contains(., 'Select security')]"),
            ("Current Property Condition", "//button[@role='combobox' and contains(., 'Select condition')]")
        ]
        
        for dropdown_name, xpath_selector in dropdowns_to_fill:
            try:
                combobox = driver.find_element(By.XPATH, xpath_selector)
                
                if not combobox.is_displayed():
                    print(f"⚠️  {dropdown_name} combobox not visible")
                    continue
                
                driver.execute_script("arguments[0].scrollIntoView({block:'center'});", combobox)
                time.sleep(0.2)
                driver.execute_script("arguments[0].click();", combobox)
                
                first_option = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.XPATH, "//div[@role='option'][1]"))
                )
                driver.execute_script("arguments[0].click();", first_option)
                print(f"✓ {dropdown_name} selected (first option)")
                time.sleep(0.2)
            except Exception as inner_e:
                print(f"⚠️  {dropdown_name} selection failed:", str(inner_e))
                driver.execute_script("document.body.click();")
                time.sleep(0.2)
    except Exception as e:
        print("✗ Could not process dropdown selections:", str(e))
    
    # Directions to Property textarea
    try:
        directions_textarea = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//textarea[@name='directionsTip']"))
        )
        directions_textarea.clear()
        directions_textarea.send_keys(DIRECTIONS_TIP)
        print(f"✓ Directions to Property filled: {DIRECTIONS_TIP}")
    except Exception as e:
        print("✗ Could not fill Directions to Property field:", str(e))
    
    # Click Save & Continue button
    try:
        # Try multiple selectors for Save & Continue button
        save_button = None
        selectors = [
            "//button[contains(text(), 'Save & Continue')]",
            "//button[contains(text(), 'Save &amp; Continue')]",
            "//button[contains(@class, 'bg-red-600') and contains(text(), 'Save')]",
            "//button[@type='button' and contains(text(), 'Save')]"
        ]
        
        for selector in selectors:
            try:
                elements = driver.find_elements(By.XPATH, selector)
                visible_elements = [el for el in elements if el.is_displayed()]
                if visible_elements:
                    save_button = visible_elements[0]
                    break
            except:
                continue
        
        if save_button:
            driver.execute_script("arguments[0].click();", save_button)
            print("✓ Save & Continue button clicked - proceeding to next page")
        else:
            print("✗ Could not find Save & Continue button with any selector")
    except Exception as e:
        print("✗ Could not find Save & Continue button:", str(e))

def fill_gallery_page(driver):
    """Fill the gallery page by uploading images to all categories."""
    print("Starting to fill gallery page...")
    
    # Get absolute path to the image file
    current_dir = os.path.dirname(os.path.abspath(__file__))
    image_absolute_path = os.path.join(current_dir, IMAGE_PATH)
    
    # Check if image exists
    if not os.path.exists(image_absolute_path):
        print(f"✗ Image file not found: {image_absolute_path}")
        print("⚠️  Skipping gallery upload")
    else:
        print(f"✓ Found image file: {image_absolute_path}")
        
        # Wait for page transition
        time.sleep(3)
        
        # Find all file inputs and upload images
        try:
            # Find all file inputs that accept images
            file_inputs = driver.find_elements(By.XPATH, "//input[@type='file' and @accept='image/*']")
            visible_file_inputs = [inp for inp in file_inputs if inp.is_displayed()]
            
            print(f"Found {len(file_inputs)} total file inputs, {len(visible_file_inputs)} visible")
            
            # Upload to the first 3 visible file inputs (Front View, Interior View, Others)
            gallery_categories = ["Front View", "Interior View", "Others"]
            
            for i in range(min(3, len(visible_file_inputs))):
                try:
                    file_input = visible_file_inputs[i]
                    
                    # Scroll to make sure the element is in view
                    driver.execute_script("arguments[0].scrollIntoView(true);", file_input)
                    time.sleep(0.5)
                    
                    # Upload the image
                    file_input.send_keys(image_absolute_path)
                    print(f"✓ Uploaded image to {gallery_categories[i]}")
                    time.sleep(1)
                    
                except Exception as e:
                    print(f"✗ Could not upload image to {gallery_categories[i]}:", str(e))
                    
        except Exception as e:
            print("✗ Could not find file inputs for images:", str(e))
    
    # Click Save & Continue button
    try:
        # Try multiple selectors for Save & Continue button
        save_button = None
        selectors = [
            "//button[contains(text(), 'Save & Continue')]",
            "//button[contains(text(), 'Save &amp; Continue')]",
            "//button[contains(@class, 'bg-red-600') and contains(text(), 'Save')]",
            "//button[@type='button' and contains(text(), 'Save')]"
        ]
        
        for selector in selectors:
            try:
                elements = driver.find_elements(By.XPATH, selector)
                visible_elements = [el for el in elements if el.is_displayed()]
                if visible_elements:
                    save_button = visible_elements[0]
                    break
            except:
                continue
        
        if save_button:
            driver.execute_script("arguments[0].click();", save_button)
            print("✓ Save & Continue button clicked - proceeding to next page")
        else:
            print("✗ Could not find Save & Continue button with any selector")
    except Exception as e:
        print("✗ Could not find Save & Continue button:", str(e))

def fill_schedule_and_submit(driver):
    """Fill the schedule page and submit the property."""
    print("Starting to fill schedule page...")
    
    # Wait for page transition
    time.sleep(3)
    
    # Click Submit Property button
    try:
        submit_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Submit Property')]"))
        )
        driver.execute_script("arguments[0].scrollIntoView({block:'center'});", submit_button)
        time.sleep(0.5)
        driver.execute_script("arguments[0].click();", submit_button)
        print("✓ Submit Property button clicked - property submitted!")
        
        # Wait for submission to complete
        time.sleep(3)
        
    except Exception as e:
        print("✗ Could not find or click Submit Property button:", str(e))

def start_new_post(driver):
    """Navigate to post property page to start a new property posting."""
    print("Starting new property posting...")
    
    try:
        driver.get("https://homehni.in/post-property")
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.XPATH, "//button[@role='combobox' and contains(., 'Select city')] | //button[contains(., 'Start Posting Your Ad For FREE')]"))
        )
        print("✓ Navigated to post property page - ready for next property")
        time.sleep(2)
    except Exception as e:
        print("✗ Could not navigate to post property page:", str(e))

def run_full_post_flow(driver, property_index):
    """Run the complete property posting flow for one property."""
    print(f"\n{'='*50}")
    print(f"COMMERCIAL RENT PROPERTY {property_index} - Starting posting flow")
    print(f"{'='*50}")
    
    try:
        # Fill the first page form
        fill_first_page(driver)
        time.sleep(3)

        # Fill the property details page
        fill_property_details(driver)
        time.sleep(3)

        # Fill the locality details page
        fill_locality_details_page(driver)
        time.sleep(3)

        # Fill the rental details page
        fill_rental_details_page(driver)
        time.sleep(3)

        # Fill the amenities page
        fill_amenities_page(driver)
        time.sleep(3)

        # Fill the gallery page
        fill_gallery_page(driver)
        time.sleep(3)

        # Fill the schedule page and submit
        fill_schedule_and_submit(driver)
        
        print(f"✓ Commercial Rent Property {property_index} submitted successfully!")
        return True
        
    except Exception as e:
        print(f"✗ Error posting Commercial Rent property {property_index}: {str(e)}")
        return False

def main():
    """Main entry point."""
    # Ask user for number of properties to post
    try:
        num_properties = int(input("How many Commercial Rent properties do you want to post? Enter a number: "))
        if num_properties <= 0:
            print("Please enter a positive number.")
            return
    except ValueError:
        print("Please enter a valid number.")
        return

    # Initialize Chrome WebDriver
    driver = webdriver.Chrome()
    driver.maximize_window()

    try:
        # Navigate to HomeHNI and wait for manual login
        login_and_wait(driver)

        successful_posts = 0
        failed_posts = 0

        # Post each property
        for i in range(1, num_properties + 1):
            try:
                # Run the complete flow for one property
                success = run_full_post_flow(driver, i)
                
                if success:
                    successful_posts += 1
                    print(f"✓ Commercial Rent Property {i} completed successfully!")
                else:
                    failed_posts += 1
                    print(f"✗ Commercial Rent Property {i} failed!")
                
                # If not the last property, start a new post
                if i < num_properties:
                    print(f"\nStarting Commercial Rent property {i+1}...")
                    start_new_post(driver)
                    time.sleep(2)
                    
            except Exception as e:
                print(f"✗ Error with Commercial Rent property {i}: {str(e)}")
                failed_posts += 1
                
                # If not the last property, try to start a new post
                if i < num_properties:
                    try:
                        start_new_post(driver)
                        time.sleep(2)
                    except:
                        print("Could not start new post. Please check the browser manually.")
                        break

        # Final summary
        print(f"\n{'='*60}")
        print(f"COMMERCIAL RENT POSTING COMPLETE!")
        print(f"{'='*60}")
        print(f"Total properties requested: {num_properties}")
        print(f"Successfully posted: {successful_posts}")
        print(f"Failed posts: {failed_posts}")
        print(f"Success rate: {(successful_posts/num_properties)*100:.1f}%")
        print(f"{'='*60}")

        input("Press Enter to close the browser...")

    except Exception as e:
        print(f"An error occurred: {str(e)}")
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
