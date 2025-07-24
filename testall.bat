set PLUTOVERSION=25v2
set BASEPATH=C:\xxx\
set DATABASE=xxxx
REM HTTP_PROXY=http://domain\account:password@proxy.xxx:port
REM set HTTP_PROXY=%HTTP_PROXY%
REM SDEFILE for condoloader target only, use a mock file gdb for inputs 
set SDEFILE=%BASEPATH%connections\oracle19c\dev\GIS-%DATABASE%\bldg.sde
set TOILER=%BASEPATH%geodatabase-toiler\
set PYTHONPATH=%PYTHONPATH%;%TOILER%\src\py
REM set PROPY=c:\Progra~1\ArcGIS\Pro\bin\Python\envs\arcgispro-py3\python.exe
set PROPY=C:\Users\%USERNAME%\AppData\Local\Programs\ArcGIS\Pro\bin\Python\envs\arcgispro-py3\python.exe
CALL %PROPY% test_condo.py 
CALL %PROPY% test_pluto.py
CALL %PROPY% test_condoloader.py
