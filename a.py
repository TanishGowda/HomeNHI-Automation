"""
Script Name: homehni_stress_test.py

Purpose:
    This script demonstrates how you could automate the process of posting a property
    on the HomeHNI platform multiple times using Selenium WebDriver.  It is
    intended for stress‑testing and repetitive data entry.  The script uses a
    consistent set of values for each form field across all iterations.  You can
    modify the constant values at the top of the script to suit your own test
    scenario.

Usage:
    1. Install the necessary dependencies:
       pip install selenium

    2. Download the appropriate WebDriver for your browser (e.g., ChromeDriver for
       Google Chrome) and ensure it is in your PATH or provide the executable
       location when initializing the driver.

    3. Run the script.  You will be prompted to log in manually during the first
       iteration.  After you’ve logged in successfully and you are on the
       post‑property page, press Enter in the terminal to allow the script to
       proceed with automated postings.

    4. The script loops through the property posting workflow the number of
       times specified by the ITERATIONS constant.  At the end of each
       submission it clicks the "Go to Dashboard" button and then starts a new
       listing.

Note:
    - Because HomeHNI’s UI can change over time, you may need to adjust the
      locators used below.  Inspect the page’s HTML using your browser’s dev
      tools to find reliable IDs, names or XPaths.  The script uses explicit
      waits to ensure elements are interactable before operating on them.
    - This script does not handle CAPTCHA or other forms of bot mitigation.
    - Do not run this against a site unless you have permission to perform
      automated stress testing.
"""

import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC

# -----------------------------------------------------------------------------
# Configuration
# -----------------------------------------------------------------------------

ITERATIONS = 100  # number of properties to submit

# Values to use for each form field.  Modify these to suit your test case.
PRIMARY_NAME = "Tanish"
PRIMARY_MOBILE = "9902978675"
CITY_OPTION = "Abohar"  # the city selected on the first page

# Property details
PROPERTY_TITLE = "Stress Test Property"
BUILT_UP_AREA = "850"
PROPERTY_TYPE = "Apartment"      # options: Apartment, Villa, Penthouse, etc.
BHK_TYPE = "2 BHK"
PROPERTY_AGE = "Ready to Move"    # options: Under Construction, 0-1 Years, Ready to Move, etc.
FACING_DIRECTION = "North-East"

# Locality details
LOCALITY_CITY = "Delhi Division"
LOCALITY_AREA = "Rohini, Delhi"

# Rental details
EXPECTED_RENT = "18000"
EXPECTED_DEPOSIT = "36000"
RENT_NEGOTIABLE = True
MAINTENANCE_SCHEME = "Included in Rent"  # or "Extra"
MAINTENANCE_AMOUNT = "1500"  # only used if MAINTENANCE_SCHEME == "Extra"
AVAILABLE_FROM_DATE = "21/10/2025"  # dd/mm/yyyy
PREFERRED_TENANT = "Company"  # choose one: Anyone, Family, Bachelor Female, Bachelor Male, Company
FURNISHING = "Unfurnished"     # or Semi Furnished, Fully Furnished
PARKING = "Car + Bike Parking"  # options: Car Parking, Bike Parking, Car + Bike Parking, No Parking

# Amenities – set these to True to enable
AMENITIES = {
    "Pet Allowed": True,
    "Non-Veg Allowed": True,
    "Gym": True,
    "Gated Security": True,
    "Lift": True,
    "Air Conditioner": True,
    "Swimming Pool": True,
    "Park": True,
}

# -----------------------------------------------------------------------------
# Helper functions
# -----------------------------------------------------------------------------

def wait_and_click(driver: webdriver, by: By, locator: str, timeout: int = 20):
    """Wait for an element to be clickable and then click it."""
    WebDriverWait(driver, timeout).until(EC.element_to_be_clickable((by, locator))).click()

def wait_and_send_keys(driver: webdriver, by: By, locator: str, text: str, timeout: int = 20):
    """Wait for an input element and send keys to it."""
    element = WebDriverWait(driver, timeout).until(
        EC.visibility_of_element_located((by, locator))
    )
    element.clear()
    element.send_keys(text)

