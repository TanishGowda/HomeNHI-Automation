"""
Script Name: homehni_pg_property.py

Purpose:
    This script automates filling the PG/Hostel property posting form on HomeHNI.
    It handles the initial contact details and property ad type selection for PG/Hostel properties.

Usage:
    1. Install selenium: pip install selenium
    2. Download ChromeDriver and ensure it's in your PATH
    3. Run: python pg.py
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

# Room Details Configuration
EXPECTED_RENT = "12000"
EXPECTED_DEPOSIT = "20000"

# PG Details Configuration
DESCRIPTION = "Student Friendly PG, with all the essential amenities and an affordable rent, combined with the best cuisines, from all parts of the world."

# Amenities Configuration
DIRECTIONS_TIP = "Come straight, from Top in Town supermarket, and take a left, when you see a bike repair shop."

# Gallery Configuration
IMAGE_PATH = "try.png"  # Path to the image file to upload
VIDEO_PATH = "trial.MP4"  # Path to the video file to upload

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
    """Fill the first page form - select city, PG/Hostel option, and submit.
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

        # PG/Hostel button (scoped within the same form section as the submit button)
        try:
            pg_button = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//div[.//button[normalize-space()='Start Posting Your Ad For FREE']]//button[normalize-space()='PG/Hostel']"))
            )
            driver.execute_script("arguments[0].scrollIntoView({block:'center'});", pg_button)
            time.sleep(0.3)
            driver.execute_script("arguments[0].click();", pg_button)
            print("✓ PG/Hostel button clicked")
        except Exception as e:
            print("✗ Could not click PG/Hostel:", str(e))

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

def fill_room_type_page(driver):
    """Fill the room type page - select Single room type and submit."""
    print("Starting to fill room type page...")
    
    # Wait for page transition
    time.sleep(3)
    
    # Select Single room type
    try:
        single_room = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//div[contains(@class, 'border-2') and contains(@class, 'cursor-pointer') and contains(., 'Single')]"))
        )
        driver.execute_script("arguments[0].scrollIntoView({block:'center'});", single_room)
        time.sleep(0.5)
        driver.execute_script("arguments[0].click();", single_room)
        print("✓ Single room type selected")
    except Exception as e:
        print("✗ Could not select Single room type:", str(e))
    
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

def fill_room_details_page(driver):
    """Fill the room details page - rent, deposit, and amenities."""
    print("Starting to fill room details page...")
    
    # Wait for page transition
    time.sleep(3)
    
    # Expected Rent per person
    try:
        rent_input = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//input[@id='single-rent']"))
        )
        rent_input.clear()
        rent_input.send_keys(EXPECTED_RENT)
        print(f"✓ Expected Rent per person filled: {EXPECTED_RENT}")
    except Exception as e:
        print("✗ Could not fill Expected Rent field:", str(e))
    
    # Expected Deposit per Person
    try:
        deposit_input = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//input[@id='single-deposit']"))
        )
        deposit_input.clear()
        deposit_input.send_keys(EXPECTED_DEPOSIT)
        print(f"✓ Expected Deposit per person filled: {EXPECTED_DEPOSIT}")
    except Exception as e:
        print("✗ Could not fill Expected Deposit field:", str(e))
    
    # Room Amenities - Select Cupboard
    try:
        cupboard_checkbox = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[@id='cupboard']"))
        )
        driver.execute_script("arguments[0].click();", cupboard_checkbox)
        print("✓ Cupboard amenity selected")
    except Exception as e:
        print("✗ Could not select Cupboard amenity:", str(e))
    
    # Room Amenities - Select AC
    try:
        ac_checkbox = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[@id='ac']"))
        )
        driver.execute_script("arguments[0].click();", ac_checkbox)
        print("✓ AC amenity selected")
    except Exception as e:
        print("✗ Could not select AC amenity:", str(e))
    
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

