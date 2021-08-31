REM I dunno are these sensitive?
set HTTP_PROXY=http://xxpxyxx.nycnet:xxxx
set HTTPS_PROXY=http://xxpxyxx.nycnet:xxxx
REM update the first 3
set PLUTOVERSION=21v2
set DATABASE=DITGSDV1
set ENV=DEV
REM unmask the next 4
set NOTIFY=xxxx@xxxxx.nyc.gov,xxxx@xxxxx.nyc.gov
set NOTIFYFROM=xxx-xxxxxxx@xxxxx.nyc.gov
set SMTPFROM=xxxxxxxxx.xxxxxx
set BASEPATH=C:\xxx\
REM review the rest
REM dof_taxmap@geocdev is in bad shape, we must use staging here in dev to get anything
set SDEFILE=%BASEPATH%connections\oracle11g\%ENV%\dof_readonly.sde
set TARGETSDEFILE=%BASEPATH%connections\oracle19c\%ENV%\GIS-%DATABASE%\bldg.sde
set TOILER=%BASEPATH%geodatabase-toiler\
set PYTHONPATH=%PYTHONPATH%;%TOILER%\src\py
set TARGETLOGDIR=%BASEPATH%\geodatabase-scripts\logs\condoetl\
set BATLOG=%TARGETLOGDIR%geodatabase-buildings-condoetl.log
set ETL=%BASEPATH%geodatabase-buildings-condoetl\
set PROPY=c:\Progra~1\ArcGIS\Pro\bin\Python\envs\arcgispro-py3\python.exe
echo starting refresh of condo table in %TARGETSDEFILE% on %date% at %time% > %BATLOG%
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
