# Imports
import csv
import pandas
import re
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException

# Base
csv_path = [
'./../Expansions/Base/ID/Base_IDs.csv',
'./../Expansions/Base/Timeout/Base_Stats_Timeout_IDs.csv',
'./../Expansions/Base/Invalid/Base_Stats_Invalid_IDs.csv',
'./../Expansions/Base/Data/Base_NPC_Stats.csv'
]

# Burning Crusade
# csv_path = [
#   './../Expansions/BC/ID/BC_IDs.csv',
#   './../Expansions/BC/Timeout/BC_Stats_Timeout_IDs.csv',
#   './../Expansions/BC/Invalid/BC_Stats_Invalid_IDs.csv',
#   './../Expansions/BC/Data/BC_NPC_Stats.csv'
#   ]

# Wrath of the Lich King
# csv_path = [
# './../Expansions/WOTLK/ID/WOTLK_IDs.csv',
# './../Expansions/WOTLK/Timeout/WOTLK_Stats_Timeout_IDs.csv',
# './../Expansions/WOTLK/Invalid/WOTLK_Stats_Invalid_IDs.csv',
# './../Expansions/WOTLK/Data/WOTLK_NPC_Stats.csv'
# ]

# Cataclysm
# csv_path = [
# './../Expansions/CAT/ID/CAT_IDs.csv',
# './../Expansions/CAT/Timeout/CAT_Stats_Timeout_IDs.csv',
# './../Expansions/CAT/Invalid/CAT_Stats_Invalid_IDs.csv',
# './../Expansions/CAT/Data/CAT_NPC_Stats.csv'
# ]

# Mists of Pandaria
# csv_path = [
# './../Expansions/MOP/ID/MOP_IDs.csv',
# './../Expansions/MOP/Timeout/MOP_Stats_Timeout_IDs.csv',
# './../Expansions/MOP/Invalid/MOP_Stats_Invalid_IDs.csv',
# './../Expansions/MOP/Data/MOP_NPC_Stats.csv'
# ]

# Warlords of Draenor
# csv_path = [
# './../Expansions/WOD/ID/WOD_IDs.csv',
# './../Expansions/WOD/Timeout/WOD_Stats_Timeout_IDs.csv',
# './../Expansions/WOD/Invalid/WOD_Stats_Invalid_IDs.csv',
# './../Expansions/WOD/Data/WOD_NPC_Stats.csv'
# ]

# Legion
# csv_path = [
# './../Expansions/LEG/ID/LEG_IDs.csv',
# './../Expansions/LEG/Timeout/LEG_Stats_Timeout_IDs.csv',
# './../Expansions/LEG/Invalid/LEG_Stats_Invalid_IDs.csv',
# './../Expansions/LEG/Data/LEG_NPC_Stats.csv'
# ]

# Battle for Azeroth
# csv_path = [
# './../Expansions/BFA/ID/BFA_IDs.csv',
# './../Expansions/BFA/Timeout/BFA_Stats_Timeout_IDs.csv',
# './../Expansions/BFA/Invalid/BFA_Stats_Invalid_IDs.csv',
# './../Expansions/BFA/Data/BFA_NPC_Stats.csv'
# ]

# Shadowlands
# csv_path = [
# './../Expansions/SL/ID/SL_IDs.csv',
# './../Expansions/Timeout/SL_Stats_Timeout_IDs.csv',
# './../Expansions/Invalid/SL_Stats_Invalid_IDs.csv',
# './../Expansions/Data/SL_NPC_Stats.csv'
# ]

# Dragonflight
# csv_path = [
# './../Expansions/DRA/ID/DRA_IDs.csv',
# './../Expansions/DRA/Timeout/DRA_Stats_Timeout_IDs.csv',
# './../Expansions/DRA/Invalid/DRA_Stats_Invalid_IDs.csv',
# './../Expansions/DRA/Data/DRA_NPC_Stats.csv'
# ]

# The War Within
# csv_path = [
# './../Expansions/TWW/ID/TWW_IDs.csv',
# './../Expansions/TWW/Timeout/TWW_Stats_Timeout_IDs.csv',
# './../Expansions/TWW/Invalid/TWW_Stats_Invalid_IDs.csv',
# './../Expansions/TWW/Data/TWW_NPC_Stats.csv'
# ]

# Paths to csv files
id_path = Path(__file__).parent / csv_path[0]
timeout_path = Path(__file__).parent / csv_path[1]
invalid_path = Path(__file__).parent / csv_path[2]
stats_path = Path(__file__).parent / csv_path[3]

# Read IDs csv
df = pandas.read_csv(id_path)
end = len(df)

# Timeout IDs
timeout_ids = []

# Invalid IDs
invalid_ids = []

# NPC Data
npc_stats = []

# Webdriver
options = webdriver.ChromeOptions()
options.add_argument('--headless=new')
driver = webdriver.Chrome(options=options)

# Gather stat data for every row
for row in range(0, end):
  npc_id = df.get('ID')[row] # Get ID from valid_ids.csv
  print(npc_id)

  try:
    # Load webpage / load page wait - 2 seconds 
    driver.get(f'https://www.wowhead.com/npc={npc_id}')

    # Get the stats list
    try:
      stats_container = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'infobox-inner-table')))
      stats = stats_container.find_elements(By.TAG_NAME, 'div')

      level_data = None
      level_range = False
      classification_data = 'Normal'
      type_data = None
      patch_data = None
      health_data = None

      # 0 and 1 never contain the required data
      for i in range(2, len(stats)):
        stat = stats[i].text
        if 'Level' in stat:
          if ' - ' in stat:
              level_range = True
              level_data = re.sub('[^0-9-?]', '', stat).replace('-', ', ').strip()
          else:
            level_data = re.sub('[^0-9-?]', '', stat).strip()
        elif 'Classification' in stat:
          classification_data = stat.replace('Classification: ', '').strip()
        elif 'Type' in stat:
          type_data = stat.replace('Type: ', '').strip()
        elif 'Added in patch' in stat:
          patch_data = re.sub('[^0-9.]','', stat).strip()
        elif 'Health' in stat:
          health_data = re.sub('[^0-9,]','', stat).strip()

      # Level and Health data are required for NPC to be valid
      if level_data != None and health_data != None:
        npc_stats.append({'ID': npc_id, 'Levels': level_data, 'Level Range': level_range, 'Classification': classification_data, 'Type': type_data, 'Patch': patch_data, 'Health': health_data})
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

# Npc stat data to .csv file
with open(stats_path, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=['ID', 'Levels', 'Level Range', 'Classification', 'Type', 'Patch', 'Health'])
    writer.writeheader()
    writer.writerows(npc_stats)

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