import time, csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import *

URL = "https://rera.odisha.gov.in/projects/project-list"
CSV_FILE_NAME = "rera_projects_data.csv"

def scrape_rera_projects(num_projects_to_scrape=6):
    all_projects_data = []
    options = webdriver.ChromeOptions()
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--window-size=1920,1080')
    options.add_argument('--start-maximized')
    options.add_argument("user-agent=Mozilla/5.0")

    driver = webdriver.Chrome(options=options)

    try:
        driver.get(URL)
        time.sleep(3)
        WebDriverWait(driver, 30).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.card.project-card")))

        try:
            WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Accept') or contains(text(), 'Close') or contains(text(), 'OK')]"))
            ).click()
            time.sleep(1)
        except: pass

        scraped_count = 0
        for i in range(len(driver.find_elements(By.CSS_SELECTOR, "div.card.project-card"))):
            if scraped_count >= num_projects_to_scrape:
                break

            try:
                project_cards = WebDriverWait(driver, 10).until(
                    EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.card.project-card"))
                )
                if i >= len(project_cards): continue
                current_card = project_cards[i]
            except: continue

            project_data = {}
            try:
                project_data['Project Name'] = current_card.find_element(By.XPATH, ".//h5[contains(@class, 'card-title')]").text.strip()
            except: project_data['Project Name'] = "Not Found"

            try:
                project_data['Rera Regd. No'] = current_card.find_element(By.XPATH, ".//span[contains(@class, 'fw-bold') and contains(@class, 'me-2')]").text.strip()
            except: project_data['Rera Regd. No'] = "Not Found"

            try:
                view_details_button = WebDriverWait(current_card, 10).until(EC.element_to_be_clickable((By.XPATH, ".//a[contains(text(), 'View Details')]")))
                driver.execute_script("arguments[0].scrollIntoView(true);", view_details_button)
                driver.execute_script("var e=document.querySelector('div.header-utilities__setting.d-md-flex.text-nowrap.d-none');if(e){e.style.pointerEvents='none';}")
                prev_url = driver.current_url
                driver.execute_script("arguments[0].click();", view_details_button)
                WebDriverWait(driver, 20).until(EC.url_changes(prev_url))

                WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'Promoter Details')]"))).click()
                time.sleep(1.5)
                WebDriverWait(driver, 35).until(EC.visibility_of_element_located((By.XPATH, "/html/body/app-root/app-project-details/app-inner-layout/div/div[2]/div/div/app-promoter-details/div[1]/div/div[2]/div/div[1]/div/div[2]/strong")))

                try:
                    project_data['Promoter Name (Company Name)'] = driver.find_element(By.XPATH, "/html/body/app-root/app-project-details/app-inner-layout/div/div[2]/div/div/app-promoter-details/div[1]/div/div[2]/div/div[1]/div/div[2]/strong").text.strip()
                except: project_data['Promoter Name (Company Name)'] = "Not Found"

                try:
                    project_data['Address of the Promoter'] = driver.find_element(By.XPATH, "/html/body/app-root/app-project-details/app-inner-layout/div/div[2]/div/div/app-promoter-details/div[1]/div/div[2]/div/div[6]/div/div[2]/strong").text.strip()
                except: project_data['Address of the Promoter'] = "Not Found"

                try:
                    project_data['GST No.'] = driver.find_element(By.XPATH, "/html/body/app-root/app-project-details/app-inner-layout/div/div[2]/div/div/app-promoter-details/div[1]/div/div[2]/div/div[11]/div/div[2]/strong").text.strip()
                except: project_data['GST No.'] = "Not Found"

                all_projects_data.append(project_data)
                scraped_count += 1
                driver.back()
                WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.card.project-card")))

            except:
                try:
                    driver.back()
                    WebDriverWait(driver, 15).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.card.project-card")))
                except: pass
                continue

    except: pass
    finally:
        driver.quit()

    if all_projects_data:
        csv_headers = ['Rera Regd. No', 'Project Name', 'Promoter Name (Company Name)', 'Address of the Promoter', 'GST No.']
        for project in all_projects_data:
            for header in csv_headers:
                if header not in project:
                    project[header] = "Not Found"
        with open(CSV_FILE_NAME, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=csv_headers)
            writer.writeheader()
            writer.writerows(all_projects_data)

if __name__ == "__main__":
    scrape_rera_projects()
