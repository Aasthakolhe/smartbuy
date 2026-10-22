#!/bin/bash
echo "=== SmartBuy setup and run ==="
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python generate_catalog.py
python analysis.py
python validate_real_data.py
echo "Done. Check the output folder."
