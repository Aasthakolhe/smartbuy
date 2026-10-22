@echo off
echo === SmartBuy setup and run ===
python -m venv venv
call venv\Scripts\activate
pip install -r requirements.txt
python generate_catalog.py
python analysis.py
python validate_real_data.py
echo.
echo Done. Check the output folder.
pause
