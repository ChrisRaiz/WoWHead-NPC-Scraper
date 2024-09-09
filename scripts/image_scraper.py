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
'./../Expansions/Base/Timeout/Base_Images_Timeout_IDs.csv',
'./../Expansions/Base/Invalid/Base_Images_Invalid_IDs.csv',
'./../Expansions/Base/Data/Base_NPC_Images.csv'
]

# Burning Crusade
# csv_path = [
#   './../Expansions/BC/ID/BC_IDs.csv',
#   './../Expansions/BC/Timeout/BC_Images_Timeout_IDs.csv',
#   './../Expansions/BC/Invalid/BC_Images_Invalid_IDs.csv',
#   './../Expansions/BC/Data/BC_NPC_Images.csv'
#   ]

# Wrath of the Lich King
# csv_path = [
# './../Expansions/WOTLK/ID/WOTLK_IDs.csv',
# './../Expansions/WOTLK/Timeout/WOTLK_Images_Timeout_IDs.csv',
# './../Expansions/WOTLK/Invalid/WOTLK_Images_Invalid_IDs.csv',
# './../Expansions/WOTLK/Data/WOTLK_NPC_Images.csv'
# ]

# Cataclysm
# csv_path = [
# './../Expansions/CAT/ID/CAT_IDs.csv',
# './../Expansions/CAT/Timeout/CAT_Images_Timeout_IDs.csv',
# './../Expansions/CAT/Invalid/CAT_Images_Invalid_IDs.csv',
# './../Expansions/CAT/Data/CAT_NPC_Images.csv'
# ]

# Mists of Pandaria
# csv_path = [
# './../Expansions/MOP/ID/MOP_IDs.csv',
# './../Expansions/MOP/Timeout/MOP_Images_Timeout_IDs.csv',
# './../Expansions/MOP/Invalid/MOP_Images_Invalid_IDs.csv',
# './../Expansions/MOP/Data/MOP_NPC_Images.csv'
# ]

# Warlords of Draenor
# csv_path = [
# './../Expansions/WOD/ID/WOD_IDs.csv',
# './../Expansions/WOD/Timeout/WOD_Images_Timeout_IDs.csv',
# './../Expansions/WOD/Invalid/WOD_Images_Invalid_IDs.csv',
# './../Expansions/WOD/Data/WOD_NPC_Images.csv'
# ]

# Legion
# csv_path = [
# './../Expansions/LEG/ID/LEG_IDs.csv',
# './../Expansions/LEG/Timeout/LEG_Images_Timeout_IDs.csv',
# './../Expansions/LEG/Invalid/LEG_Images_Invalid_IDs.csv',
# './../Expansions/LEG/Data/LEG_NPC_Images.csv'
# ]

# Battle for Azeroth
# csv_path = [
# './../Expansions/BFA/ID/BFA_IDs.csv',
# './../Expansions/BFA/Timeout/BFA_Images_Timeout_IDs.csv',
# './../Expansions/BFA/Invalid/BFA_Images_Invalid_IDs.csv',
# './../Expansions/BFA/Data/BFA_NPC_Images.csv'
# ]

# Shadowlands
# csv_path = [
# './../Expansions/SL/ID/SL_IDs.csv',
# './../Expansions/Timeout/SL_Images_Timeout_IDs.csv',
# './../Expansions/Invalid/SL_Images_Invalid_IDs.csv',
# './../Expansions/Data/SL_NPC_Images.csv'
# ]

# Dragonflight
# csv_path = [
# './../Expansions/DRA/ID/DRA_IDs.csv',
# './../Expansions/DRA/Timeout/DRA_Images_Timeout_IDs.csv',
# './../Expansions/DRA/Invalid/DRA_Images_Invalid_IDs.csv',
# './../Expansions/DRA/Data/DRA_NPC_Images.csv'
# ]

# The War Within
# csv_path = [
# './../Expansions/TWW/ID/TWW_IDs.csv',
# './../Expansions/TWW/Timeout/TWW_Images_Timeout_IDs.csv',
# './../Expansions/TWW/Invalid/TWW_Images_Invalid_IDs.csv',
# './../Expansions/TWW/Data/TWW_NPC_Images.csv'
# ]

# Paths to csv files
id_path = Path(__file__).parent / csv_path[0]
timeout_path = Path(__file__).parent / csv_path[1]
invalid_path = Path(__file__).parent / csv_path[2]
images_path = Path(__file__).parent / csv_path[3]

# Read IDs csv
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

# Gather image data for every row
for row in range(0, end):
  npc_id = df.get("ID")[row] # Get ID from valid_ids.csv
  print(npc_id)

  try:
    # Load webpage / load page wait - 2 seconds 
    driver.get(f"https://www.wowhead.com/npc={npc_id}")

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