# Imports
import csv
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
'./../Expansions/Base/Timeout/Base_Names_Timeout_IDs.csv',
'./../Expansions/Base/Invalid/Base_Names_Invalid_IDs.csv',
'./../Expansions/Base/Data/Base_NPC_Names.csv'
]

# Burning Crusade
# csv_path = [
#   './../Expansions/BC/ID/BC_IDs.csv',
#   './../Expansions/BC/Timeout/BC_Names_Timeout_IDs.csv',
#   './../Expansions/BC/Invalid/BC_Names_Invalid_IDs.csv',
#   './../Expansions/BC/Data/BC_NPC_Names.csv'
#   ]

# Wrath of the Lich King
# csv_path = [
# './../Expansions/WOTLK/ID/WOTLK_IDs.csv',
# './../Expansions/WOTLK/Timeout/WOTLK_Names_Timeout_IDs.csv',
# './../Expansions/WOTLK/Invalid/WOTLK_Names_Invalid_IDs.csv',
# './../Expansions/WOTLK/Data/WOTLK_NPC_Names.csv'
# ]

# Cataclysm
# csv_path = [
# './../Expansions/CAT/ID/CAT_IDs.csv',
# './../Expansions/CAT/Timeout/CAT_Names_Timeout_IDs.csv',
# './../Expansions/CAT/Invalid/CAT_Names_Invalid_IDs.csv',
# './../Expansions/CAT/Data/CAT_NPC_Names.csv'
# ]

# Mists of Pandaria
# csv_path = [
# './../Expansions/MOP/ID/MOP_IDs.csv',
# './../Expansions/MOP/Timeout/MOP_Names_Timeout_IDs.csv',
# './../Expansions/MOP/Invalid/MOP_Names_Invalid_IDs.csv',
# './../Expansions/MOP/Data/MOP_NPC_Names.csv'
# ]

# Warlords of Draenor
# csv_path = [
# './../Expansions/WOD/ID/WOD_IDs.csv',
# './../Expansions/WOD/Timeout/WOD_Names_Timeout_IDs.csv',
# './../Expansions/WOD/Invalid/WOD_Names_Invalid_IDs.csv',
# './../Expansions/WOD/Data/WOD_NPC_Names.csv'
# ]

# Legion
# csv_path = [
# './../Expansions/LEG/ID/LEG_IDs.csv',
# './../Expansions/LEG/Timeout/LEG_Names_Timeout_IDs.csv',
# './../Expansions/LEG/Invalid/LEG_Names_Invalid_IDs.csv',
# './../Expansions/LEG/Data/LEG_NPC_Names.csv'
# ]

# Battle for Azeroth
# csv_path = [
# './../Expansions/BFA/ID/BFA_IDs.csv',
# './../Expansions/BFA/Timeout/BFA_Names_Timeout_IDs.csv',
# './../Expansions/BFA/Invalid/BFA_Names_Invalid_IDs.csv',
# './../Expansions/BFA/Data/BFA_NPC_Names.csv'
# ]

# Shadowlands
# csv_path = [
# './../Expansions/SL/ID/SL_IDs.csv',
# './../Expansions/Timeout/SL_Names_Timeout_IDs.csv',
# './../Expansions/Invalid/SL_Names_Invalid_IDs.csv',
# './../Expansions/Data/SL_NPC_Names.csv'
# ]

# Dragonflight
# csv_path = [
# './../Expansions/DRA/ID/DRA_IDs.csv',
# './../Expansions/DRA/Timeout/DRA_Names_Timeout_IDs.csv',
# './../Expansions/DRA/Invalid/DRA_Names_Invalid_IDs.csv',
# './../Expansions/DRA/Data/DRA_NPC_Names.csv'
# ]

# The War Within
# csv_path = [
# './../Expansions/TWW/ID/TWW_IDs.csv',
# './../Expansions/TWW/Timeout/TWW_Names_Timeout_IDs.csv',
# './../Expansions/TWW/Invalid/TWW_Names_Invalid_IDs.csv',
# './../Expansions/TWW/Data/TWW_NPC_Names.csv'
# ]

# Paths to csv files
id_path = Path(__file__).parent / csv_path[0]
timeout_path = Path(__file__).parent / csv_path[1]
invalid_path = Path(__file__).parent / csv_path[2]
names_path = Path(__file__).parent / csv_path[3]

# Read IDs csv
df = pandas.read_csv(id_path)
end = len(df)

# Timeout IDs
timeout_ids = []

# Invalid IDs
invalid_ids = []

# NPC Data
npc_names = []

# Webdriver
options = webdriver.ChromeOptions()
options.add_argument("--headless=new")
driver = webdriver.Chrome(options=options)

# Gather name data for every row
for row in range(0, end):
  npc_id = df.get("ID")[row] # Get ID from valid_ids.csv
  print(npc_id)
  url = f"https://www.wowhead.com/npc={npc_id}"
  # try:
    # Load webpage / load page wait - 2 seconds 
  driver.get(url)

  # Get the title text
  try:
    name = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "/html/head/title"))).get_attribute('innerText')

    if " - NPC - World of Warcraft" in name:
      name = name.replace(" - NPC - World of Warcraft", "").strip()
      npc_names.append({'ID': npc_id, 'Name': name})
      continue
  except TimeoutException:
    timeout_ids.append({'ID': npc_id})
    continue

    # Invalid ID if loop is not continued
  invalid_ids.append({'ID': npc_id})
  # except WebDriverException:
  #   timeout_ids.append({'ID': npc_id})

# Release the resources allocated by Selenium and shut down the browser
driver.quit()

# Npc name data to .csv file
with open(names_path, mode="w", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(file, fieldnames=["ID", "Name"])
    writer.writeheader()
    writer.writerows(npc_names)

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