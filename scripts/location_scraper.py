# Imports
import csv
import re
import pandas
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException

# Base
csv_path = [
'./../Expansions/Base/ID/Base_IDs.csv',
'./../Expansions/Base/Timeout/Base_Locations_Timeout_IDs.csv',
'./../Expansions/Base/Invalid/Base_Locations_Invalid_IDs.csv',
'./../Expansions/Base/Data/Base_NPC_Locations.csv'
]

# Burning Crusade
# csv_path = [
#   './../Expansions/BC/ID/BC_IDs.csv',
#   './../Expansions/BC/Timeout/BC_Locations_Timeout_IDs.csv',
#   './../Expansions/BC/Invalid/BC_Locations_Invalid_IDs.csv',
#   './../Expansions/BC/Data/BC_NPC_Locations.csv'
#   ]

# Wrath of the Lich King
# csv_path = [
# './../Expansions/WOTLK/ID/WOTLK_IDs.csv',
# './../Expansions/WOTLK/Timeout/WOTLK_Locations_Timeout_IDs.csv',
# './../Expansions/WOTLK/Invalid/WOTLK_Locations_Invalid_IDs.csv',
# './../Expansions/WOTLK/Data/WOTLK_NPC_Locations.csv'
# ]

# Cataclysm
# csv_path = [
# './../Expansions/CAT/ID/CAT_IDs.csv',
# './../Expansions/CAT/Timeout/CAT_Locations_Timeout_IDs.csv',
# './../Expansions/CAT/Invalid/CAT_Locations_Invalid_IDs.csv',
# './../Expansions/CAT/Data/CAT_NPC_Locations.csv'
# ]

# Mists of Pandaria
# csv_path = [
# './../Expansions/MOP/ID/MOP_IDs.csv',
# './../Expansions/MOP/Timeout/MOP_Locations_Timeout_IDs.csv',
# './../Expansions/MOP/Invalid/MOP_Locations_Invalid_IDs.csv',
# './../Expansions/MOP/Data/MOP_NPC_Locations.csv'
# ]

# Warlords of Draenor
# csv_path = [
# './../Expansions/WOD/ID/WOD_IDs.csv',
# './../Expansions/WOD/Timeout/WOD_Locations_Timeout_IDs.csv',
# './../Expansions/WOD/Invalid/WOD_Locations_Invalid_IDs.csv',
# './../Expansions/WOD/Data/WOD_NPC_Locations.csv'
# ]

# Legion
# csv_path = [
# './../Expansions/LEG/ID/LEG_IDs.csv',
# './../Expansions/LEG/Timeout/LEG_Locations_Timeout_IDs.csv',
# './../Expansions/LEG/Invalid/LEG_Locations_Invalid_IDs.csv',
# './../Expansions/LEG/Data/LEG_NPC_Locations.csv'
# ]

# Battle for Azeroth
# csv_path = [
# './../Expansions/BFA/ID/BFA_IDs.csv',
# './../Expansions/BFA/Timeout/BFA_Locations_Timeout_IDs.csv',
# './../Expansions/BFA/Invalid/BFA_Locations_Invalid_IDs.csv',
# './../Expansions/BFA/Data/BFA_NPC_Locations.csv'
# ]

# Shadowlands
# csv_path = [
# './../Expansions/SL/ID/SL_IDs.csv',
# './../Expansions/Timeout/SL_Locations_Timeout_IDs.csv',
# './../Expansions/Invalid/SL_Locations_Invalid_IDs.csv',
# './../Expansions/Data/SL_NPC_Locations.csv'
# ]

# Dragonflight
# csv_path = [
# './../Expansions/DRA/ID/DRA_IDs.csv',
# './../Expansions/DRA/Timeout/DRA_Locations_Timeout_IDs.csv',
# './../Expansions/DRA/Invalid/DRA_Locations_Invalid_IDs.csv',
# './../Expansions/DRA/Data/DRA_NPC_Locations.csv'
# ]

# The War Within
# csv_path = [
# './../Expansions/TWW/ID/TWW_IDs.csv',
# './../Expansions/TWW/Timeout/TWW_Locations_Timeout_IDs.csv',
# './../Expansions/TWW/Invalid/TWW_Locations_Invalid_IDs.csv',
# './../Expansions/TWW/Data/TWW_NPC_Locations.csv'
# ]

# Paths to csv files
id_path = Path(__file__).parent / csv_path[0]
timeout_path = Path(__file__).parent / csv_path[1]
invalid_path = Path(__file__).parent / csv_path[2]
locations_path = Path(__file__).parent / csv_path[3]

# Read IDs csv
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

# Gather location data for every row
for row in range(0, end):
  npc_id = df.get('ID')[row] # Get ID from valid_ids.csv
  print(npc_id)

  try:
    # Load webpage / load page wait - 2 seconds 
    driver.get(f'https://www.wowhead.com/npc={npc_id}')

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