@echo off
mode con cols=100 lines=20
set PYPATH=C:\Python27;C:\Python27\Lib;C:\Python27\libs;C:\Python27\Tools\Scripts;
set path=%PYPATH%;%path%
set /p url_domain=please input domain eg:[cert.org.cn]
cls
start python main.py
pause

