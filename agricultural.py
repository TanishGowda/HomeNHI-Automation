"""
Script Name: homehni_agricultural_land.py

Purpose:
    This script automates filling the Agricultural Land property posting form on HomeHNI.
    It handles the initial contact details and property ad type selection for Agricultural Land properties.

Usage:
    1. Install selenium: pip install selenium
    2. Download ChromeDriver and ensure it's in your PATH
    3. Run: python agricultural.py
    4. Manually log in and click "Post Property" 
    5. Press Enter in terminal to start automation
"""

import time
import os
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Configuration
PRIMARY_NAME = "Tanish"
PRIMARY_MOBILE = "9902978675"

# Plot Details Configuration
PLOT_AREA = "2000"
PLOT_LENGTH = "80"
PLOT_WIDTH = "100"

# Location Details Rotation
CITIES_LOCALITIES = [
    ("Bangalore", "Bellandur"),
    ("Mumbai", "Thane"),
    ("Hyderabad", "mgroad"),
]

# Sale Details Configuration
EXPECTED_PRICE = "8000000"
APPROVED_BY = "Karnataka Student Software Testing"
DESCRIPTION = "Hello Worlddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddd!"

# Infrastructure Configuration
ROAD_WIDTH = "100"
DIRECTIONS_FOR_BUYERS = "Come Straight from top in Town and take a left."

def wait_and_click(driver, by, locator, timeout=20):
    """Wait for an element to be clickable and then click it."""
    element = WebDriverWait(driver, timeout).until(EC.element_to_be_clickable((by, locator)))
    try:
        element.click()
    except:
        # If regular click fails, try JavaScript click
        driver.execute_script("arguments[0].click();", element)

def login_and_wait(driver):
    """
    Navigate to HomeHNI homepage and pause for manual login and navigation.
    Once you are logged in and have clicked on 'Post Property' to reach the
    first page form, press Enter in your terminal to continue.
    """
    driver.get("https://homehni.in")
    input("Please complete the login process, click on 'Post Property', and when you reach the first page form, press Enter here to continue...")

