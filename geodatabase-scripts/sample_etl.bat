REM update the first 3
set PLUTOVERSION=21v1
set DATABASE=XXXXXXXX
set ENV=XXX
REM unmask the next 4
set NOTIFY=xxxxxxx@xxxxx.xxx.xxx
set NOTIFYFROM=xxxxxxx@xxxxx.xxx.xxx
set SMTPFROM=xxxxxxxxx.xxxxxx
set BASEPATH=X:\gis\
REM review the rest
set SDEFILE=%BASEPATH%connections\oracle11g\%ENV%\dof_readonly.sde
set TARGETSDEFILE=%BASEPATH%connections\oracle19c\%ENV%\GIS-%DATABASE%\bldg.sde
set TOILER=%BASEPATH%geodatabase-toiler\
set PYTHONPATH=%PYTONPATH%;%TOILER%\src\py
set TARGETLOGDIR=%BASEPATH%\geodatabase-scripts\logs\condoetl\
set BATLOG=%TARGETLOGDIR%geodatabase-buildings-condoetl.log
set ETL=%BASEPATH%geodatabase-buildings-condoetl\
set PROPY=c:\Progra~1\ArcGIS\Pro\bin\Python\envs\arcgispro-py3\python.exe
echo starting refresh of condo table in %SDEFILE% on %date% at %time% > %BATLOG%
%PROPY% %ETL%extractcondo.py && (
  echo extracted DOF condos from %SDEFILE% on %date% at %time% >> %BATLOG%
) || (
  %PROPY% %ETL%notify.py ": Failed to extract DOF condos from %SDEFILE%" %NOTIFY% "extractcondo" && EXIT /B 1
)  
%PROPY% %ETL%extractpluto.py && (
  echo extracted pluto condos from %PLUTOVERSION% on %date% at %time% >> %BATLOG%
) || (
  %PROPY% %ETL%notify.py ": Failed to extract pluto condos from %PLUTOVERSION%" %NOTIFY% "extractpluto" && EXIT /B 1
) 
SET SDEFILE=%TARGETSDEFILE%
%PROPY% %ETL%loadcondo.py && (
  %PROPY% %ETL%notify.py ": Successfully loaded condos to %SDEFILE%" %NOTIFY% "loadcondo"
) || (
  %PROPY% %ETL%notify.py ": Failed to load condos to %SDEFILE%" %NOTIFY% "loadcondo" && EXIT /B 1
) 
echo loaded condos to %SDEFILE% on %date% at %time% >> %BATLOG%