def fill_pg_details_page(driver):
    """Fill the PG details page - rules and description."""
    print("Starting to fill PG details page...")
    
    # Wait for page transition
    time.sleep(3)
    
    # No Smoking checkbox
    try:
        no_smoking_checkbox = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[@id='noSmoking']"))
        )
        driver.execute_script("arguments[0].click();", no_smoking_checkbox)
        print("✓ No Smoking rule selected")
    except Exception as e:
        print("✗ Could not select No Smoking rule:", str(e))
    
    # No Drinking checkbox
    try:
        no_drinking_checkbox = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[@id='noDrinking']"))
        )
        driver.execute_script("arguments[0].click();", no_drinking_checkbox)
        print("✓ No Drinking rule selected")
    except Exception as e:
        print("✗ Could not select No Drinking rule:", str(e))
    
    # Description textarea
    try:
        description_textarea = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//textarea[@id='description']"))
        )
        description_textarea.clear()
        description_textarea.send_keys(DESCRIPTION)
        print(f"✓ Description filled: {DESCRIPTION[:50]}...")
    except Exception as e:
        print("✗ Could not fill Description field:", str(e))
    
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
    """Fill the amenities page - dropdowns, checkboxes, and directions."""
    print("Starting to fill amenities page...")
    
    # Wait for page transition
    time.sleep(3)
    
    # Handle all dropdowns - select first option for each
    try:
        # Close any stray popovers
        driver.execute_script("document.body.click();")
        time.sleep(0.3)
        
        # Find all visible combobox buttons on the page
        comboboxes = WebDriverWait(driver, 10).until(
            lambda d: [el for el in d.find_elements(By.XPATH, "//button[@role='combobox']") if el.is_displayed()]
        )
        
        # We expect 3 dropdowns: Laundry, Room Cleaning, Warden Facility
        dropdown_names = ["Laundry", "Room Cleaning", "Warden Facility"]
        
        for idx, cb in enumerate(comboboxes[:3]):
            try:
                driver.execute_script("arguments[0].scrollIntoView({block:'center'});", cb)
                time.sleep(0.2)
                driver.execute_script("arguments[0].click();", cb)
                
                # Wait for dropdown options to appear and select first option
                first_option = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.XPATH, "//div[@role='option'][1]"))
                )
                driver.execute_script("arguments[0].click();", first_option)
                print(f"✓ {dropdown_names[idx]} selected (first option)")
                time.sleep(0.2)
            except Exception as inner_e:
                print(f"⚠️  {dropdown_names[idx]} selection failed:", str(inner_e))
                driver.execute_script("document.body.click();")
                time.sleep(0.2)
    except Exception as e:
        print("✗ Could not process dropdown selections:", str(e))
    
    # Directions for clients textarea
    try:
        directions_textarea = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//textarea[contains(@placeholder, 'Take the road opposite')]"))
        )
        directions_textarea.clear()
        directions_textarea.send_keys(DIRECTIONS_TIP)
        print(f"✓ Directions filled: {DIRECTIONS_TIP[:50]}...")
    except Exception as e:
        print("✗ Could not fill Directions field:", str(e))
    
    # Select checkboxes: Mess, Cooking Allowed, Wifi
    checkbox_ids = ["mess", "cookingAllowed", "wifi"]
    checkbox_names = ["Mess", "Cooking Allowed", "Wifi"]
    
    for i, checkbox_id in enumerate(checkbox_ids):
        try:
            checkbox = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, f"//button[@id='{checkbox_id}']"))
            )
            driver.execute_script("arguments[0].click();", checkbox)
            print(f"✓ {checkbox_names[i]} selected")
        except Exception as e:
            print(f"✗ Could not select {checkbox_names[i]}:", str(e))
    
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
    """Skip gallery uploads and just click Save & Continue."""
    print("Starting to fill gallery page...")
    print("⚠️  Skipping image and video uploads - proceeding directly to Save & Continue")
    
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
    print(f"PG/HOSTEL PROPERTY {property_index} - Starting posting flow")
    print(f"{'='*50}")
    
    try:
        # Fill the first page form
        fill_first_page(driver)
        time.sleep(3)

        # Fill the room type page
        fill_room_type_page(driver)
        time.sleep(3)

        # Fill the room details page
        fill_room_details_page(driver)
        time.sleep(3)

        # Fill the locality details page
        fill_locality_details_page(driver)
        time.sleep(3)

        # Fill the PG details page
        fill_pg_details_page(driver)
        time.sleep(3)

        # Fill the amenities page
        fill_amenities_page(driver)
        time.sleep(3)

        # Fill the gallery page
        fill_gallery_page(driver)
        time.sleep(3)

        # Fill the schedule page and submit
        fill_schedule_and_submit(driver)
        
        print(f"✓ PG/Hostel Property {property_index} submitted successfully!")
        return True
        
    except Exception as e:
        print(f"✗ Error posting PG/Hostel property {property_index}: {str(e)}")
        return False

def main():
    """Main entry point."""
    # Ask user for number of properties to post
    try:
        num_properties = int(input("How many PG/Hostel properties do you want to post? Enter a number: "))
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
                    print(f"✓ PG/Hostel Property {i} completed successfully!")
                else:
                    failed_posts += 1
                    print(f"✗ PG/Hostel Property {i} failed!")
                
                # If not the last property, start a new post
                if i < num_properties:
                    print(f"\nStarting PG/Hostel property {i+1}...")
                    start_new_post(driver)
                    time.sleep(2)
                    
            except Exception as e:
                print(f"✗ Error with PG/Hostel property {i}: {str(e)}")
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
        print(f"PG/HOSTEL POSTING COMPLETE!")
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
