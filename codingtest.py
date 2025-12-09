import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.expected_conditions import presence_of_element_located

def test_failed_login_banned_user(driver, wait):
    """Test login with banned user account"""
    driver.find_element(By.ID, "user-name").send_keys("locked_out_user")
    driver.find_element(By.ID, "password").send_keys("secret_sauce")
    driver.find_element(By.ID, "login-button").click()
    
    error_msg = wait.until(presence_of_element_located((By.XPATH, "//h3[@data-test='error']")))
    expected_text = "Sorry, this user has been banned"
    assert expected_text in error_msg.text, f"Expected '{expected_text}', got '{error_msg.text}'"

def test_failed_login_invalid_credentials(driver, wait):
    """Test login with invalid credentials"""
    driver.find_element(By.ID, "user-name").send_keys("invalid_user")
    driver.find_element(By.ID, "password").send_keys("wrong_password")
    driver.find_element(By.ID, "login-button").click()
    
    error_msg = wait.until(presence_of_element_located((By.XPATH, "//h3[@data-test='error']")))
    expected_text = "Username and password do not match"
    assert expected_text in error_msg.text, f"Expected '{expected_text}', got '{error_msg.text}'"

def test_successful_login(driver, wait):
    """Test successful login with valid credentials"""
    driver.find_element(By.ID, "user-name").send_keys("standard_user")
    driver.find_element(By.ID, "password").send_keys("secret_sauce")
    driver.find_element(By.ID, "login-button").click()
    
    logo = wait.until(presence_of_element_located((By.XPATH, "//div[@class='app_logo']")))
    assert logo.is_displayed(), "App Logo should be displayed after successful login"

    wait.until(EC.text_to_be_present_in_element((By.XPATH, "//*[@id='header_container']/div[2]/span"), "Products"))
    
    #get the text of all items using list comprehension
    items = [item.text for item in driver.find_elements(By.CLASS_NAME, "inventory_item_name")]
    print("Items available after login:", items)
    
    print("All items verified successfully")

    #Write the items to a text file
    with open("items_list.txt", "w") as f:
        for item in items:
            f.write(item + "\n")
    print("Items list written to items_list.txt")

