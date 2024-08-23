# Imports
import csv
import pandas
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

# Path to valid_ids.csv
file = Path(__file__).parent / "valid_ids.csv"

# Read valid_ids.csv (Pandas)
df = pandas.read_csv(file)

# Timeout IDs
timeout_id_data = "Timeout_IDs.csv"
timeout_ids = []

# Invalid IDs
invalid_id_data = "Invalid_IDs.csv"
invalid_ids = []

# NPC Data
npc_data = "NPC_Images.csv"
npc_image_data = []

# Webdriver
options = webdriver.ChromeOptions()
options.add_argument("--headless=new")
driver = webdriver.Chrome(options=options)

# Gather img data for npc id (start, end)
for row in range(0, 20725):
  npc_id = df.get("ID")[row] # Get ID from valid_ids.csv
  driver.get(f"https://www.wowhead.com/npc={npc_id}")

  print(npc_id)

  # Gather all img tags on page
  try:
    imgs = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.TAG_NAME, 'img')))
  except TimeoutException:
    timeout_ids.append({'ID': npc_id})
    continue

  # Find the npc img
  for img in imgs:
    img_src = img.get_attribute('src')
    img_class = img.get_attribute('class')
    if img_class == 'border' and 'https://wow.zamimg.com/' in img_src:
      npc_image_data.append({'ID': npc_id, 'Image': img_src})
      continue

  # Invalid ID if loop is not continued
  invalid_ids.append({'ID': npc_id})

# Release the resources allocated by Selenium and shut down the browser
driver.quit()

# Npc image data to .csv file
with open(npc_data, mode="w", newline="", encoding="utf-8") as file:
    #? Write the headers
    writer = csv.DictWriter(file, fieldnames=["ID", "Image"])
    writer.writeheader()
    #? Write the rows
    writer.writerows(npc_image_data)

# Invalid ID data to .csv file
with open(invalid_id_data, mode='w', newline="", encoding='utf-8') as file:
  writer = csv.DictWriter(file, fieldnames=["ID"])
  writer.writeheader()
  writer.writerows(invalid_ids)

# Timeout ID data to .csv file
with open(timeout_id_data, mode='w', newline="", encoding='utf-8') as file:
  writer = csv.DictWriter(file, fieldnames=["ID"])
  writer.writeheader()
  writer.writerows(timeout_ids)