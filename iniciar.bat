@echo off
cd apirest
start python main.py
cd ..
cd todo
cd src
start python bl.py
cd ..
cd ..
start chrome http://localhost:8000/menu