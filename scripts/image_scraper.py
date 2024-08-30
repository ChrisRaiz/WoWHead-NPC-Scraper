# Imports
import csv
import pandas
import time
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException

csv_path = './../BC-WoW/ID/BC_IDs.csv'

# Path to valid_ids.csv
id_path = Path(__file__).parent / csv_path
images_path = Path(__file__).parent / './../BC-WoW/Data/BC_NPC_Images.csv'
timeout_path = Path(__file__).parent / './../BC-WoW/Timeout/BC_Images_Timeout_IDs.csv'
invalid_path = Path(__file__).parent / './../BC-WoW/Invalid/BC_Images_Invalid_IDs.csv'
# Read valid_ids.csv (Pandas)
df = pandas.read_csv(id_path)
end = len(df)


# Timeout IDs
timeout_ids = []

# Invalid IDs
invalid_ids = []

# NPC Data
npc_image_data = []

# Webdriver
options = webdriver.ChromeOptions()
options.add_argument("--headless=new")
driver = webdriver.Chrome(options=options)

# Gather img data for npc id (start, end)
for row in range(0, end):
  npc_id = df.get("ID")[row] # Get ID from valid_ids.csv
  print(npc_id)

  try:
    driver.get(f"https://www.wowhead.com/npc={npc_id}")
    time.sleep(2)

    image_found = False

    # Gather all img tags on page
    try:
      imgs = WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located((By.TAG_NAME, 'img')))
      for img in imgs:
        img_src = img.get_attribute('src')
        img_class = img.get_attribute('class')
        if img_class == 'border' and 'https://wow.zamimg.com/' in img_src:
          image_found = True
          npc_image_data.append({'ID': npc_id, 'Image': img_src})
          break
      if image_found:
        continue
    except TimeoutException:
      timeout_ids.append({'ID': npc_id})
      continue

    # Invalid ID if loop is not continued
    invalid_ids.append({'ID': npc_id})

  except WebDriverException:
    timeout_ids.append({'ID': npc_id})

# Release the resources allocated by Selenium and shut down the browser
driver.quit()

# Npc image data to .csv file
with open(images_path, mode="w", newline="", encoding="utf-8") as file:
    #? Write the headers
    writer = csv.DictWriter(file, fieldnames=["ID", "Image"])
    writer.writeheader()
    #? Write the rows
    writer.writerows(npc_image_data)

# Invalid ID data to .csv file
with open(invalid_path, mode='w', newline="", encoding='utf-8') as file:
  writer = csv.DictWriter(file, fieldnames=["ID"])
  writer.writeheader()
  writer.writerows(invalid_ids)

# Timeout ID data to .csv file
with open(timeout_path, mode='w', newline="", encoding='utf-8') as file:
  writer = csv.DictWriter(file, fieldnames=["ID"])
  writer.writeheader()
  writer.writerows(timeout_ids)