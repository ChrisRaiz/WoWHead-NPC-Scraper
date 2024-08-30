# Imports
import csv
import re
import pandas
import time
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException

# Base
# csv_path = ['./../Base-WoW/ID/Base_IDs.csv', './Base-WoW/Timeout/Timeout_IDs.csv', './Base-WoW/Invalid/Invalid_IDs.csv', './Base-WoW/Data/NPC_Location.csv']

# Burning Crusade
csv_path = ['./../BC-WoW/ID/BC_IDs.csv', './../BC-WoW/Timeout/BC_Timeout_IDs.csv', './../BC-WoW/Invalid/BC_Invalid_IDs.csv', './../BC-WoW/Data/BC_NPC_Locations.csv']

# Wrath of the Lich King
# csv_path = ['./../WOTLK-WoW/ID/WOTLK_IDs.csv', './WOTLK-WoW/Timeout/Timeout_IDs.csv', './WOTLK-WoW/Invalid/Invalid_IDs.csv', './WOTLK-WoW/Data/NPC_Location.csv']

# Cataclysm
# csv_path = ['./../CAT-WoW/ID/CAT_IDs.csv, './CAT-WoW/Timeout/Timeout_IDs.csv', './CAT-WoW/Invalid/Invalid_IDs.csv', './CAT-WoW/Data/NPC_Location.csv']

# Mists of Pandaria
# csv_path = ['./../MOP-WoW/ID/MOP_IDs.csv, './MOP-WoW/Timeout/Timeout_IDs.csv', './MOP-WoW/Invalid/Invalid_IDs.csv', './MOP-WoW/Data/NPC_Location.csv']

# Warlords of Draenor
# csv_path = ['./../WOD-WoW/ID/WOD_IDs.csv, './WOD-WoW/Timeout/Timeout_IDs.csv', './WOD-WoW/Invalid/Invalid_IDs.csv', './WOD-WoW/Data/NPC_Location.csv']

# Legion
# csv_path = ['./../LEG-WoW/ID/LEG_IDs.csv, './LEG-WoW/Timeout/Timeout_IDs.csv', './LEG-WoW/Invalid/Invalid_IDs.csv', './LEG-WoW/Data/NPC_Location.csv']

# Battle for Azeroth
# csv_path = ['./../BFA-WoW/ID/BFA_IDs.csv, './BFA-WoW/Timeout/Timeout_IDs.csv', './BFA-WoW/Invalid/Invalid_IDs.csv', './BFA-WoW/Data/NPC_Location.csv']

# Shadowlands
# csv_path = ['./../SL-WoW/ID/SL_IDs.csv, './SL-WoW/Timeout/Timeout_IDs.csv', './SL-WoW/Invalid/Invalid_IDs.csv', './SL-WoW/Data/NPC_Location.csv']

# Dragonflight
# csv_path = ['./../DRA-WoW/ID/DRA_IDs.csv, './DRA-WoW/Timeout/Timeout_IDs.csv', './DRA-WoW/Invalid/Invalid_IDs.csv', './DRA-WoW/Data/NPC_Location.csv']

# The War Within
# csv_path = ['./../TWW-WoW/ID/TWW_IDs.csv, './TWW-WoW/Timeout/Timeout_IDs.csv', './TWW-WoW/Invalid/Invalid_IDs.csv', './TWW-WoW/Data/NPC_Location.csv']

# Path to valid_ids.csv
id_path = Path(__file__).parent / csv_path[0]
timeout_path = Path(__file__).parent / csv_path[1]
invalid_path = Path(__file__).parent / csv_path[2]
locations_path = Path(__file__).parent / csv_path[3]
# Read valid_ids.csv (Pandas)
df = pandas.read_csv(id_path)
end = len(df)

# Timeout IDs
timeout_ids = []

# Invalid IDs
invalid_ids = []

# NPC Data
npc_locations = []

# Webdriver
options = webdriver.ChromeOptions()
options.add_argument('--headless=new')
driver = webdriver.Chrome(options=options)

# Gather location data for npc id (start, end)
for row in range(0, end):
  npc_id = df.get('ID')[row] # Get ID from valid_ids.csv
  print(npc_id)

  try:
    # Load webpage / wait 2 seconds before continuing
    driver.get(f'https://www.wowhead.com/npc={npc_id}')
    time.sleep(2)

    # If True, continue to next ID
    location_found = False

    # Redirect if url is incorrect (Different Expansion DB)
    try:
      cur_url = driver.current_url
      if 'https://www.wowhead.com/npc=' not in cur_url:
        cur_url = f'https://www.wowhead.com/npc={npc_id}'
        driver.get(cur_url)
    except WebDriverException:
      print('URL WebDriverException')

    # Check if location is unknown
    try:
      meta_tags = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.TAG_NAME, 'meta')))
      for tag in meta_tags:
        if tag.get_attribute('property') == 'og:description' and 'The location of this NPC is unknown' in tag.get_attribute('content'):
          location_found = True
          npc_locations.append({'ID': npc_id, 'Locations': 'Unknown'})
          break
      if location_found == True:
        continue
    except TimeoutException:
      print('Timed out - Unknown')

    # Get the location
    try:
      locations_container = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="locations"]')))
      locations = locations_container.text
      if locations:
        location_found = True
        locations = re.sub('[^a-zA-Z,]+', ' ', locations).replace(' ,', ',').strip()
        npc_locations.append({'ID': npc_id, 'Locations': locations})
      if location_found == True:
        continue
    except TimeoutException:
      print('Timed out - Location')
    
    # Get the alternative location
    try:
      alt_locations_container = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'heading-size-2')))

      for alt_locations in alt_locations_container:
        element_id = alt_locations.get_attribute('id')
        if element_id:
          location_found = True
          locations = re.sub('[^a-zA-Z,]+', ' ', alt_locations.text).replace(' ,', ',').strip()
          npc_locations.append({'ID': npc_id, 'Locations': locations})

      if location_found == True:
        continue
    except TimeoutException:
      print('Timed out - Alt. Location')
      timeout_ids.append({'ID': npc_id})
      continue
      
    # Invalid ID if loop is not continued
    invalid_ids.append({'ID': npc_id})

  except WebDriverException:
    timeout_ids.append({'ID': npc_id})

# Release the resources allocated by Selenium and shut down the browser
driver.quit()

# Npc location data to .csv file
with open(locations_path, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=['ID', 'Locations'])
    writer.writeheader()
    writer.writerows(npc_locations)

# Invalid ID data to .csv file
with open(invalid_path, mode='w', newline='', encoding='utf-8') as file:
  writer = csv.DictWriter(file, fieldnames=['ID'])
  writer.writeheader()
  writer.writerows(invalid_ids)

# Timeout ID data to .csv file
with open(timeout_path, mode='w', newline='', encoding='utf-8') as file:
  writer = csv.DictWriter(file, fieldnames=['ID'])
  writer.writeheader()
  writer.writerows(timeout_ids)