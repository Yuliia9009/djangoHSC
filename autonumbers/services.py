from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def check_available_plates(digits, region_code, tsc_code=None, vehicle_type="all"):
    options = webdriver.ChromeOptions()
    # options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)
    wait = WebDriverWait(driver, 10)
    results = []

    try:
        driver.get("https://opendata.hsc.gov.ua/check-leisure-license-plates/")
        wait.until(EC.presence_of_element_located((By.ID, "region")))

        Select(driver.find_element(By.ID, "region")).select_by_value(str(region_code))
        time.sleep(1)

        if tsc_code:
            Select(driver.find_element(By.ID, "tsc")).select_by_value(tsc_code)
            time.sleep(1)

        Select(driver.find_element(By.ID, "type_venichle")).select_by_value(vehicle_type)
        time.sleep(1)

        number_input = driver.find_element(By.ID, "number")
        number_input.clear()
        number_input.send_keys(digits)

        driver.find_element(By.CSS_SELECTOR, 'input[type="submit"]').click()
        wait.until(EC.presence_of_element_located((By.ID, "exampleTable")))
        time.sleep(1)

        try:
            select_length = Select(driver.find_element(By.NAME, "exampleTable_length"))
            select_length.select_by_value("100")
            time.sleep(1.5)
        except Exception as e:
            print("Не удалось изменить количество записей на странице:", e)

        while True:
            rows = driver.find_elements(By.CSS_SELECTOR, "table#exampleTable tbody tr")
            for row in rows:
                cols = row.find_elements(By.TAG_NAME, "td")
                if len(cols) >= 3:
                    number = cols[0].text.strip()
                    price = cols[1].text.strip()
                    location = cols[2].text.strip()

                    if not digits or digits in number:
                        results.append({
                            "number": number,
                            "price": price,
                            "location": location,
                        })

            try:
                next_button = driver.find_element(By.ID, "exampleTable_next")
                if "disabled" in next_button.get_attribute("class"):
                    break
                else:
                    next_button.click()
                    time.sleep(1.5)
            except:
                break

        return results

    finally:
        driver.quit()