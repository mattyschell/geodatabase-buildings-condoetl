set PLUTOVERSION=21v1
set BASEPATH=C:\gis\
set DATABASE=DITGSDV1
set SDEFILE=%BASEPATH%connections\oracle19c\dev\GIS-%DATABASE%\bldg.sde
set TOILER=%BASEPATH%geodatabase-toiler\
set PYTHONPATH=%PYTONPATH%;%TOILER%\src\py
CALL c:\Progra~1\ArcGIS\Pro\bin\Python\scripts\propy.bat test_condo.py 
CALL c:\Progra~1\ArcGIS\Pro\bin\Python\scripts\propy.bat test_pluto.py
CALL c:\Progra~1\ArcGIS\Pro\bin\Python\scripts\propy.bat test_condoloader.py