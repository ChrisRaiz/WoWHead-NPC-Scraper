# WoWHead NPC Scraper

A Selenium-based scraper that collects World of Warcraft NPC data from [Wowhead](https://www.wowhead.com) (names, stats, locations, and images) and organizes it into clean, structured CSV datasets.

![Python](https://img.shields.io/badge/Python-3-3776AB?logo=python&logoColor=white)
![Selenium](https://img.shields.io/badge/Selenium-43B02A?logo=selenium&logoColor=white)
![pandas](https://img.shields.io/badge/pandas-150458?logo=pandas&logoColor=white)
![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)

📖 **[Full Documentation](https://chrisraiz.github.io/WoWHead-NPC-Scraper/)**: setup, usage, output format, and troubleshooting.

---

## Overview

Wowhead builds its NPC pages with JavaScript after they load, so a plain HTTP request comes back without the data. This project uses Selenium to drive a headless Chrome browser that waits for each page to finish rendering before reading it.

- **About 20,400 NPC IDs** across all 11 expansions, from Classic to The War Within
- **Complete datasets** for Classic, The Burning Crusade, Wrath of the Lich King, Cataclysm, and Mists of Pandaria
- **Four focused scrapers**, each producing a CSV keyed by NPC ID so the datasets can be joined
- **Failure tracking**: IDs that time out or have no matching data are saved to separate files so they can be retried or reviewed

## What It Collects

| Script | Data | Example |
|---|---|---|
| `name_scraper.py` | Name | C'Thun |
| `stats_scraper.py` | Level, level range, classification, creature type, patch added, health | 60 · Elite · Aberration · 1.11.1 |
| `location_scraper.py` | Zones where the NPC appears | Temple of Ahn Qiraj |
| `image_scraper.py` | Screenshot URL | `wow.zamimg.com/uploads/screenshots/...` |

## Tech Stack

- **Python 3**
- **Selenium** with headless Chrome, for pages that render with JavaScript
- **pandas**, for reading the ID lists
- **CSV** for every output file

## Getting Started

```bash
git clone https://github.com/ChrisRaiz/WoWHead-NPC-Scraper.git
cd WoWHead-NPC-Scraper

python3 -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

pip install selenium pandas
```

You need Google Chrome installed. Selenium 4.6 and later downloads a matching ChromeDriver automatically.

## Usage

1. Open a script in `scripts/` and uncomment the `csv_path` block for the expansion you want (Base is the default).
2. Run it from inside the `scripts` folder:

```bash
cd scripts
python3 stats_scraper.py
```

Results are written to `Expansions/<code>/` once every ID has been processed.

## Project Structure

```
.
├── scripts/
│   ├── name_scraper.py
│   ├── stats_scraper.py
│   ├── location_scraper.py
│   └── image_scraper.py
└── Expansions/
    └── <code>/              # Base, BC, WOTLK, CAT, MOP, WOD, LEG, BFA, SL, DRA, TWW
        ├── ID/              # Input: NPC IDs, all together and by creature type
        ├── Data/            # Output: scraped data
        ├── Invalid/         # Output: IDs whose page had no matching data
        └── Timeout/         # Output: IDs whose page didn't load in time
```

## Expansion Coverage

| Expansion | Code | IDs | Scraped |
|---|---|---|---|
| World of Warcraft (Classic) | Base | 993 | ✅ |
| The Burning Crusade | BC | 977 | ✅ |
| Wrath of the Lich King | WOTLK | 982 | ✅ |
| Cataclysm | CAT | 982 | ✅ |
| Mists of Pandaria | MOP | 750 | ✅ |
| Warlords of Draenor | WOD | 904 | — |
| Legion | LEG | 927 | — |
| Battle for Azeroth | BFA | 901 | — |
| Shadowlands | SL | 917 | — |
| Dragonflight | DRA | 930 | — |
| The War Within | TWW | 952 | — |

## Disclaimer

This is a personal, non-commercial project. All game data belongs to Blizzard Entertainment and Wowhead. Please scrape responsibly and follow Wowhead's terms of service.

## License

Released under the [MIT License](LICENSE).
