set PLUTOVERSION=21v2
set BASEPATH=C:\xxx\
set DATABASE=XXXXXXX1
REM SDEFILE for condoloader target only, use a mock file gdb for inputs 
set SDEFILE=%BASEPATH%connections\oracle19c\dev\GIS-%DATABASE%\bldg.sde
set TOILER=%BASEPATH%geodatabase-toiler\
set PYTHONPATH=%PYTONPATH%;%TOILER%\src\py
CALL c:\Progra~1\ArcGIS\Pro\bin\Python\scripts\propy.bat test_condo.py 
CALL c:\Progra~1\ArcGIS\Pro\bin\Python\scripts\propy.bat test_pluto.py
CALL c:\Progra~1\ArcGIS\Pro\bin\Python\scripts\propy.bat test_condoloader.py