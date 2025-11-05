"""
Script Name: homehni_industrial_land.py

Purpose:
    This script automates filling the Industrial Land property posting form on HomeHNI.
    It handles the initial contact details and property ad type selection for Industrial Land properties.

Usage:
    1. Install selenium: pip install selenium
    2. Download ChromeDriver and ensure it's in your PATH
    3. Run: python Industrial.py
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

# Plot Details Configuration
PLOT_AREA = "3000"
PLOT_LENGTH = "80"
PLOT_WIDTH = "50"

# Location Details Configuration - Rotation of city/locality pairs
CITIES_LOCALITIES = [
    ("Bangalore", "Bellandur"),
    ("Mumbai", "Thane"),
    ("Hyderabad", "mgroad")
]

# Sale Details Configuration
EXPECTED_PRICE = "20000"
APPROVED_BY = "Bengaluru Land Authority, Banashankari"
DESCRIPTION = "Hello Worlddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddd!"

# Infrastructure Configuration
ROAD_WIDTH = "200"
DIRECTIONS_FOR_BUYERS = "Come straight from top in town and take a left"

# Gallery Configuration
IMAGE_PATHS = ["try.png", "try2.png", "try3.png"]

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
    """Fill the first page form - select city, Land/Plot option, Industrial Land option, and submit.
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

        # Land/Plot button - try multiple approaches
        try:
            # Try finding button by text that contains "Land/Plot"
            land_plot_button = None
            selectors = [
                "//button[contains(text(), 'Land/Plot')]",
                "//button[@class='flex-1' and contains(., 'Land/Plot')]",
                "//button[contains(@class, 'flex-1') and contains(text(), 'Land/Plot')]",
                "//button[contains(@class, 'text-sm') and contains(., 'Land/Plot')]"
            ]
            
            for selector in selectors:
                try:
                    elements = driver.find_elements(By.XPATH, selector)
                    for element in elements:
                        if element.is_displayed():
                            land_plot_button = element
                            break
                    if land_plot_button:
                        break
                except:
                    continue
            
            if land_plot_button:
                driver.execute_script("arguments[0].scrollIntoView({block:'center'});", land_plot_button)
                time.sleep(0.3)
                driver.execute_script("arguments[0].click();", land_plot_button)
                print("✓ Land/Plot button clicked")
            else:
                print("✗ Could not find Land/Plot button")
        except Exception as e:
            print("✗ Could not click Land/Plot button:", str(e))

        # Wait for Industrial Land options to appear
        time.sleep(0.5)

        # Industrial Land button - try multiple approaches
        try:
            industrial_land_button = None
            selectors = [
                "//button[contains(text(), 'Industrial land')]",
                "//button[normalize-space()='Industrial land']",
                "//button[contains(text(), 'Industrial')]",
                "//button[contains(., 'Industrial land')]"
            ]
            
            for selector in selectors:
                try:
                    elements = driver.find_elements(By.XPATH, selector)
                    for element in elements:
                        if element.is_displayed():
                            industrial_land_button = element
                            break
                    if industrial_land_button:
                        break
                except:
                    continue
            
            if industrial_land_button:
                driver.execute_script("arguments[0].scrollIntoView({block:'center'});", industrial_land_button)
                time.sleep(0.3)
                driver.execute_script("arguments[0].click();", industrial_land_button)
                print("✓ Industrial Land button clicked")
            else:
                print("✗ Could not find Industrial Land button")
        except Exception as e:
            print("✗ Could not click Industrial Land button:", str(e))

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

def fill_plot_details_page(driver):
    """Fill the plot details page form - plot area, length, width, and gated property."""
    print("Starting to fill plot details page...")
    
    # Wait for page transition
    time.sleep(3)
    
    # Plot Area
    try:
        plot_area_input = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//input[@name='plotArea']"))
        )
        plot_area_input.clear()
        plot_area_input.send_keys(PLOT_AREA)
        print(f"✓ Plot Area filled: {PLOT_AREA}")
    except Exception as e:
        print("✗ Could not fill Plot Area field:", str(e))

    # Plot Length
    try:
        plot_length_input = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//input[@name='plotLength']"))
        )
        plot_length_input.clear()
        plot_length_input.send_keys(PLOT_LENGTH)
        print(f"✓ Plot Length filled: {PLOT_LENGTH}")
    except Exception as e:
        print("✗ Could not fill Plot Length field:", str(e))

    # Plot Width
    try:
        plot_width_input = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//input[@name='plotWidth']"))
        )
        plot_width_input.clear()
        plot_width_input.send_keys(PLOT_WIDTH)
        print(f"✓ Plot Width filled: {PLOT_WIDTH}")
    except Exception as e:
        print("✗ Could not fill Plot Width field:", str(e))

    # Gated Property? - Select Yes or No randomly
    try:
        gated_combobox = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[@role='combobox' and contains(., 'Select')]"))
        )
        driver.execute_script("arguments[0].scrollIntoView({block:'center'});", gated_combobox)
        time.sleep(0.2)
        driver.execute_script("arguments[0].click();", gated_combobox)
        time.sleep(0.5)
        
        # Get all options
        options = driver.find_elements(By.XPATH, "//div[@role='option']")
        if options and len(options) >= 2:
            # Randomly select either Yes (index 1) or No (index 0)
            selected_index = random.randint(0, 1)
            selected_option = options[selected_index]
            gated_value = selected_option.text
            driver.execute_script("arguments[0].click();", selected_option)
            print(f"✓ Gated Property? selected (random): {gated_value}")
        elif options:
            # If only one option available, select it
            selected_option = options[0]
            gated_value = selected_option.text
            driver.execute_script("arguments[0].click();", selected_option)
            print(f"✓ Gated Property? selected: {gated_value}")
        else:
            print("✗ No options found for Gated Property? dropdown")
    except Exception as e:
        print("✗ Could not select Gated Property?:", str(e))
    
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

