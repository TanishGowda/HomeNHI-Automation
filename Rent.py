"""
Script Name: homehni_first_page.py

Purpose:
    This script automates filling the first page of the HomeHNI property posting form.
    It handles the initial contact details and property ad type selection.

Usage:
    1. Install selenium: pip install selenium
    2. Download ChromeDriver and ensure it's in your PATH
    3. Run: python b.py
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

# Configuration
PRIMARY_NAME = "Tanish"
PRIMARY_MOBILE = "9902978675"
CITY_OPTION = "Abohar"

# Property Details Configuration
PROPERTY_NAME = "Test Property"
BUILT_UP_AREA = "10000"
PROPERTY_TYPE = "Apartment"
BHK_TYPE = "2 BHK"
PROPERTY_AGE = "0-1 Years"
FACING = "North"

# Locality Details Configuration (defaults; flow now uses rotating list below)
CITY_NAME = "Bangalore"
LOCALITY_NAME = "Bellandur"
# Rotation of city/locality pairs for each property index
CITY_LOCALITY_ROTATION = [
    ("Bangalore", "Bellandur"),
    ("Mumbai", "Thane"),
    ("Hyderabad", "mgroad"),
]

# Rental Details Configuration
EXPECTED_RENT = "40000"
EXPECTED_DEPOSIT = "70000"
MONTHLY_MAINTENANCE = "Included in Rent"
AVAILABLE_FROM_DATE = ""  # Will be set to today's date
PREFERRED_TENANTS = "Anyone"
FURNISHING = "Fully Furnished"
PARKING = "Car Parking"

# Amenities Configuration
BATHROOMS_COUNT = 2
BALCONIES_COUNT = 2
WATER_SUPPLY = "First Option"  # Will select first option
PETS_ALLOWED = "Yes"
GYM = "Yes"
NON_VEG_ALLOWED = "Yes"
GATED_SECURITY = "Yes"
WHO_SHOW_PROPERTY = "First Option"  # Will select first option
PROPERTY_CONDITION = "First Option"  # Will select first option
DIRECTIONS_TIP = "Take a right near Superstore and come straight."
SELECTED_AMENITIES = ["Lift", "Club House", "Swimming Pool", "Internet Services"]

# Gallery Configuration
IMAGE_PATH = "try.png"  # Path to the image file to upload
GALLERY_CATEGORIES = ["Bathroom", "Bedroom", "Hall", "Kitchen", "Front View", "Balcony"]
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

def select_dropdown_by_visible_text(driver, by, locator, text, timeout=20):
    """Wait for a dropdown element and select by visible text."""
    element = WebDriverWait(driver, timeout).until(
        EC.element_to_be_clickable((by, locator))
    )
    select = Select(element)
    select.select_by_visible_text(text)

def debug_dropdown_options(driver, dropdown_name):
    """Debug function to print available dropdown options."""
    try:
        print(f"Debug: Looking for options in {dropdown_name} dropdown...")
        # Wait a moment for dropdown to fully load
        time.sleep(2)
        
        # Try to find all possible option elements
        option_selectors = [
            "//div[@role='option']",
            "//li[@role='option']", 
            "//div[contains(@class, 'option')]",
            "//li[contains(@class, 'option')]",
            "//div[contains(@class, 'item')]",
            "//li[contains(@class, 'item')]"
        ]
        
        for selector in option_selectors:
            try:
                options = driver.find_elements(By.XPATH, selector)
                if options:
                    print(f"Found {len(options)} options with selector: {selector}")
                    for i, option in enumerate(options[:5]):  # Show first 5 options
                        print(f"  Option {i+1}: '{option.text}'")
                    break
            except:
                continue
                
    except Exception as e:
        print(f"Debug failed for {dropdown_name}: {str(e)}")

def login_and_wait(driver):
    """
    Navigate to HomeHNI homepage and pause for manual login and navigation.
    Once you are logged in and have clicked on 'Post Property' to reach the
    first page form, press Enter in your terminal to continue.
    """
    driver.get("https://homehni.in")
    input("Please complete the login process, click on 'Post Property', and when you reach the first page form, press Enter here to continue...")

def fill_first_page(driver):
    """Fill the first page form - select city, rent option, and submit.
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

        # Rent button (scoped within the same form section as the submit button)
        try:
            rent_button = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//div[.//button[normalize-space()='Start Posting Your Ad For FREE']]//button[normalize-space()='Rent']"))
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

