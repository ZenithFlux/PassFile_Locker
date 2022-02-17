@echo off
pyinstaller -w --add-data=icon.ico;. --icon=icon.ico --name=passfile gui.py