@echo off
cd apirest
start python main.py
start python routes.py
cd ..
cls
start chrome http://localhost:8000/login