def fill_location_details_page(driver, city_name, locality_name):
    """Fill the location details page - city and locality using autocomplete."""
    print("Starting to fill location details page...")
    
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
        time.sleep(1.5)  # Wait for autocomplete suggestions
        
        # Click first suggestion (Google Places autocomplete)
        try:
            first_suggestion = WebDriverWait(driver, 3).until(
                EC.element_to_be_clickable((By.XPATH, "//div[contains(@class, 'pac-item')][1]"))
            )
            driver.execute_script("arguments[0].click();", first_suggestion)
            print(f"✓ City selected: {city_name}")
        except:
            print("⚠️  Could not click city suggestion, but city typed")
    except Exception as e:
        print("✗ Could not fill city field:", str(e))
    
    # Locality field - Type and select first suggestion
    try:
        locality_input = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//input[@name='locality']"))
        )
        locality_input.clear()
        locality_input.send_keys(locality_name)
        print(f"✓ Typed locality: {locality_name}")
        time.sleep(1.5)  # Wait for autocomplete suggestions
        
        # Click first suggestion (Google Places autocomplete)
        try:
            first_suggestion = WebDriverWait(driver, 3).until(
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
    """Fill the sale details page - expected price, approved by authority, and description."""
    print("Starting to fill sale details page...")
    
    # Wait for page transition
    time.sleep(3)
    
    # Expected Price
    try:
        price_input = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//input[@id='expectedPrice']"))
        )
        price_input.clear()
        price_input.send_keys(EXPECTED_PRICE)
        print(f"✓ Expected Price filled: {EXPECTED_PRICE}")
    except Exception as e:
        print("✗ Could not fill Expected Price field:", str(e))
    
    # Which authority the property is posted by
    try:
        approved_by_input = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//input[@id='approvedBy']"))
        )
        approved_by_input.clear()
        approved_by_input.send_keys(APPROVED_BY)
        print(f"✓ Approved By filled: {APPROVED_BY}")
    except Exception as e:
        print("✗ Could not fill Approved By field:", str(e))
    
    # Description
    try:
        description_textarea = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//textarea[@id='description']"))
        )
        description_textarea.clear()
        description_textarea.send_keys(DESCRIPTION)
        print("✓ Description filled")
    except Exception as e:
        print("✗ Could not fill Description field:", str(e))
    
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

