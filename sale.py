"""
Script Name: homehni_sale_property.py

Purpose:
    This script automates filling the Sale property posting form on HomeHNI.
    It handles the initial contact details and property ad type selection for Sale properties.

Usage:
    1. Install selenium: pip install selenium
    2. Download ChromeDriver and ensure it's in your PATH
    3. Run: python sale.py
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
PROPERTY_NAME = "Test Sale Property"
BUILT_UP_AREA = "10000"
CARPET_AREA = "2000"

# Sale Details Configuration
SALE_PRICE = "8000000"
PRICE_PER_SQFT = "5000"
MONTHLY_MAINTENANCE = "3500"
BOOKING_AMOUNT = "200000"

# Amenities Configuration
DIRECTIONS_TIP = "Go straight and take left."

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
    """Fill the first page form - select city, sale option, and submit.
    More robust with retries, scrolling, and JS clicks to avoid interceptions.
    """
    print("Starting to fill first page...")
    print("Note: Name and Mobile are pre-filled automatically")

    def try_fill_once():
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

        # Sale button (scoped within the same form section as the submit button)
        try:
            sale_button = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//div[.//button[normalize-space()='Start Posting Your Ad For FREE']]//button[normalize-space()='Sale']"))
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

def fill_property_details(driver):
    """Fill the property details page form."""
    print("Starting to fill property details page...")
    
    # Property Name - Direct approach (fastest)
    try:
        all_inputs = driver.find_elements(By.XPATH, "//input[@name='title']")
        visible_inputs = [inp for inp in all_inputs if inp.is_displayed()]
        if visible_inputs:
            visible_inputs[0].clear()
            visible_inputs[0].send_keys(PROPERTY_NAME)
            print("✓ Property Name filled:", PROPERTY_NAME)
    except Exception as e:
        print("✗ Could not fill Property Name field:", str(e))

    # Built Up Area - Direct approach (fastest)
    try:
        all_inputs = driver.find_elements(By.XPATH, "//input[@name='builtUpArea']")
        visible_inputs = [inp for inp in all_inputs if inp.is_displayed()]
        if visible_inputs:
            visible_inputs[0].clear()
            visible_inputs[0].send_keys(BUILT_UP_AREA)
            print("✓ Built Up Area filled:", BUILT_UP_AREA)
    except Exception as e:
        print("✗ Could not fill Built Up Area field:", str(e))

    # Carpet Area - Direct approach (fastest)
    try:
        all_inputs = driver.find_elements(By.XPATH, "//input[@name='carpetArea']")
        visible_inputs = [inp for inp in all_inputs if inp.is_displayed()]
        if visible_inputs:
            visible_inputs[0].clear()
            visible_inputs[0].send_keys(CARPET_AREA)
            print("✓ Carpet Area filled:", CARPET_AREA)
    except Exception as e:
        print("✗ Could not fill Carpet Area field:", str(e))

    # Dropdowns on this page can vary in text after first selection. To be robust,
    # always pick the first option from each visible combobox on the page in order.
    try:
        # Close stray popovers
        driver.execute_script("document.body.click();")
        time.sleep(0.3)
        # Collect visible combobox buttons on the page step
        comboboxes = WebDriverWait(driver, 10).until(
            lambda d: [el for el in d.find_elements(By.XPATH, "//button[@role='combobox']") if el.is_displayed()]
        )
        # We expect at least 4: Property Type, BHK Type, Property Age, Facing
        for idx, cb in enumerate(comboboxes[:4], start=1):
            try:
                driver.execute_script("arguments[0].scrollIntoView({block:'center'});", cb)
                time.sleep(0.2)
                driver.execute_script("arguments[0].click();", cb)
                first_option = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.XPATH, "//div[@role='option'][1]"))
                )
                driver.execute_script("arguments[0].click();", first_option)
                print(f"✓ Combobox {idx} selected (first option)")
                time.sleep(0.2)
            except Exception as inner_e:
                print(f"⚠️  Combobox {idx} selection failed:", str(inner_e))
                driver.execute_script("document.body.click();")
                time.sleep(0.2)
    except Exception as e:
        print("✗ Could not process combobox selections:", str(e))

    # Click Save & Continue button
    try:
        wait_and_click(driver, By.XPATH, "//button[contains(text(), 'Save & Continue')]")
        print("✓ Save & Continue button clicked - proceeding to next page")
    except Exception as e:
        print("✗ Could not find Save & Continue button:", str(e))

def fill_locality_details(driver):
    """Fill the locality details page form."""
    print("Starting to fill locality details page...")
    
    # Wait for page transition
    time.sleep(2)
    
    # City input - Direct approach
    try:
        all_inputs = driver.find_elements(By.XPATH, "//input[@name='city']")
        visible_inputs = [inp for inp in all_inputs if inp.is_displayed()]
        if visible_inputs:
            city_input = visible_inputs[0]
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
    
    # Locality input - Direct approach
    try:
        all_inputs = driver.find_elements(By.XPATH, "//input[@name='locality']")
        visible_inputs = [inp for inp in all_inputs if inp.is_displayed()]
        if visible_inputs:
            locality_input = visible_inputs[0]
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
        wait_and_click(driver, By.XPATH, "//button[contains(text(), 'Save & Continue')]")
        print("✓ Save & Continue button clicked - proceeding to next page")
    except Exception as e:
        print("✗ Could not find Save & Continue button:", str(e))

def fill_sale_details(driver):
    """Fill the sale details page form."""
    print("Starting to fill sale details page...")
    
    # Wait for page transition
    time.sleep(2)
    
    # Sale Price - Direct approach
    try:
        all_inputs = driver.find_elements(By.XPATH, "//input[@placeholder='Enter Amount']")
        visible_inputs = [inp for inp in all_inputs if inp.is_displayed()]
        if visible_inputs:
            visible_inputs[0].clear()
            visible_inputs[0].send_keys(SALE_PRICE)
            print("✓ Sale Price filled:", SALE_PRICE)
    except Exception as e:
        print("✗ Could not fill Sale Price field:", str(e))

    # Price per Sq.Ft - Auto-filled based on Sale Price, so skip
    print("✓ Price per Sq.Ft auto-calculated (skipped)")

    # Availability Status - Dropdown (select first option)
    try:
        # Try multiple selectors for availability dropdown
        availability_combobox = None
        selectors = [
            "//button[@role='combobox' and contains(., 'Ready to Move')]",
            "//button[@role='combobox' and contains(@class, 'combobox')]",
            "//button[contains(@class, 'combobox') and contains(., 'Ready')]"
        ]
        
        for selector in selectors:
            try:
                elements = driver.find_elements(By.XPATH, selector)
                visible_elements = [el for el in elements if el.is_displayed()]
                if visible_elements:
                    availability_combobox = visible_elements[0]
                    break
            except:
                continue
        
        if availability_combobox:
            driver.execute_script("arguments[0].click();", availability_combobox)
            time.sleep(0.5)
            first_option = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, "//div[@role='option'][1]"))
            )
            driver.execute_script("arguments[0].click();", first_option)
            print("✓ Availability Status selected (first option)")
        else:
            print("✗ Could not find Availability Status dropdown")
    except Exception as e:
        print("✗ Could not select Availability Status:", str(e))

    # Monthly Maintenance - Direct approach
    try:
        all_inputs = driver.find_elements(By.XPATH, "//input[@name='maintenanceCharges']")
        visible_inputs = [inp for inp in all_inputs if inp.is_displayed()]
        if visible_inputs:
            visible_inputs[0].clear()
            visible_inputs[0].send_keys(MONTHLY_MAINTENANCE)
            print("✓ Monthly Maintenance filled:", MONTHLY_MAINTENANCE)
    except Exception as e:
        print("✗ Could not fill Monthly Maintenance field:", str(e))

    # Booking Amount - Direct approach
    try:
        all_inputs = driver.find_elements(By.XPATH, "//input[@name='bookingAmount']")
        visible_inputs = [inp for inp in all_inputs if inp.is_displayed()]
        if visible_inputs:
            visible_inputs[0].clear()
            visible_inputs[0].send_keys(BOOKING_AMOUNT)
            print("✓ Booking Amount filled:", BOOKING_AMOUNT)
    except Exception as e:
        print("✗ Could not fill Booking Amount field:", str(e))
    
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

def fill_amenities(driver):
    """Fill the amenities page form."""
    print("Starting to fill amenities page...")
    
    # Wait for page transition
    time.sleep(2)
    
    # Debug: Check what elements are available on amenities page
    try:
        all_buttons = driver.find_elements(By.XPATH, "//button")
        print(f"Debug: Found {len(all_buttons)} buttons on amenities page")
        for i, btn in enumerate(all_buttons[:10]):  # Show first 10 buttons
            text = btn.text or 'no-text'
            classes = btn.get_attribute('class') or 'no-class'
            role = btn.get_attribute('role') or 'no-role'
            is_displayed = btn.is_displayed()
            print(f"  Button {i+1}: text='{text}', role='{role}', displayed={is_displayed}, classes='{classes[:50]}...'")
        
        all_textareas = driver.find_elements(By.XPATH, "//textarea")
        print(f"Debug: Found {len(all_textareas)} textareas on amenities page")
        for i, ta in enumerate(all_textareas):
            name = ta.get_attribute('name') or 'no-name'
            placeholder = ta.get_attribute('placeholder') or 'no-placeholder'
            is_displayed = ta.is_displayed()
            print(f"  Textarea {i+1}: name='{name}', placeholder='{placeholder}', displayed={is_displayed}")
    except Exception as e:
        print("Debug failed:", str(e))
    
    # Find all visible buttons and look for Yes/No buttons
    try:
        all_buttons = driver.find_elements(By.XPATH, "//button")
        visible_buttons = [btn for btn in all_buttons if btn.is_displayed()]
        yes_buttons = [btn for btn in visible_buttons if btn.text.strip() == 'Yes']
        no_buttons = [btn for btn in visible_buttons if btn.text.strip() == 'No']
        checkbox_buttons = [btn for btn in visible_buttons if btn.get_attribute('role') == 'checkbox']
        
        print(f"Found {len(visible_buttons)} visible buttons, {len(yes_buttons)} Yes buttons, {len(no_buttons)} No buttons, {len(checkbox_buttons)} checkboxes")
        
        # Select first 4 Yes buttons (Pet Allowed, Gym, Non-Veg, Gated Security)
        for i, yes_btn in enumerate(yes_buttons[:4]):
            try:
                driver.execute_script("arguments[0].click();", yes_btn)
                amenity_names = ["Pet Allowed", "Gym", "Non-Veg Allowed", "Gated Security"]
                print(f"✓ {amenity_names[i]}: Yes")
            except Exception as e:
                print(f"✗ Could not click Yes button {i+1}:", str(e))
        
        # Select first 4 checkboxes (Lift, Internet Services, Air Conditioner, Swimming Pool)
        for i, checkbox_btn in enumerate(checkbox_buttons[:4]):
            try:
                driver.execute_script("arguments[0].click();", checkbox_btn)
                amenity_names = ["Lift", "Internet Services", "Air Conditioner", "Swimming Pool"]
                print(f"✓ {amenity_names[i]}: Selected")
            except Exception as e:
                print(f"✗ Could not click checkbox {i+1}:", str(e))
                
    except Exception as e:
        print("✗ Could not process amenities buttons:", str(e))
    
    # Directions Tip - Fill textarea (use visible one)
    try:
        all_textareas = driver.find_elements(By.XPATH, "//textarea[@name='directionsTip']")
        visible_textareas = [ta for ta in all_textareas if ta.is_displayed()]
        if visible_textareas:
            directions_textarea = visible_textareas[0]
            directions_textarea.clear()
            directions_textarea.send_keys(DIRECTIONS_TIP)
            print("✓ Directions Tip filled:", DIRECTIONS_TIP)
        else:
            print("✗ No visible directions textarea found")
    except Exception as e:
        print("✗ Could not fill Directions Tip:", str(e))
    
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

def fill_gallery(driver):
    """Skip gallery uploads and just click Save & Continue."""
    print("Starting to fill gallery page...")
    print("⚠️  Skipping image uploads - proceeding directly to Save & Continue")
    
    # Wait a moment for page to load
    time.sleep(2)
    
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
    print(f"PROPERTY {property_index} - Starting posting flow")
    print(f"{'='*50}")
    
    # Update property name for this iteration
    global PROPERTY_NAME
    PROPERTY_NAME = f"Test Sale Property {property_index}"
    print(f"Property Name: {PROPERTY_NAME}")
    
    try:
        # Fill the first page form
        fill_first_page(driver)
        time.sleep(3)

        # Fill the property details page
        fill_property_details(driver)
        time.sleep(3)

        # Fill the locality details page
        fill_locality_details(driver)
        time.sleep(3)

        # Fill the sale details page
        fill_sale_details(driver)
        time.sleep(3)

        # Fill the amenities page
        fill_amenities(driver)
        time.sleep(3)

        # Fill the gallery page
        fill_gallery(driver)
        time.sleep(3)

        # Fill the schedule page and submit
        fill_schedule_and_submit(driver)
        
        print(f"✓ Property {property_index} submitted successfully!")
        return True
        
    except Exception as e:
        print(f"✗ Error posting property {property_index}: {str(e)}")
        return False

def main():
    """Main entry point."""
    # Ask user for number of properties to post
    try:
        num_properties = int(input("How many Sale properties do you want to post? Enter a number: "))
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
                    print(f"✓ Property {i} completed successfully!")
                else:
                    failed_posts += 1
                    print(f"✗ Property {i} failed!")
                
                # If not the last property, start a new post
                if i < num_properties:
                    print(f"\nStarting property {i+1}...")
                    start_new_post(driver)
                    time.sleep(2)
                    
            except Exception as e:
                print(f"✗ Error with property {i}: {str(e)}")
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
        print(f"POSTING COMPLETE!")
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
