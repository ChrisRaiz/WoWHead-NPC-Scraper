# Imports
import csv
import pandas
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

# To create the NPC ID files, set the following filters
# Level | Min = 1, Max = None
# Added in Patch | >= 1.1.2
# Added in Expansion | Expansion to look for NPC IDs
# Addition Filter - Type | Check every type, for each copy the ID values
# Creature Types - https://wowpedia.fandom.com/wiki/Creature

csv_path = './../BC-WoW/ID/BC_IDs.csv'

# Path to valid_ids.csv
file = Path(__file__).parent / csv_path

# Read valid_ids.csv (Pandas)
df = pandas.read_csv(file)
end = len(df)
print(end)

# Timeout IDs
timeout_id_data = 'Timeout_IDs.csv'
timeout_ids = []

# Invalid IDs
invalid_id_data = 'Invalid_IDs.csv'
invalid_ids = []

# NPC Data
npc_data = 'NPC_Stats.csv'
npc_stats = []

# Webdriver
options = webdriver.ChromeOptions()
options.add_argument('--headless=new')
driver = webdriver.Chrome(options=options)

# Gather stat data for npc id (start, end)
for row in range(0, end):
  npc_id = df.get('ID')[row] # Get ID from valid_ids.csv
  driver.get(f'https://www.wowhead.com/npc={npc_id}')

  print(npc_id)

  # Scoping variables
  level_data = None
  level_range = None
  classification_data = 'Normal'
  type_data = None
  patch_data = None
  health_data = None

  # Get the stats
  try:
    stats_container = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'infobox-inner-table')))
    stats = stats_container.find_elements(By.TAG_NAME, 'div')

    # Starts at index 2 due to 0 and 1 not containing the required data
    for i in range(2, len(stats)):
      stat = stats[i].text
      if 'Level' in stat:
        if ' - ' in stat:
            level_range = True
            level_data = stat.replace('Level:', '').replace(' - ', ', ').strip()
        else:
          level_data = stat.replace('Level: ', '').strip()
      elif 'Classification' in stat:
        classification_data = stat.replace('Classification: ', '').strip()
      elif 'Type' in stat:
        type_data = stat.replace('Type: ', '').strip()
      elif 'Added in patch' in stat:
        patch_data = stat.replace('Added in patch ', '').strip()
      elif 'Health' in stat:
        health_data = stat.replace('Health: ', '').strip()
  except TimeoutException:
    timeout_ids.append({'ID': npc_id})
    continue
  
  # Level and Health data are required for NPC to be valid
  if level_data != None and health_data != None:
    npc_stats.append({'ID': npc_id, 'Levels': level_data, 'Level Range': level_range, 'Classification': classification_data, 'Type': type_data, 'Patch': patch_data, 'Health': health_data})
    continue

  # Invalid ID if loop is not continued
  invalid_ids.append({'ID': npc_id})

# Release the resources allocated by Selenium and shut down the browser
driver.quit()

# Npc stat data to .csv file
with open(npc_data, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=['ID', 'Levels', 'Level Range', 'Classification', 'Type', 'Patch', 'Health'])
    writer.writeheader()
    writer.writerows(npc_stats)

# Invalid ID data to .csv file
with open(invalid_id_data, mode='w', newline='', encoding='utf-8') as file:
  writer = csv.DictWriter(file, fieldnames=['ID'])
  writer.writeheader()
  writer.writerows(invalid_ids)

# Timeout ID data to .csv file
with open(timeout_id_data, mode='w', newline='', encoding='utf-8') as file:
  writer = csv.DictWriter(file, fieldnames=['ID'])
  writer.writeheader()
  writer.writerows(timeout_ids)