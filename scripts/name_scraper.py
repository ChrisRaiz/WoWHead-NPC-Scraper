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
names_path = Path(__file__).parent / './../BC-WoW/Data/BC_NPC_Names.csv'
timeout_path = Path(__file__).parent / './../BC-WoW/Timeout/BC_Name_Timeout_IDs.csv'
invalid_path = Path(__file__).parent / './../BC-WoW/Invalid/BC_Name_Invalid_IDs.csv'

# Read valid_ids.csv (Pandas)
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

# Gather name data for npc id (start, end)
for row in range(0, end):
  npc_id = df.get("ID")[row] # Get ID from valid_ids.csv
  print(npc_id)

  try:
    driver.get(f"https://www.wowhead.com/npc={npc_id}")
    time.sleep(2)

    # Get the title text (name - NPC - World of Warcraft)
    try:
      name = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "/html/head/title"))).get_attribute('innerText')
    except TimeoutException:
      timeout_ids.append({'ID': npc_id})
      continue
    
    # Check if the title is a valid ID
    if " - NPC - World of Warcraft" in name:
      name = name.replace(" - NPC - World of Warcraft", "").strip()
      npc_names.append({'ID': npc_id, 'Name': name})
      continue

    # Invalid ID if loop is not continued
    invalid_ids.append({'ID': npc_id})
  except WebDriverException:
    row -= 1
    continue

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