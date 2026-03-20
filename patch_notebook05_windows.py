"""
patch_notebook05_windows.py
==========================
Patches cells 2 (paths), 6 (data loading), 13 (max epochs), 26 (early stopping)
in 05_TRAISformer_Q1.ipynb for Windows and 150 epochs.
"""
import json
from pathlib import Path

NB_PATH = Path(
    r"F:\PyTorch_GPU\AIS_trajectory_forecasting"
    r"\CEE-Transformer_architecture_driven_trajectory_forecasting"
    r"\CEE-Replication\Geohashed_traisformer\Notebooks\05_TRAISformer_Q1.ipynb"
)

with open(NB_PATH, "r", encoding="utf-8") as f:
    nb = json.load(f)

# ── Patch Cell 2 (Path Setup) ────────────────────────────────────────────────
CELL2_NEW = [
    "from pathlib import Path\n",
    "import os, sys, json, pickle\n",
    "import numpy as np\n",
    "import matplotlib.pyplot as plt\n",
    "import torch\n",
    "from torch.utils.data import DataLoader\n",
    "import pandas as pd\n",
    "\n",
    "# ── Windows paths ────────────────────────────────────────────────\n",
    "BASE_DIR = Path(r'F:\\\\PyTorch_GPU\\\\AIS_trajectory_forecasting')\n",
    "ROOT     = BASE_DIR / 'CEE-Transformer_architecture_driven_trajectory_forecasting'\n",
    "\n",
    "GEODIR        = ROOT / 'CEE-Replication' / 'Geohashed_traisformer'\n",
    "NOTEBOOK_DIR  = GEODIR / 'Notebooks'\n",
    "TRAISFORMER_DIR   = ROOT / 'CEE_TrAISformer'\n",
    "MAIN_NOTEBOOK_DIR = ROOT / 'CEE-Replication' / 'Notebook'\n",
    "REGION_DATA_DIR   = ROOT / 'CEE-Replication' / 'traisformer_data' / 'region_1'\n",
    "RUN_DIR = ROOT / 'CEE-Replication' / 'results' / 'region_1_trAISformer_mlops'\n",
    "\n",
    "for sub in ['processed', 'pkl', 'embeddings', 'results', 'logs']:\n",
    "    (GEODIR / sub).mkdir(parents=True, exist_ok=True)\n",
    "\n",
    "assert TRAISFORMER_DIR.exists(), str(TRAISFORMER_DIR)\n",
    "sys.path.insert(0, str(TRAISFORMER_DIR))\n",
    "sys.path.insert(0, str(MAIN_NOTEBOOK_DIR))\n",
    "sys.path.insert(0, str(NOTEBOOK_DIR))\n",
    "\n",
    "print('ROOT          :', ROOT)\n",
    "print('TRAISFORMER   :', TRAISFORMER_DIR)\n",
    "print('REGION_DATA   :', REGION_DATA_DIR)\n",
    "print('RUN_DIR       :', RUN_DIR)\n",
]

# ── Patch Cell 6 (Parquet Load) ──────────────────────────────────────────────
CELL6_NEW = [
    "import pandas as pd\n",
    "\n",
    "# Q1 merged parquet (already produced by the Geohashed pipeline)\n",
    "input_path = BASE_DIR / 'Data' / 'region_1_q1_merged_renamed.parquet'\n",
    "print('Reading Q1 merged parquet:', input_path)\n",
    "df = pd.read_parquet(input_path)\n",
    "print('Rows loaded:', len(df))\n",
    "print('Columns:', list(df.columns))\n",
    "\n",
    "# Harmonise NAVSTATUS column name expected by AISPreprocessor\n",
    "if 'NAVSTATUS' in df.columns and 'Navstatus' not in df.columns:\n",
    "    df = df.rename(columns={'NAVSTATUS': 'Navstatus'})\n",
    "    print('Renamed NAVSTATUS -> Navstatus')\n",
    "\n",
    "# Copy into Notebooks folder so downstream cells find the file\n",
    "output_file = NOTEBOOK_DIR / 'region_1_q1_merged_renamed.parquet'\n",
    "df.to_parquet(output_file, index=False)\n",
    "print('Saved notebook copy to', output_file)\n",
]

# ── Patch Cell 13 (RegionConfig max_epochs) ───────────────────────────────────
def patch_cell13(cell):
    src = cell["source"]
    new_src = []
    for line in src:
        if "max_epochs =" in line and "120" in line:
            new_src.append(line.replace("120", "150"))
        else:
            new_src.append(line)
    cell["source"] = new_src

# ── Patch Cell 26 (EarlyStoppingConfig max_epochs) ───────────────────────────
def patch_cell26(cell):
    src = cell["source"]
    new_src = []
    for line in src:
        if "max_epochs=" in line and "50" in line:
            new_src.append(line.replace("50", "150"))
        else:
            new_src.append(line)
    cell["source"] = new_src

# ------------------------------------------------------------------
# Find and apply patches
# ------------------------------------------------------------------
all_cells = nb["cells"]

def find_cell_by_snippet(cells, snippet):
    for i, cell in enumerate(cells):
        src = "".join(cell.get("source", []))
        if snippet in src:
            return i
    return None

idx2 = find_cell_by_snippet(all_cells, "ROOT = Path('/home/")
if idx2 is not None:
    all_cells[idx2]["source"] = CELL2_NEW
    print(f"Patched Cell {idx2} (Path Setup)")

idx6 = find_cell_by_snippet(all_cells, "region_1_first_three_2025.parquet")
if idx6 is not None:
    all_cells[idx6]["source"] = CELL6_NEW
    print(f"Patched Cell {idx6} (Parquet Load)")

idx13 = find_cell_by_snippet(all_cells, "class RegionConfig:")
if idx13 is not None:
    patch_cell13(all_cells[idx13])
    print(f"Patched Cell {idx13} (RegionConfig 150 epochs)")

idx26 = find_cell_by_snippet(all_cells, "EarlyStoppingConfig(max_epochs=50")
if idx26 is not None:
    patch_cell26(all_cells[idx26])
    print(f"Patched Cell {idx26} (EarlyStoppingConfig 150 epochs)")

# Write back
with open(NB_PATH, "w", encoding="utf-8") as f:
    json.dump(nb, f, indent=1, ensure_ascii=False)

print("\nNotebook patched successfully.")