def select_dropdown_by_visible_text(element, text: str):
    """Select a dropdown option by visible text."""
    select = Select(element)
    select.select_by_visible_text(text)

def login_and_wait(driver: webdriver):
    """
    Navigate to HomeHNI homepage and pause for manual login and navigation.
    Once you are logged in and have clicked on 'Post Property' to reach the
    first page form, press Enter in your terminal to continue.
    """
    driver.get("https://homehni.in")
    input("Please complete the login process, click on 'Post Property', and when you reach the first page form, press Enter here to continue...")

def fill_first_page(driver: webdriver):
    """Fill the initial page (name, mobile, city, and property type)."""
    print("Starting to fill first page...")
    
    # Name field - try multiple possible selectors
    try:
        wait_and_send_keys(driver, By.XPATH, "//input[contains(@placeholder, 'Name')]", PRIMARY_NAME)
        print("✓ Name field filled")
    except:
        try:
            wait_and_send_keys(driver, By.XPATH, "//input[@type='text' and contains(@placeholder, 'Name')]", PRIMARY_NAME)
            print("✓ Name field filled (alternative selector)")
        except:
            print("✗ Could not find Name field")

    # Mobile number field - try multiple possible selectors
    try:
        wait_and_send_keys(driver, By.XPATH, "//input[contains(@placeholder, 'Mobile')]", PRIMARY_MOBILE)
        print("✓ Mobile field filled")
    except:
        try:
            wait_and_send_keys(driver, By.XPATH, "//input[@type='tel']", PRIMARY_MOBILE)
            print("✓ Mobile field filled (alternative selector)")
        except:
            print("✗ Could not find Mobile field")

    # City dropdown - try multiple approaches
    try:
        wait_and_click(driver, By.XPATH, "//input[contains(@placeholder, 'City')]")
        time.sleep(1)  # Wait for dropdown to appear
        wait_and_click(driver, By.XPATH, f"//li[contains(text(), '{CITY_OPTION}')]")
        print("✓ City selected")
    except:
        try:
            wait_and_click(driver, By.XPATH, "//div[contains(@class, 'city') or contains(@class, 'dropdown')]")
            time.sleep(1)
            wait_and_click(driver, By.XPATH, f"//li[contains(text(), '{CITY_OPTION}')]")
            print("✓ City selected (alternative selector)")
        except:
            print("✗ Could not find City dropdown")

    # Choose property ad type (Rent) - try multiple approaches
    try:
        wait_and_click(driver, By.XPATH, "//button[contains(text(), 'Rent')]")
        print("✓ Rent button clicked")
    except:
        try:
            wait_and_click(driver, By.XPATH, "//label[contains(text(), 'Rent')]")
            print("✓ Rent option selected (alternative selector)")
        except:
            print("✗ Could not find Rent button")

    # Click the submit button - try multiple approaches
    try:
        wait_and_click(driver, By.XPATH, "//button[contains(text(), 'Start Posting Your Ad For FREE')]")
        print("✓ Submit button clicked")
    except:
        try:
            wait_and_click(driver, By.XPATH, "//button[contains(text(), 'Start Posting')]")
            print("✓ Submit button clicked (alternative selector)")
        except:
            print("✗ Could not find Submit button")

def fill_property_details(driver: webdriver):
    """Fill out the property details page."""
    wait_and_send_keys(driver, By.XPATH, "//input[contains(@placeholder, 'Property Name') or contains(@name, 'propertyName')]", PROPERTY_TITLE)
    wait_and_send_keys(driver, By.XPATH, "//input[contains(@placeholder, 'Built Up Area') or contains(@name, 'builtUpArea')]", BUILT_UP_AREA)
    # Property type dropdown
    select_dropdown_by_visible_text(
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//select[contains(@name, 'propertyType')]"))),
        PROPERTY_TYPE,
    )
    # BHK type
    select_dropdown_by_visible_text(
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//select[contains(@name, 'bhkType')]"))),
        BHK_TYPE,
    )
    # Property age
    select_dropdown_by_visible_text(
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//select[contains(@name, 'propertyAge')]"))),
        PROPERTY_AGE,
    )
    # Facing direction
    select_dropdown_by_visible_text(
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//select[contains(@name, 'facing')]"))),
        FACING_DIRECTION,
    )
    # Save and continue
    wait_and_click(driver, By.XPATH, "//button[contains(., 'Save') and contains(., 'Continue')]")

