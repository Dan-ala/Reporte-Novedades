@echo off
cd apirest
start python api.py
cd ..
cd todo
cd src
start python run.py
cd ..
cd ..
start chrome http://localhost:8000/menu