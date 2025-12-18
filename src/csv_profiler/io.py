from __future__ import annotations
from csv import DictReader
from pathlib import Path


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    
    if not path.exists():
      raise FileNotFoundError(f"CSV not found: {path}")
   
    with path.open("r",encoding="utf-8")as f:
      reader=DictReader(f)
      row = list(reader)
    
    if not row:
       raise ValueError("CSV fill has no rows!")
    return row
    


      