def fill_location_details(driver: webdriver):
    """Fill the locality/city page."""
    # City (Google Places auto-suggest) – type city name and select first match
    city_input = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, "//input[contains(@placeholder, 'Search') and contains(@aria-label, 'City') or contains(@name, 'city')]"))
    )
    city_input.clear()
    city_input.send_keys(LOCALITY_CITY)
    # wait for suggestion and click
    WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, f"//div[contains(@class, 'pac-item') and contains(., '{LOCALITY_CITY.split()[0]}')]"))
    ).click()

    # Locality/area
    locality_input = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, "//input[contains(@placeholder, 'Locality') or contains(@aria-label, 'Locality') or contains(@name, 'locality')]"))
    )
    locality_input.clear()
    locality_input.send_keys(LOCALITY_AREA)
    WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, f"//div[contains(@class, 'pac-item') and contains(., '{LOCALITY_AREA.split(',')[0]}')]"))
    ).click()

    # Save and continue
    wait_and_click(driver, By.XPATH, "//button[contains(., 'Save') and contains(., 'Continue')]")

def fill_rental_details(driver: webdriver):
    """Fill in expected rent, deposit, maintenance, etc."""
    wait_and_send_keys(driver, By.XPATH, "//input[contains(@placeholder, 'Enter Amount')][1]", EXPECTED_RENT)
    wait_and_send_keys(driver, By.XPATH, "(//input[contains(@placeholder, 'Enter Amount')])[2]", EXPECTED_DEPOSIT)

    # Rent negotiable checkbox
    if RENT_NEGOTIABLE:
        wait_and_click(driver, By.XPATH, "//label[contains(., 'Rent Negotiable')]/preceding-sibling::input")

    # Maintenance drop‑down
    maintenance_select = Select(
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//select[contains(@name, 'maintenance')]")))
    )
    maintenance_select.select_by_visible_text(MAINTENANCE_SCHEME)
    if MAINTENANCE_SCHEME.lower().startswith("extra"):
        # fill maintenance amount field
        wait_and_send_keys(driver, By.XPATH, "//input[contains(@placeholder, 'Maintenance Amount')]", MAINTENANCE_AMOUNT)

    # Available from date – click the input and type the date
    date_input = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, "//input[contains(@placeholder, 'dd/mm/yyyy') or contains(@type, 'date')]"))
    )
    date_input.click()
    date_input.clear()
    date_input.send_keys(AVAILABLE_FROM_DATE)

    # Preferred tenants – click the checkbox/label matching PREFERRED_TENANT
    wait_and_click(driver, By.XPATH, f"//label[contains(., '{PREFERRED_TENANT}')]/preceding-sibling::input")

    # Furnishing drop‑down
    furnishing_select = Select(
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//select[contains(@name, 'furnishing')]")))
    )
    furnishing_select.select_by_visible_text(FURNISHING)

    # Parking drop‑down
    parking_select = Select(
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//select[contains(@name, 'parking')]")))
    )
    parking_select.select_by_visible_text(PARKING)

    # Save and continue
    wait_and_click(driver, By.XPATH, "//button[contains(., 'Save') and contains(., 'Continue')]")