def fill_property_details(driver, property_name: str):
    """Fill the property details page form."""
    print("Starting to fill property details page...")
    
    # Property Name
    try:
        wait_and_send_keys(driver, By.XPATH, "//input[@placeholder='Enter Property Name']", property_name)
        print("✓ Property Name filled:", property_name)
    except Exception as e:
        print("✗ Could not find Property Name field:", str(e))

    # Built Up Area - number input field
    try:
        wait_and_send_keys(driver, By.XPATH, "//input[@type='number' and @name='superBuiltUpArea']", BUILT_UP_AREA)
        print("✓ Built Up Area filled:", BUILT_UP_AREA)
    except Exception as e:
        print("✗ Could not find Built Up Area field:", str(e))

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

def fill_locality_details(driver, property_index: int):
    """Fill the locality details page form with rotating city/locality."""
    print("Starting to fill locality details page...")
    # Determine pair by rotation
    pair = CITY_LOCALITY_ROTATION[(property_index - 1) % len(CITY_LOCALITY_ROTATION)]
    city_to_use, locality_to_use = pair
    
    # City field - Google Places autocomplete
    try:
        city_input = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//input[@name='city' and contains(@placeholder, 'Search')]"))
        )
        city_input.clear()
        city_input.send_keys(city_to_use)
        time.sleep(2)  # Wait for suggestions to appear
        
        # Click the first suggestion
        try:
            first_suggestion = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, "//div[contains(@class, 'pac-item')][1]"))
            )
            driver.execute_script("arguments[0].click();", first_suggestion)
            print("✓ City selected:", city_to_use)
        except:
            print("⚠️  City suggestion not found, but text entered:", city_to_use)
    except Exception as e:
        print("✗ Could not find City field:", str(e))

    # Locality/Area field - Google Places autocomplete
    try:
        locality_input = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//input[@name='locality' and contains(@placeholder, 'Search')]"))
        )
        locality_input.clear()
        locality_input.send_keys(locality_to_use)
        time.sleep(2)  # Wait for suggestions to appear
        
        # Click the first suggestion
        try:
            first_suggestion = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, "//div[contains(@class, 'pac-item')][1]"))
            )
            driver.execute_script("arguments[0].click();", first_suggestion)
            print("✓ Locality selected:", locality_to_use)
        except:
            print("⚠️  Locality suggestion not found, but text entered:", locality_to_use)
    except Exception as e:
        print("✗ Could not find Locality field:", str(e))

    # Landmark field - leave empty as it's optional
    print("✓ Landmark field skipped (optional)")

    # Click Save & Continue button
    try:
        wait_and_click(driver, By.XPATH, "//button[contains(text(), 'Save & Continue')]")
        print("✓ Save & Continue button clicked - proceeding to next page")
    except Exception as e:
        print("✗ Could not find Save & Continue button:", str(e))

