@echo off
python train.py "data" "models/new"
python generate.py "models/new" "" 5
pause