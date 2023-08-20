@echo off
cd /d %~dp0
start python server.py
start python fileupdata.py
start python TimeWork.py
exit
