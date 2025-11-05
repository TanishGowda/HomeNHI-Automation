"""
Script Name: homehni_commercial_sale_property.py

Purpose:
    This script automates filling the Commercial Sale property posting form on HomeHNI.
    It handles the initial contact details and property ad type selection for Commercial Sale properties.

Usage:
    1. Install selenium: pip install selenium
    2. Download ChromeDriver and ensure it's in your PATH
    3. Run: python Commercial_Sale.py
    4. Manually log in and click "Post Property" 
    5. Press Enter in terminal to start automation
"""

import time
import os
import random
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
PROPERTY_NAME = "Commercial Sale"
SUPER_BUILT_UP_AREA = "10000"

# Locality Details Configuration - Dynamic cities and localities
CITIES_LOCALITIES = [
    ("Bangalore", "Bellandur"),
    ("Mumbai", "Thane"),
    ("Hyderabad", "mgroad")
]

# Sale Details Configuration
EXPECTED_PRICE = "20000"
SUITABLE_BUSINESS_TYPES = "Hello Worlddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddd!"

# Amenities Configuration
DIRECTIONS_TIP = "Come straight from Top in Town and Take a left."

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
    """Fill the first page form - select city, Commercial option, Sale option, and submit.
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

        # Sale button (after clicking Commercial)
        try:
            sale_button = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//button[normalize-space()='Sale']"))
            )
            driver.execute_script("arguments[0].scrollIntoView({block:'center'});", sale_button)
            time.sleep(0.3)
            driver.execute_script("arguments[0].click();", sale_button)
            print("✓ Sale button clicked")
        except Exception as e:
            print("✗ Could not click Sale:", str(e))

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

def fill_property_details(driver, property_name):
    """Fill the property details page form."""
    print("Starting to fill property details page...")
    
    # Wait for page transition
    time.sleep(3)
    
    # Property Name - Direct approach
    try:
        all_inputs = driver.find_elements(By.XPATH, "//input[@name='title']")
        visible_inputs = [inp for inp in all_inputs if inp.is_displayed()]
        if visible_inputs:
            visible_inputs[0].clear()
            visible_inputs[0].send_keys(property_name)
            print("✓ Property Name filled:", property_name)
    except Exception as e:
        print("✗ Could not fill Property Name field:", str(e))

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

    # Dropdowns on this page - select first option for each visible combobox
    try:
        # Close stray popovers
        driver.execute_script("document.body.click();")
        time.sleep(0.3)
        
        # Collect visible combobox buttons on the page
        comboboxes = WebDriverWait(driver, 10).until(
            lambda d: [el for el in d.find_elements(By.XPATH, "//button[@role='combobox']") if el.is_displayed()]
        )
        
        # We expect 3 dropdowns: Space Type (already has default "Office"), Building Type, Furnishing Status
        # Filter out the Space Type that already has "Office" selected
        filtered_comboboxes = []
        for cb in comboboxes:
            cb_text = cb.text
            # Skip if it already has a value selected (like "Office")
            if cb_text != "Office" and "Select" not in cb_text:
                filtered_comboboxes.append(cb)
            elif "Select" in cb_text:
                filtered_comboboxes.append(cb)
        
        # We expect 2 dropdowns to fill: Building Type, Furnishing Status
        dropdown_names = ["Building Type", "Furnishing Status"]
        
        for idx, cb in enumerate(filtered_comboboxes[:2], start=1):
            try:
                driver.execute_script("arguments[0].scrollIntoView({block:'center'});", cb)
                time.sleep(0.2)
                driver.execute_script("arguments[0].click();", cb)
                first_option = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.XPATH, "//div[@role='option'][1]"))
                )
                driver.execute_script("arguments[0].click();", first_option)
                print(f"✓ Dropdown {idx} ({dropdown_names[idx-1]}) selected (first option)")
                time.sleep(0.2)
            except Exception as inner_e:
                print(f"⚠️  Dropdown {idx} ({dropdown_names[idx-1]}) selection failed:", str(inner_e))
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

def fill_locality_details_page(driver, city_name, locality_name):
    """Fill the locality details page - city and locality using autocomplete."""
    print("Starting to fill locality details page...")
    
    # Wait for page transition
    time.sleep(3)
    
    # City field - Type and select first suggestion
    try:
        city_input = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//input[@name='city']"))
        )
        city_input.clear()
        city_input.send_keys(city_name)
        print(f"✓ Typed city: {city_name}")
        time.sleep(2)  # Wait for autocomplete suggestions
        
        # Click first suggestion (Google Places autocomplete)
        try:
            first_suggestion = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, "//div[contains(@class, 'pac-item')][1]"))
            )
            driver.execute_script("arguments[0].click();", first_suggestion)
            print(f"✓ City selected: {city_name}")
        except:
            print("⚠️  Could not click city suggestion, but city typed")
    except Exception as e:
        print("✗ Could not fill city field:", str(e))
    
    time.sleep(1)
    
    # Locality field - Type and select first suggestion
    try:
        locality_input = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//input[@name='locality']"))
        )
        locality_input.clear()
        locality_input.send_keys(locality_name)
        print(f"✓ Typed locality: {locality_name}")
        time.sleep(2)  # Wait for autocomplete suggestions
        
        # Click first suggestion (Google Places autocomplete)
        try:
            first_suggestion = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, "//div[contains(@class, 'pac-item')][1]"))
            )
            driver.execute_script("arguments[0].click();", first_suggestion)
            print(f"✓ Locality selected: {locality_name}")
        except:
            print("⚠️  Could not click locality suggestion, but locality typed")
    except Exception as e:
        print("✗ Could not fill locality field:", str(e))
    
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

def fill_sale_details_page(driver):
    """Fill the sale details page - expected price, ownership type, and suitable business types."""
    print("Starting to fill sale details page...")
    
    # Wait for page transition
    time.sleep(3)
    
    # Expected Price
    try:
        price_input = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//input[@type='number' and contains(@placeholder, 'Amount')]"))
        )
        price_input.clear()
        price_input.send_keys(EXPECTED_PRICE)
        print("✓ Expected Price filled:", EXPECTED_PRICE)
    except Exception as e:
        print("✗ Could not fill Expected Price field:", str(e))
    
    # Ownership Type - Random selection
    try:
        ownership_combobox = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[@role='combobox' and contains(@id, 'form-item') and .//span[text()='Select']]"))
        )
        driver.execute_script("arguments[0].scrollIntoView({block:'center'});", ownership_combobox)
        time.sleep(0.2)
        driver.execute_script("arguments[0].click();", ownership_combobox)
        time.sleep(0.5)
        
        # Get all options
        options = driver.find_elements(By.XPATH, "//div[@role='option']")
        if options and len(options) >= 4:
            # Randomly select one of the 4 options (0, 1, 2, or 3)
            selected_index = random.randint(0, 3)
            selected_option = options[selected_index]
            ownership_type = selected_option.text
            driver.execute_script("arguments[0].click();", selected_option)
            print(f"✓ Ownership Type selected (random index {selected_index}): {ownership_type}")
        elif options:
            # If less than 4 options, randomly select from available
            selected_index = random.randint(0, len(options) - 1)
            selected_option = options[selected_index]
            ownership_type = selected_option.text
            driver.execute_script("arguments[0].click();", selected_option)
            print(f"✓ Ownership Type selected (random index {selected_index}): {ownership_type}")
        else:
            # Fallback: select first option if can't get all options
            first_option = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, "//div[@role='option'][1]"))
            )
            driver.execute_script("arguments[0].click();", first_option)
            print("✓ Ownership Type selected (first option as fallback)")
    except Exception as e:
        print("✗ Could not select Ownership Type:", str(e))
    
    time.sleep(0.5)
    
    # Suitable Business Types
    try:
        business_types_textarea = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//textarea[contains(@placeholder, 'Retail, Office, Restaurant')]"))
        )
        business_types_textarea.clear()
        business_types_textarea.send_keys(SUITABLE_BUSINESS_TYPES)
        print("✓ Suitable Business Types filled")
    except Exception as e:
        print("✗ Could not fill Suitable Business Types field:", str(e))
    
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

    def select_dropdown_option(driver, label_text, select_random=False):
        """Helper function to select an option from a dropdown."""
        try:
            # Find the combobox button by looking for all comboboxes, then check associated labels
            all_comboboxes = driver.find_elements(By.XPATH, "//button[@role='combobox']")
            target_combobox = None
            
            for cb in all_comboboxes:
                # Try to find the label associated with this combobox
                try:
                    # Check if there's a label nearby (could be before or after)
                    parent = cb.find_element(By.XPATH, "./ancestor::div[1]")
                    label = parent.find_elements(By.XPATH, ".//label")
                    if label:
                        if label[0].text.strip() == label_text or label_text in label[0].text.strip():
                            target_combobox = cb
                            break
                except:
                    continue
            
            if not target_combobox:
                # Fallback: try to find by aria-describedby or nearby text
                for cb in all_comboboxes:
                    try:
                        aria_desc = cb.get_attribute('aria-describedby')
                        if aria_desc:
                            desc_element = driver.find_element(By.ID, aria_desc)
                            if label_text in desc_element.text:
                                target_combobox = cb
                                break
                    except:
                        continue
            
            if target_combobox:
                driver.execute_script("arguments[0].scrollIntoView({block:'center'});", target_combobox)
                time.sleep(0.2)
                driver.execute_script("arguments[0].click();", target_combobox)
                time.sleep(0.5)
                
                # Get all options
                options = WebDriverWait(driver, 5).until(
                    EC.presence_of_all_elements_located((By.XPATH, "//div[@role='option']"))
                )
                
                if options:
                    if select_random and len(options) > 1:
                        selected_index = random.randint(0, len(options) - 1)
                        selected_option = options[selected_index]
                        option_text = selected_option.text
                        driver.execute_script("arguments[0].click();", selected_option)
                        print(f"✓ {label_text} selected (random index {selected_index}): {option_text}")
                    else:
                        # Select the first option
                        selected_option = options[0]
                        option_text = selected_option.text
                        driver.execute_script("arguments[0].click();", selected_option)
                        print(f"✓ {label_text} selected (first option): {option_text}")
                else:
                    print(f"✗ No options found for {label_text} dropdown.")
            else:
                print(f"✗ Could not find {label_text} dropdown.")
                
        except Exception as e:
            print(f"✗ Could not select {label_text}: {str(e)}")
            # Close any open dropdowns
            driver.execute_script("document.body.click();")
            time.sleep(0.2)

    # Dropdown Selections
    # Power Backup (Random)
    select_dropdown_option(driver, "Power Backup", select_random=True)
    time.sleep(0.5)
    
    # Lift (Random)
    select_dropdown_option(driver, "Lift", select_random=True)
    time.sleep(0.5)
    
    # Parking (First option)
    select_dropdown_option(driver, "Parking", select_random=False)
    time.sleep(0.5)
    
    # Washrooms (First option)
    select_dropdown_option(driver, "Washrooms", select_random=False)
    time.sleep(0.5)
    
    # Water Storage Facility (First option)
    select_dropdown_option(driver, "Water Storage Facility", select_random=False)
    time.sleep(0.5)
    
    # Security (Random)
    select_dropdown_option(driver, "Security", select_random=True)
    time.sleep(0.5)
    
    # Current Property Condition (First option)
    select_dropdown_option(driver, "Current Property Condition", select_random=False)
    time.sleep(0.5)
    
    # What business is currently running (First option)
    select_dropdown_option(driver, "What business is currently running", select_random=False)
    time.sleep(0.5)

    # Add directions for your buyers - Fill textarea
    try:
        directions_textarea = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//textarea[@name='directionsTip']"))
        )
        directions_textarea.clear()
        directions_textarea.send_keys(DIRECTIONS_TIP)
        print("✓ Directions for Buyers filled:", DIRECTIONS_TIP)
    except Exception as e:
        print("✗ Could not fill Directions for Buyers:", str(e))
    
    # Click Save & Continue button
    try:
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
        
        # Gallery categories for Commercial Sale (3 fields)
        gallery_categories = ["Front View", "Interior View", "Others"]
        
        # Upload image to each category
        for i, category in enumerate(gallery_categories):
            try:
                # Find the file input for this specific category using position-based selection
                # Each category card has a unique structure, so we'll use the nth-of-type approach
                file_inputs = driver.find_elements(By.XPATH, "//input[@type='file' and @accept='image/*']")
                
                if i < len(file_inputs):
                    file_input = file_inputs[i]
                    
                    # Scroll to the element to ensure it's visible
                    driver.execute_script("arguments[0].scrollIntoView(true);", file_input)
                    time.sleep(0.5)
                    
                    # Send the file path to the input element
                    file_input.send_keys(image_absolute_path)
                    time.sleep(1)
                    
                    print(f"✓ Uploaded image to {category}")
                else:
                    print(f"✗ Could not find file input for {category} (position {i})")
                    
            except Exception as e:
                print(f"✗ Could not upload image to {category}:", str(e))
    
    # Click Save & Continue button
    try:
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
    # Get city and locality for this property
    city_index = (property_index - 1) % len(CITIES_LOCALITIES)
    city_name, locality_name = CITIES_LOCALITIES[city_index]
    property_name = f"Commercial Property {property_index}"
    
    print(f"\n{'='*50}")
    print(f"COMMERCIAL SALE PROPERTY {property_index} - Starting posting flow")
    print(f"City: {city_name}, Locality: {locality_name}")
    print(f"{'='*50}")
    
    try:
        # Fill the first page form
        fill_first_page(driver)
        time.sleep(3)

        # Fill the property details page
        fill_property_details(driver, property_name)
        time.sleep(3)

        # Fill the locality details page
        fill_locality_details_page(driver, city_name, locality_name)
        time.sleep(3)

        # Fill the sale details page
        fill_sale_details_page(driver)
        time.sleep(3)

        # Fill the amenities page
        fill_amenities_page(driver)
        time.sleep(3)

        # Fill the gallery page
        fill_gallery_page(driver)
        time.sleep(3)

        # Fill the schedule page and submit
        fill_schedule_and_submit(driver)
        
        print(f"✓ Commercial Sale Property {property_index} submitted successfully!")
        return True
        
    except Exception as e:
        print(f"✗ Error posting Commercial Sale property {property_index}: {str(e)}")
        return False

def main():
    """Main entry point."""
    # Ask user for number of properties to post
    try:
        num_properties = int(input("How many Commercial Sale properties do you want to post? Enter a number: "))
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
                    print(f"✓ Commercial Sale Property {i} completed successfully!")
                else:
                    failed_posts += 1
                    print(f"✗ Commercial Sale Property {i} failed!")
                
                # If not the last property, start a new post
                if i < num_properties:
                    print(f"\nStarting Commercial Sale property {i+1}...")
                    start_new_post(driver)
                    time.sleep(2)
                    
            except Exception as e:
                print(f"✗ Error with Commercial Sale property {i}: {str(e)}")
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
        print(f"COMMERCIAL SALE POSTING COMPLETE!")
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