def fill_rental_details(driver):
    """Fill the rental details page form."""
    print("Starting to fill rental details page...")
    
    # Expected Rent
    try:
        rent_input = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//input[@type='number' and contains(@placeholder, 'Enter Amount') and contains(@class, 'pl-8')]"))
        )
        rent_input.clear()
        rent_input.send_keys(EXPECTED_RENT)
        print("✓ Expected Rent filled:", EXPECTED_RENT)
    except Exception as e:
        print("✗ Could not find Expected Rent field:", str(e))

    # Expected Deposit
    try:
        deposit_input = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//input[@type='number' and contains(@placeholder, 'Enter Amount') and contains(@class, 'pl-8') and not(contains(@class, 'pr-20'))]"))
        )
        deposit_input.clear()
        deposit_input.send_keys(EXPECTED_DEPOSIT)
        print("✓ Expected Deposit filled:", EXPECTED_DEPOSIT)
    except Exception as e:
        print("✗ Could not find Expected Deposit field:", str(e))

    # Monthly Maintenance dropdown - select first option
    try:
        maintenance_combobox = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//button[@role='combobox' and contains(., 'Select')]"))
        )
        driver.execute_script("arguments[0].click();", maintenance_combobox)
        time.sleep(1)
        
        first_option = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, "//div[@role='option'][1]"))
        )
        driver.execute_script("arguments[0].click();", first_option)
        print("✓ Monthly Maintenance selected (first option)")
    except Exception as e:
        print("✗ Could not find Monthly Maintenance dropdown:", str(e))

    # Available From date picker - select first available date
    try:
        # Find the date picker button using the specific structure
        date_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//button[@type='button' and contains(@class, 'inline-flex') and contains(., 'dd/mm/yyyy')]"))
        )
        driver.execute_script("arguments[0].click();", date_button)
        time.sleep(2)  # Wait for calendar to appear
        
        # Select the first available date
        try:
            first_date = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'day')][1]"))
            )
            driver.execute_script("arguments[0].click();", first_date)
            print("✓ Available From date selected (first available)")
        except:
            # Try alternative selector for date buttons
            try:
                first_date = WebDriverWait(driver, 3).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), '1') or contains(text(), '2') or contains(text(), '3')][1]"))
                )
                driver.execute_script("arguments[0].click();", first_date)
                print("✓ Available From date selected (first available)")
            except:
                print("⚠️  Could not select specific date, but date picker opened")
    except Exception as e:
        print("✗ Could not find Available From date picker:", str(e))

    # Preferred Tenants checkbox
    try:
        tenant_checkbox = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, f"//button[@role='checkbox' and @id='{PREFERRED_TENANTS}']"))
        )
        driver.execute_script("arguments[0].click();", tenant_checkbox)
        print("✓ Preferred Tenants selected:", PREFERRED_TENANTS)
    except Exception as e:
        print("✗ Could not find Preferred Tenants checkbox:", str(e))

    # Furnishing dropdown - select first option
    try:
        furnishing_combobox = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//button[@role='combobox' and contains(., 'Select')]"))
        )
        driver.execute_script("arguments[0].click();", furnishing_combobox)
        time.sleep(1)
        
        first_option = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, "//div[@role='option'][1]"))
        )
        driver.execute_script("arguments[0].click();", first_option)
        print("✓ Furnishing selected (first option)")
    except Exception as e:
        print("✗ Could not find Furnishing dropdown:", str(e))

    # Parking dropdown - select first option
    try:
        parking_combobox = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//button[@role='combobox' and contains(., 'Select')]"))
        )
        driver.execute_script("arguments[0].click();", parking_combobox)
        time.sleep(1)
        
        first_option = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, "//div[@role='option'][1]"))
        )
        driver.execute_script("arguments[0].click();", first_option)
        print("✓ Parking selected (first option)")
    except Exception as e:
        print("✗ Could not find Parking dropdown:", str(e))

    # Click Save & Continue button
    try:
        wait_and_click(driver, By.XPATH, "//button[contains(text(), 'Save & Continue')]")
        print("✓ Save & Continue button clicked - proceeding to next page")
    except Exception as e:
        print("✗ Could not find Save & Continue button:", str(e))

