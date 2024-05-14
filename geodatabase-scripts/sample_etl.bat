set HTTP_PROXY=http://domain\user:pass@XXXXX.xxxxxx:1234
set HTTPS_PROXY=%HTTP_PROXY%
REM update the first 3
set PLUTOVERSION=24v1_1
set DATABASE=XXXXXXXX1
set ENV=DEV
REM unmask the next 4
set NOTIFY=xxxx@xxxxx.nyc.gov
set NOTIFYFROM=xxxxxx@xxxxx.nyc.gov
set SMTPFROM=xxxxxxxxxx.nycnet
set BASEPATH=C:\xxxx\
REM review the rest
REM more like SDE CONTAINAH am I right?
set SDEFILE=https://services6.arcgis.com/yG5s3afENB5iO9fj/arcgis/rest/services/Digital_Tax_Map_VIEW/FeatureServer/
set HOSTEDLAYER=7
set TARGETSDEFILE=%BASEPATH%connections\oracle19c\%ENV%\GIS-%DATABASE%\bldg.sde
set TOILER=%BASEPATH%geodatabase-toiler\
set PYTHONPATH=%PYTHONPATH%;%TOILER%\src\py
set TARGETLOGDIR=%BASEPATH%\geodatabase-scripts\logs\condoetl\
set BATLOG=%TARGETLOGDIR%geodatabase-buildings-condoetl.log
set ETL=%BASEPATH%geodatabase-buildings-condoetl\
set PROPY=c:\Progra~1\ArcGIS\Pro\bin\Python\envs\arcgispro-py3\python.exe
echo starting refresh of condo table in %TARGETSDEFILE% on %date% at %time% > %BATLOG%
%PROPY% %ETL%extractcondo.py %HOSTEDLAYER% && (
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
