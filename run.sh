find . -name "*.pyc" -exec rm -rf {} \;
sh makeGui.sh
clear
python -B src/Classes.py
python -B src/Main.py