def fill_amenities(driver):
    """Fill the amenities page form."""
    print("Starting to fill amenities page...")
    
    # Bathrooms and Balconies - find all plus buttons and click them in order
    try:
        # Find all plus buttons on the page
        plus_buttons = driver.find_elements(By.XPATH, "//button[.//svg[contains(@class, 'lucide-plus')]]")
        
        if len(plus_buttons) >= 2:
            # Click first plus button twice (Bathrooms)
            for i in range(BATHROOMS_COUNT):
                driver.execute_script("arguments[0].click();", plus_buttons[0])
                time.sleep(0.5)
            print(f"✓ Bathrooms set to {BATHROOMS_COUNT}")
            
            # Click second plus button twice (Balconies)
            for i in range(BALCONIES_COUNT):
                driver.execute_script("arguments[0].click();", plus_buttons[1])
                time.sleep(0.5)
            print(f"✓ Balconies set to {BALCONIES_COUNT}")
        else:
            print("⚠️  Could not find enough plus buttons for bathrooms/balconies")
    except Exception as e:
        print("✗ Could not find plus buttons:", str(e))

    # Water Supply dropdown - select first option
    try:
        water_supply_combobox = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//button[@role='combobox' and contains(., 'Select')]"))
        )
        driver.execute_script("arguments[0].click();", water_supply_combobox)
        time.sleep(1)
        
        first_option = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, "//div[@role='option'][1]"))
        )
        driver.execute_script("arguments[0].click();", first_option)
        print("✓ Water Supply selected (first option)")
    except Exception as e:
        print("✗ Could not find Water Supply dropdown:", str(e))

    # Pet Allowed - select Yes
    try:
        pet_yes_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Yes') and contains(@class, 'border')]"))
        )
        driver.execute_script("arguments[0].click();", pet_yes_button)
        print("✓ Pet Allowed selected: Yes")
    except Exception as e:
        print("✗ Could not find Pet Allowed Yes button:", str(e))

    # Gym - select Yes
    try:
        gym_yes_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Yes') and contains(@class, 'border')]"))
        )
        driver.execute_script("arguments[0].click();", gym_yes_button)
        print("✓ Gym selected: Yes")
    except Exception as e:
        print("✗ Could not find Gym Yes button:", str(e))

    # Non-Veg Allowed - select Yes
    try:
        non_veg_yes_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Yes') and contains(@class, 'border')]"))
        )
        driver.execute_script("arguments[0].click();", non_veg_yes_button)
        print("✓ Non-Veg Allowed selected: Yes")
    except Exception as e:
        print("✗ Could not find Non-Veg Allowed Yes button:", str(e))

    # Gated Security - select Yes
    try:
        security_yes_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Yes') and contains(@class, 'border')]"))
        )
        driver.execute_script("arguments[0].click();", security_yes_button)
        print("✓ Gated Security selected: Yes")
    except Exception as e:
        print("✗ Could not find Gated Security Yes button:", str(e))

    # Who will show the property dropdown - select first option
    try:
        show_property_combobox = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//button[@role='combobox' and contains(., 'Select')]"))
        )
        driver.execute_script("arguments[0].click();", show_property_combobox)
        time.sleep(1)
        
        first_option = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, "//div[@role='option'][1]"))
        )
        driver.execute_script("arguments[0].click();", first_option)
        print("✓ Who will show property selected (first option)")
    except Exception as e:
        print("✗ Could not find Who will show property dropdown:", str(e))

    # Current Property Condition dropdown - select first option
    try:
        condition_combobox = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//button[@role='combobox' and contains(., 'Select')]"))
        )
        driver.execute_script("arguments[0].click();", condition_combobox)
        time.sleep(1)
        
        first_option = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, "//div[@role='option'][1]"))
        )
        driver.execute_script("arguments[0].click();", first_option)
        print("✓ Property Condition selected (first option)")
    except Exception as e:
        print("✗ Could not find Property Condition dropdown:", str(e))

    # Directions tip textarea
    try:
        directions_textarea = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//textarea[@name='directionsTip']"))
        )
        directions_textarea.clear()
        directions_textarea.send_keys(DIRECTIONS_TIP)
        print("✓ Directions tip filled:", DIRECTIONS_TIP)
    except Exception as e:
        print("✗ Could not find Directions tip textarea:", str(e))

    # Select available amenities checkboxes
    for amenity in SELECTED_AMENITIES:
        try:
            amenity_checkbox = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, f"//button[@role='checkbox' and following-sibling::label[contains(text(), '{amenity}')]]"))
            )
            driver.execute_script("arguments[0].click();", amenity_checkbox)
            print(f"✓ {amenity} selected")
        except Exception as e:
            print(f"✗ Could not find {amenity} checkbox:", str(e))

    # Click Save & Continue button
    try:
        wait_and_click(driver, By.XPATH, "//button[contains(text(), 'Save & Continue')]")
        print("✓ Save & Continue button clicked - proceeding to next page")
    except Exception as e:
        print("✗ Could not find Save & Continue button:", str(e))

