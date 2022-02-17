@echo off
pyinstaller -w --add-data=icon.ico;. --icon=icon.ico gui.py