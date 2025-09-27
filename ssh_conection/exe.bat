@echo off
cd /d "C:\automatizaciones_consuerte\ssh_conection"
call env\Scripts\activate
python superflex_prod.py
pause
