# Imports
import csv
import re
import pandas
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from pathlib import Path

file = Path(__file__).parent / "valid_ids.csv"
df = pandas.read_csv(file)

# Timeout IDs
timeout_id_data = "Timeout_IDs.csv"
timeout_ids = []

# Invalid IDs
invalid_id_data = "Invalid_IDs.csv"
invalid_ids = []

# NPC Data
npc_data = "NPC_Locations.csv"
npc_locations = []

# Webdriver
options = webdriver.ChromeOptions()
options.add_argument("--headless=new")
driver = webdriver.Chrome(options=options)

# Gather location data for npc id (start, end)
for row in range(0, 20725):
  npc_id = df.get("ID")[row]
  print(npc_id)
  driver.get(f"https://www.wowhead.com/npc={npc_id}")

  location_unknown = False

  # Check if location is unknown
  try:
    meta_tags = WebDriverWait(driver, 5).until(EC.presence_of_all_elements_located((By.TAG_NAME, 'meta')))
    for tag in meta_tags:
      if tag.get_attribute('property') == "og:description" and 'The location of this NPC is unknown' in tag.get_attribute('content'):
        location_unknown = True
        npc_locations.append({'ID': npc_id, 'Locations': 'Unknown'})
        break
  except TimeoutException:
    print('Timed out - Unknown')

  if location_unknown == True:
    continue

  # Get the location
  try:
    # Redirect if url is incorrect (Different Expansion DB)
    cur_url = driver.current_url
    if 'https://www.wowhead.com/npc=' not in cur_url:
      cur_url = f'https://www.wowhead.com/npc={npc_id}'
      driver.get(cur_url)

    # Find location container
    locations_container = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="locations"]')))
  except TimeoutException:
    print('Timed out - Location')
    timeout_ids.append({'ID': npc_id})
    continue

  # Find locations
  locations = locations_container.text
  if locations:
    locations = re.sub('[^a-zA-Z,]+', ' ', locations).replace(' ,', ',').strip()
    npc_locations.append({'ID': npc_id, 'Locations': locations})
    continue

  # Invalid ID if loop is not continued
  invalid_ids.append({'ID': npc_id})

# Release the resources allocated by Selenium and shut down the browser
driver.quit()

# Npc location data to .csv file
with open(npc_data, mode="w", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(file, fieldnames=["ID", "Locations"])
    writer.writeheader()
    writer.writerows(npc_locations)

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