def fill_infrastructure_page(driver):
    """Fill the infrastructure page - water supply, electricity, sewage (random), road width, and directions."""
    print("Starting to fill infrastructure page...")
    
    # Wait for page transition
    time.sleep(3)
    
    # Helper function to select a random dropdown option
    def select_random_dropdown_option(combobox_xpath):
        """Click the combobox and select a random option."""
        try:
            combobox = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, combobox_xpath))
            )
            driver.execute_script("arguments[0].scrollIntoView({block:'center'});", combobox)
            time.sleep(0.2)
            driver.execute_script("arguments[0].click();", combobox)
            time.sleep(0.5)
            
            # Get all options
            options = driver.find_elements(By.XPATH, "//div[@role='option']")
            if options and len(options) >= 2:
                # Randomly select one of the options
                selected_index = random.randint(0, len(options) - 1)
                selected_option = options[selected_index]
                selected_value = selected_option.text
                driver.execute_script("arguments[0].click();", selected_option)
                print(f"✓ Selected: {selected_value}")
                return True
            elif options:
                # If only one option, select it
                driver.execute_script("arguments[0].click();", options[0])
                print(f"✓ Selected: {options[0].text}")
                return True
            else:
                print("✗ No options found in dropdown")
                return False
        except Exception as e:
            print(f"✗ Could not select dropdown option: {str(e)}")
            # Close dropdown if open
            driver.execute_script("document.body.click();")
            time.sleep(0.2)
            return False
    
    # Water Supply - Select random option
    print("Selecting Water Supply...")
    water_supply_xpath = "//button[@role='combobox' and contains(., 'water supply')]"
    select_random_dropdown_option(water_supply_xpath)
    time.sleep(0.5)
    
    # Electricity Connection - Select first option
    print("Selecting Electricity Connection...")
    try:
        # Find all visible comboboxes and select the second one (Electricity Connection)
        all_comboboxes = driver.find_elements(By.XPATH, "//button[@role='combobox']")
        visible_comboboxes = [cb for cb in all_comboboxes if cb.is_displayed()]
        
        if len(visible_comboboxes) >= 2:
            electricity_combobox = visible_comboboxes[1]  # Second combobox is Electricity
            driver.execute_script("arguments[0].scrollIntoView({block:'center'});", electricity_combobox)
            time.sleep(0.2)
            driver.execute_script("arguments[0].click();", electricity_combobox)
            time.sleep(0.5)
            
            # Select the first option
            first_option = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, "//div[@role='option'][1]"))
            )
            first_option_text = first_option.text
            driver.execute_script("arguments[0].click();", first_option)
            print(f"✓ Electricity Connection selected: {first_option_text}")
        else:
            print("✗ Could not find Electricity Connection combobox")
    except Exception as e:
        print("✗ Could not select Electricity Connection:", str(e))
    
    time.sleep(0.5)
    
    # Sewage Connection - Select random option
    print("Selecting Sewage Connection...")
    sewage_xpath = "//button[@role='combobox' and contains(., 'sewage')]"
    select_random_dropdown_option(sewage_xpath)
    time.sleep(0.5)
    
    # Width of Facing Road
    try:
        road_width_input = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//input[@id='roadWidth']"))
        )
        road_width_input.clear()
        road_width_input.send_keys(ROAD_WIDTH)
        print(f"✓ Road Width filled: {ROAD_WIDTH}")
    except Exception as e:
        print("✗ Could not fill Road Width field:", str(e))
    
    # Directions for buyers
    try:
        directions_textarea = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//textarea[@id='directionsToProperty']"))
        )
        directions_textarea.clear()
        directions_textarea.send_keys(DIRECTIONS_FOR_BUYERS)
        print("✓ Directions for buyers filled")
    except Exception as e:
        print("✗ Could not fill Directions for buyers field:", str(e))
    
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
    """Fill the gallery page by uploading images."""
    print("Starting to fill gallery page...")
    
    # Wait for page transition
    time.sleep(3)
    
    # Get absolute paths to the image files
    current_dir = os.path.dirname(os.path.abspath(__file__))
    image_paths = [os.path.join(current_dir, img_path) for img_path in IMAGE_PATHS]
    
    # Check which images exist
    existing_images = []
    for img_path in image_paths:
        if os.path.exists(img_path):
            existing_images.append(img_path)
            print(f"✓ Found image: {img_path}")
        else:
            print(f"⚠️  Image not found: {img_path}")
    
    if not existing_images:
        print("✗ No images found. Skipping gallery upload.")
        return
    
    # Upload all images at once
    try:
        # Find the file input element
        file_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//input[@type='file' and @accept='image/*']"))
        )
        
        # Convert relative paths to absolute paths
        # Selenium needs file paths separated by newlines for multiple files
        image_files = "\n".join(existing_images)
        
        # Send the file paths
        file_input.send_keys(image_files)
        print(f"✓ Uploaded {len(existing_images)} image(s)")
        
        # Wait a moment for uploads to process
        time.sleep(2)
        
    except Exception as e:
        print("✗ Could not upload images:", str(e))
    
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
    # Get city and locality for this property (rotating)
    city_index = (property_index - 1) % len(CITIES_LOCALITIES)
    city_name, locality_name = CITIES_LOCALITIES[city_index]
    
    print(f"\n{'='*50}")
    print(f"INDUSTRIAL LAND PROPERTY {property_index} - Starting posting flow")
    print(f"City: {city_name}, Locality: {locality_name}")
    print(f"{'='*50}")
    
    try:
        # Fill the first page form
        fill_first_page(driver)
        time.sleep(2)

        # Fill the plot details page
        fill_plot_details_page(driver)
        time.sleep(2)

        # Fill the location details page
        fill_location_details_page(driver, city_name, locality_name)
        time.sleep(2)

        # Fill the sale details page
        fill_sale_details_page(driver)
        time.sleep(2)

        # Fill the infrastructure page
        fill_infrastructure_page(driver)
        time.sleep(2)

        # Fill the gallery page
        fill_gallery_page(driver)
        time.sleep(2)

        # Fill the schedule page and submit
        fill_schedule_and_submit(driver)
        
        print(f"✓ Industrial Land Property {property_index} submitted successfully!")
        return True
        
    except Exception as e:
        print(f"✗ Error posting Industrial Land property {property_index}: {str(e)}")
        return False

def main():
    """Main entry point."""
    # Ask user for number of properties to post
    try:
        num_properties = int(input("How many Industrial Land properties do you want to post? Enter a number: "))
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
                    print(f"✓ Industrial Land Property {i} completed successfully!")
                else:
                    failed_posts += 1
                    print(f"✗ Industrial Land Property {i} failed!")
                
                # If not the last property, start a new post
                if i < num_properties:
                    print(f"\nStarting Industrial Land property {i+1}...")
                    start_new_post(driver)
                    time.sleep(2)
                    
            except Exception as e:
                print(f"✗ Error with Industrial Land property {i}: {str(e)}")
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
        print(f"INDUSTRIAL LAND POSTING COMPLETE!")
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

