# Imports
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

# Timeout IDs
timeout_id_data = "Timeout_IDs.csv"
timeout_ids = []

# Invalid IDs
invalid_id_data = "Invalid_IDs.csv"
invalid_ids = []

# NPC Data
npc_data = "NPC_Names.csv"
npc_names = []

# Webdriver
options = webdriver.ChromeOptions()
options.add_argument("--headless=new")
driver = webdriver.Chrome(options=options)

# Gather name data for npc id (start, end)
for npc_id in range(1, 1000):
  print(npc_id)
  driver.get(f"https://www.wowhead.com/npc={npc_id}")

  # Get the title text (name - NPC - World of Warcraft)
  try:
    npc_name = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "/html/head/title"))).get_attribute('innerText')
  except TimeoutException:
    timeout_ids.append({'ID': npc_id})
    continue
  
  # Check if the title is a valid ID
  if " - NPC - World of Warcraft" in npc_name:
    npc_name = npc_name.replace(" - NPC - World of Warcraft", "").strip()
    npc_names.append({'ID': npc_id, 'Name': npc_name})
    continue

  # Invalid ID if loop is not continued
  invalid_ids.append({'ID': npc_id})

# Release the resources allocated by Selenium and shut down the browser
driver.quit()

# Npc name data to .csv file
with open(npc_data, mode="w", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(file, fieldnames=["ID", "Name"])
    writer.writeheader()
    writer.writerows(npc_names)

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