def fill_first_page(driver):
    """Fill the first page form - select city, Land/Plot option, Agricultural Land option, and submit.
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

        # Wait for Agricultural Land options to appear
        time.sleep(0.5)

        # Agricultural Land button - try multiple approaches
        try:
            agricultural_land_button = None
            selectors = [
                "//button[contains(text(), 'Agricultural land')]",
                "//button[normalize-space()='Agricultural land']",
                "//button[contains(text(), 'Agricultural')]",
                "//button[contains(., 'Agricultural land')]"
            ]
            
            for selector in selectors:
                try:
                    elements = driver.find_elements(By.XPATH, selector)
                    for element in elements:
                        if element.is_displayed():
                            agricultural_land_button = element
                            break
                    if agricultural_land_button:
                        break
                except:
                    continue
            
            if agricultural_land_button:
                driver.execute_script("arguments[0].scrollIntoView({block:'center'});", agricultural_land_button)
                time.sleep(0.3)
                driver.execute_script("arguments[0].click();", agricultural_land_button)
                print("✓ Agricultural Land button clicked")
            else:
                print("✗ Could not find Agricultural Land button")
        except Exception as e:
            print("✗ Could not click Agricultural Land button:", str(e))

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

    # Is the Land/Plot inside a gated project? - Select Yes or No randomly
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

def fill_location_details_page(driver, city_name: str, locality_name: str):
    """Fill the location details page - city and locality using autocomplete."""
    print("Starting to fill location details page...")
    
    # City field - Type and select first suggestion
    try:
        city_input = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//input[@name='city']"))
        )
        city_input.clear()
        city_input.send_keys(city_name)
        print(f"✓ Typed city: {city_name}")
        time.sleep(1.5)
        first_suggestion = WebDriverWait(driver, 3).until(
            EC.element_to_be_clickable((By.XPATH, "//div[contains(@class, 'pac-item')][1]"))
        )
        driver.execute_script("arguments[0].click();", first_suggestion)
        print(f"✓ City selected: {city_name}")
    except Exception as e:
        print("✗ Could not select City:", str(e))

    # Locality field - Type and select first suggestion
    try:
        locality_input = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//input[@name='locality']"))
        )
        locality_input.clear()
        locality_input.send_keys(locality_name)
        print(f"✓ Typed locality: {locality_name}")
        time.sleep(1.5)
        first_suggestion = WebDriverWait(driver, 3).until(
            EC.element_to_be_clickable((By.XPATH, "//div[contains(@class, 'pac-item')][1]"))
        )
        driver.execute_script("arguments[0].click();", first_suggestion)
        print(f"✓ Locality selected: {locality_name}")
    except Exception as e:
        print("✗ Could not select Locality:", str(e))

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
        print("✗ Could not click Save & Continue:", str(e))

def main():
    """Main entry point."""
    # Ask user for number of properties to post
    try:
        num_properties = int(input("How many Agricultural Land properties do you want to post? Enter a number: "))
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

        for i in range(1, num_properties + 1):
            # Determine rotating city/locality
            ci = (i - 1) % len(CITIES_LOCALITIES)
            city_name, locality_name = CITIES_LOCALITIES[ci]

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
            try:
                # Expected Price
                price_input = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//input[@id='expectedPrice']"))
                )
                price_input.clear()
                price_input.send_keys(EXPECTED_PRICE)
                print(f"✓ Expected Price filled: {EXPECTED_PRICE}")
            except Exception as e:
                print("✗ Could not fill Expected Price field:", str(e))

            try:
                # Approved By
                approved_by_input = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//input[@id='approvedBy']"))
                )
                approved_by_input.clear()
                approved_by_input.send_keys(APPROVED_BY)
                print(f"✓ Approved By filled: {APPROVED_BY}")
            except Exception as e:
                print("✗ Could not fill Approved By field:", str(e))

            try:
                # Description
                description_textarea = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//textarea[@id='description']"))
                )
                description_textarea.clear()
                description_textarea.send_keys(DESCRIPTION)
                print("✓ Description filled")
            except Exception as e:
                print("✗ Could not fill Description field:", str(e))

            # Click Save & Continue
            try:
                buttons = driver.find_elements(By.XPATH, "//button[contains(text(), 'Save & Continue')]|//button[contains(text(), 'Save &amp; Continue')]")
                visible = [b for b in buttons if b.is_displayed()]
                if visible:
                    driver.execute_script("arguments[0].click();", visible[0])
                    print("✓ Save & Continue button clicked - proceeding to next page")
                else:
                    print("✗ Could not find Save & Continue button on sale details page")
            except Exception as e:
                print("✗ Could not click Save & Continue on sale details page:", str(e))
            
            time.sleep(2)

            # Infrastructure page
            print("Starting to fill infrastructure page...")

            # Water Supply - Random selection
            try:
                water_cb = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[@role='combobox' and contains(., 'water supply')]"))
                )
                driver.execute_script("arguments[0].click();", water_cb)
                time.sleep(0.5)
                options = driver.find_elements(By.XPATH, "//div[@role='option']")
                if options:
                    idx = random.randint(0, len(options) - 1)
                    choice = options[idx]
                    choice_text = choice.text
                    driver.execute_script("arguments[0].click();", choice)
                    print(f"✓ Water Supply selected: {choice_text}")
                else:
                    print("✗ No Water Supply options found")
            except Exception as e:
                print("✗ Water Supply selection failed:", str(e))

            # Electricity Connection - First option
            try:
                all_cb = driver.find_elements(By.XPATH, "//button[@role='combobox']")
                visible_cb = [c for c in all_cb if c.is_displayed()]
                if len(visible_cb) >= 2:
                    elec_cb = visible_cb[1]
                    driver.execute_script("arguments[0].scrollIntoView({block:'center'});", elec_cb)
                    time.sleep(0.2)
                    driver.execute_script("arguments[0].click();", elec_cb)
                    time.sleep(0.5)
                    first_option = WebDriverWait(driver, 5).until(
                        EC.element_to_be_clickable((By.XPATH, "//div[@role='option'][1]"))
                    )
                    first_text = first_option.text
                    driver.execute_script("arguments[0].click();", first_option)
                    print(f"✓ Electricity Connection selected: {first_text}")
                else:
                    print("✗ Electricity Connection combobox not found")
            except Exception as e:
                print("✗ Electricity selection failed:", str(e))

            # Width of Facing Road
            try:
                road_width_input = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//input[@id='roadWidth']"))
                )
                road_width_input.clear()
                road_width_input.send_keys(ROAD_WIDTH)
                print(f"✓ Road Width filled: {ROAD_WIDTH}")
            except Exception as e:
                print("✗ Could not fill Road Width:", str(e))

            # Directions for buyers
            try:
                directions_textarea = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//textarea[@id='directionsToProperty']"))
                )
                directions_textarea.clear()
                directions_textarea.send_keys(DIRECTIONS_FOR_BUYERS)
                print("✓ Directions for buyers filled")
            except Exception as e:
                print("✗ Could not fill Directions for buyers:", str(e))

            # Save & Continue
            try:
                buttons = driver.find_elements(By.XPATH, "//button[contains(text(), 'Save & Continue')]|//button[contains(text(), 'Save &amp; Continue')]")
                visible = [b for b in buttons if b.is_displayed()]
                if visible:
                    driver.execute_script("arguments[0].click();", visible[0])
                    print("✓ Save & Continue button clicked - proceeding to next page")
                else:
                    print("✗ Could not find Save & Continue button on infrastructure page")
            except Exception as e:
                print("✗ Could not click Save & Continue on infrastructure page:", str(e))

            time.sleep(2)

            # Gallery page
            print("Starting to fill gallery page...")
            try:
                # Prepare absolute image paths
                current_dir = os.path.dirname(os.path.abspath(__file__))
                images = [
                    os.path.join(current_dir, "try.png"),
                    os.path.join(current_dir, "try2.png"),
                    os.path.join(current_dir, "try3.png"),
                ]
                existing = [p for p in images if os.path.exists(p)]
                for p in images:
                    if os.path.exists(p):
                        print(f"✓ Found image: {p}")
                    else:
                        print(f"⚠️  Image not found: {p}")

                if existing:
                    file_input = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.XPATH, "//input[@type='file' and @accept='image/*']"))
                    )
                    file_input.send_keys("\n".join(existing))
                    print(f"✓ Uploaded {len(existing)} image(s)")
                    time.sleep(2)
                else:
                    print("✗ No images found to upload")
            except Exception as e:
                print("✗ Could not upload images:", str(e))

            # Save & Continue on gallery
            try:
                buttons = driver.find_elements(By.XPATH, "//button[contains(text(), 'Save & Continue')]|//button[contains(text(), 'Save &amp; Continue')]")
                visible = [b for b in buttons if b.is_displayed()]
                if visible:
                    driver.execute_script("arguments[0].click();", visible[0])
                    print("✓ Save & Continue button clicked - proceeding to next page")
                else:
                    print("✗ Could not find Save & Continue button on gallery page")
            except Exception as e:
                print("✗ Could not click Save & Continue on gallery page:", str(e))

            time.sleep(2)

            # Schedule -> Submit
            try:
                submit_button = WebDriverWait(driver, 12).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Submit Property')]"))
                )
                driver.execute_script("arguments[0].scrollIntoView({block:'center'});", submit_button)
                time.sleep(0.5)
                driver.execute_script("arguments[0].click();", submit_button)
                print(f"✓ Submitted Agricultural Land property {i}")
                time.sleep(2)
            except Exception as e:
                print("✗ Could not submit property:", str(e))

            # If more to post, go back to post-property for next item
            if i < num_properties:
                try:
                    driver.get("https://homehni.in/post-property")
                    WebDriverWait(driver, 15).until(
                        EC.presence_of_element_located((By.XPATH, "//button[@role='combobox' and contains(., 'Select city')] | //button[contains(., 'Start Posting Your Ad For FREE')]"))
                    )
                    print("✓ Ready for next property: https://homehni.in/post-property")
                    time.sleep(1)
                except Exception as e:
                    print("✗ Could not open post-property page:", str(e))

        print(f"\n{'='*60}")
        print("AGRICULTURAL LAND POSTING COMPLETE!")
        print(f"{'='*60}")
        print(f"Total properties posted: {num_properties}")
        print(f"{'='*60}")

        input("Press Enter to close the browser...")

    except Exception as e:
        print(f"An error occurred: {str(e)}")
    finally:
        driver.quit()

if __name__ == "__main__":
    main()