def fill_amenities(driver: webdriver):
    """Set the various amenity options."""
    # Set bathroom and balcony counts to 1 each
    # Click the plus buttons once for each
    wait_and_click(driver, By.XPATH, "(//button[.='+'])[1]")  # bathroom
    wait_and_click(driver, By.XPATH, "(//button[.='+'])[2]")  # balcony

    # Water supply
    supply_select = Select(
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//select[contains(@name, 'waterSupply')]")))
    )
    supply_select.select_by_visible_text("Corporation")  # fixed choice

    # Toggle yes/no options for pet, non‑veg, gym and gated security
    if AMENITIES.get("Pet Allowed", False):
        wait_and_click(driver, By.XPATH, "//label[contains(., 'Pet Allowed')]/following-sibling::div/button[contains(., 'Yes')]")
    if AMENITIES.get("Non-Veg Allowed", False):
        wait_and_click(driver, By.XPATH, "//label[contains(., 'Non-Veg Allowed')]/following-sibling::div/button[contains(., 'Yes')]")
    if AMENITIES.get("Gym", False):
        wait_and_click(driver, By.XPATH, "//label[contains(., 'Gym')]/following-sibling::div/button[contains(., 'Yes')]")
    if AMENITIES.get("Gated Security", False):
        wait_and_click(driver, By.XPATH, "//label[contains(., 'Gated Security')]/following-sibling::div/button[contains(., 'Yes')]")

    # Who will show the property: select "Security" as an example
    show_select = Select(
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//select[contains(@name, 'showProperty')]")))
    )
    show_select.select_by_visible_text("Security")

    # Current property condition
    condition_select = Select(
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//select[contains(@name, 'propertyCondition')]")))
    )
    condition_select.select_by_visible_text("Average")

    # Scroll down to amenities list and tick checkboxes
    for amenity_name, enabled in AMENITIES.items():
        if amenity_name in {"Pet Allowed", "Non-Veg Allowed", "Gym", "Gated Security"}:
            continue  # already handled above
        if enabled:
            try:
                checkbox = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.XPATH, f"//label[contains(., '{amenity_name}')]/preceding-sibling::input"))
                )
                checkbox.click()
            except Exception:
                # If the amenity is not present, skip it
                pass

    # Save and continue
    wait_and_click(driver, By.XPATH, "//button[contains(., 'Save') and contains(., 'Continue')]")

def upload_gallery_images(driver: webdriver):
    """
    Upload a single image for the property gallery.  The file path points to an
    example image (apple) stored alongside this script.  Adjust the path or
    upload additional images as needed.
    """
    image_path = "68c6914a-b7ae-49fb-83ba-d930341df4cb.png"  # ensure this image exists in your working directory
    # The gallery page typically has multiple file input elements (for bedroom,
    # bathroom, etc.).  Here we choose the first file input as an example.
    file_input = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, "//input[@type='file'][1]"))
    )
    file_input.send_keys(image_path)
    # Click save and continue
    wait_and_click(driver, By.XPATH, "//button[contains(., 'Save') and contains(., 'Continue')]")

def finalize_submission(driver: webdriver):
    """Click through the final screens (schedule/preview) and return to dashboard."""
    # Depending on the site flow, there may be a schedule step.  If present,
    # simply click continue.
    try:
        wait_and_click(driver, By.XPATH, "//button[contains(., 'Save') and contains(., 'Continue')]")
    except Exception:
        pass

    # On the preview/congratulations page, click the Go to Dashboard button
    wait_and_click(driver, By.XPATH, "//button[contains(., 'Dashboard')]")

def post_property(driver: webdriver):
    """Run through the entire workflow to post a single property."""
    fill_first_page(driver)
    fill_property_details(driver)
    fill_location_details(driver)
    fill_rental_details(driver)
    fill_amenities(driver)
    upload_gallery_images(driver)
    finalize_submission(driver)

def main():
    """Main entry point."""
    # Initialize the WebDriver (use the appropriate driver for your browser)
    driver = webdriver.Chrome()
    driver.maximize_window()
    try:
        login_and_wait(driver)
        for i in range(ITERATIONS):
            print(f"Starting listing {i+1}/{ITERATIONS}…")
            post_property(driver)
            # Add a short delay between postings to simulate human behaviour and
            # allow the site to process the previous submission
            time.sleep(2)
    finally:
        driver.quit()

if __name__ == "__main__":
    main()