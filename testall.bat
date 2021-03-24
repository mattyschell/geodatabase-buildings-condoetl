REM No SDE file environmental it will be sloppily mocked to a file gdb
set PLUTOVERSION=21v1
set SDEFILE=X:\gis\connections\oracle19c\dev\GIS-XXXXXX\bldg.sde
set TOILER=X:\gis\geodatabase-toiler\
set PYTHONPATH=%PYTONPATH%;%TOILER%\src\py
CALL c:\Progra~1\ArcGIS\Pro\bin\Python\scripts\propy.bat test_condo.py 
CALL c:\Progra~1\ArcGIS\Pro\bin\Python\scripts\propy.bat test_pluto.py
REM this one requires scratch schema on an enterprise gdb target
CALL c:\Progra~1\ArcGIS\Pro\bin\Python\scripts\propy.bat test_condoloader.py