def fill_gallery(driver):
    """Fill the gallery page by uploading images to all categories."""
    print("Starting to fill gallery page...")
    
    # Get absolute path to the image file
    current_dir = os.path.dirname(os.path.abspath(__file__))
    image_absolute_path = os.path.join(current_dir, IMAGE_PATH)
    
    # Check if image exists
    if not os.path.exists(image_absolute_path):
        print(f"✗ Image file not found: {image_absolute_path}")
        print("⚠️  Skipping gallery upload")
        return
    
    print(f"✓ Found image file: {image_absolute_path}")
    
    # Upload image to each category
    for i, category in enumerate(GALLERY_CATEGORIES):
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
        time.sleep(2)  # Wait a bit for uploads to process
        wait_and_click(driver, By.XPATH, "//button[contains(text(), 'Save & Continue')]")
        print("✓ Save & Continue button clicked - proceeding to next page")
    except Exception as e:
        print("✗ Could not find Save & Continue button:", str(e))
    
    # Upload property video if section is present
    try:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        video_abs = os.path.join(current_dir, VIDEO_PATH)
        if not os.path.exists(video_abs):
            print(f"⚠️  Video file not found: {video_abs} — skipping video upload")
        else:
            # Find a video input near the Upload Property Video section
            # Many UIs use a hidden <input type="file" accept="video/*">
            video_input = None
            # Try contextual search using heading text
            try:
                video_input = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, "//span[normalize-space()='Upload Property Video']/ancestor::div[contains(@class,'rounded')]|//div[.//span[normalize-space()='Upload Property Video']]//input[@type='file' and contains(@accept,'video')]"))
                )
            except:
                pass
            if video_input is None:
                # Fallback: any video file input on page
                inputs = driver.find_elements(By.XPATH, "//input[@type='file' and contains(@accept,'video')]")
                if inputs:
                    video_input = inputs[0]
            if video_input:
                driver.execute_script("arguments[0].scrollIntoView(true);", video_input)
                time.sleep(0.5)
                video_input.send_keys(video_abs)
                print("✓ Uploaded property video")
                time.sleep(1.5)
            else:
                print("⚠️  Could not locate video upload input — skipping")
    except Exception as e:
        print("✗ Video upload failed:", str(e))

def fill_schedule_and_submit(driver):
    """On Schedule page, click Submit Property, then open post-property to start next."""
    print("Starting to submit property on Schedule page...")
    try:
        submit_btn = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Submit Property']"))
        )
        driver.execute_script("arguments[0].click();", submit_btn)
        print("✓ Submit Property clicked")
    except Exception as e:
        print("✗ Could not click Submit Property:", str(e))
        return

    # Directly navigate to new post page for next property
    try:
        driver.get("https://homehni.in/post-property")
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//button[@role='combobox' and contains(., 'Select city')] | //button[normalize-space()='Start Posting Your Ad For FREE']"))
        )
        print("✓ Ready for next property (post-property page loaded)")
    except Exception as e:
        print("✗ Could not open post-property for next property:", str(e))

def start_new_post(driver):
    """From the dashboard, navigate directly to the post property page."""
    try:
        WebDriverWait(driver, 10).until(EC.url_contains("/dashboard"))
    except:
        pass
    try:
        driver.get("https://homehni.in/post-property")
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//button[contains(text(), 'Start Posting Your Ad For FREE')] | //button[@role='combobox' and contains(., 'Select city')]"))
        )
        print("✓ Navigated to post-property page")
    except Exception as e:
        print("✗ Could not navigate to post-property page:", str(e))

def run_full_post_flow(driver, property_index: int):
    """Run the entire flow to post a single property."""
    # First page
    fill_first_page(driver)
    time.sleep(2)
    # Property details
    property_name = f"Test Property {property_index}"
    fill_property_details(driver, property_name)
    time.sleep(2)
    # Locality (rotating city/locality per property)
    fill_locality_details(driver, property_index)
    time.sleep(2)
    # Rental
    fill_rental_details(driver)
    time.sleep(2)
    # Amenities
    fill_amenities(driver)
    time.sleep(2)
    # Gallery
    fill_gallery(driver)
    time.sleep(2)
    # Schedule -> Submit
    fill_schedule_and_submit(driver)

def main():
    """Main entry point."""
    driver = webdriver.Chrome()
    driver.maximize_window()
    try:
        login_and_wait(driver)
        
        # Ask how many properties to post
        while True:
            try:
                count_str = input("How many properties should be posted? Enter a number: ").strip()
                num_properties = int(count_str)
                if num_properties <= 0:
                    print("Please enter a positive number.")
                    continue
                break
            except ValueError:
                print("Invalid number. Try again.")
        
        for i in range(1, num_properties + 1):
            print(f"— Posting property {i} of {num_properties} —")
            run_full_post_flow(driver, i)
            
            if i < num_properties:
                # Back on dashboard, start a new post
                start_new_post(driver)
                # Wait for first page to load
                time.sleep(2)
        
        print("All properties posted.")
        input("Press Enter to close the browser...")
    except Exception as e:
        print(f"An error occurred: {str(e)}")
    finally:
        driver.quit()

if __name__ == "__main__":
    main()



