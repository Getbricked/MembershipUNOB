from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions

import getpass

password = getpass.getpass()

driver = webdriver.Chrome()
driver.get("https://intranet.unob.cz")

elem = driver.find_element(By.ID, "userNameInput")
elem.clear()
elem.send_keys("email@unob.cz")
elem.send_keys(Keys.RETURN)

elem = driver.find_element(By.ID, "passwordInput")
elem.clear()
elem.send_keys(password)
elem.send_keys(Keys.RETURN)

elem = driver.find_element(By.ID, "submitButton")
elem.click()


driver.get("https://intranet.unob.cz/aplikace/SitePages/DomovskaStranka.aspx")

# Seznam akreditovanych programu
# elem = driver.find_element(By.ID, "ctl00_ctl40_g_ba0590ba_842f_4a3a_b2ea_0c665ea80655_ctl00_LvApplicationGroupList_ctrl0_ctl00_LvApplicationsList_ctrl7_btnApp")
elem = WebDriverWait(driver, 10).until(
    expected_conditions.presence_of_element_located(
        (
            By.ID,
            "ctl00_ctl40_g_ba0590ba_842f_4a3a_b2ea_0c665ea80655_ctl00_LvApplicationGroupList_ctrl0_ctl00_LvApplicationsList_ctrl7_btnApp",
        )
    )
)
elem.click()

assert "No results found." not in driver.page_source
driver.close()
