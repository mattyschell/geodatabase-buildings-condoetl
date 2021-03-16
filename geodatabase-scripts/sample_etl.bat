set SDEFILE=XX:\GIS\Internal\Connections\oracle11g\stg\dof_readonly@geocstg.sde
set TARGETBLDGSDE=XX:\GIS\Internal\Connections\oracle19c\dev\GIS-ditGSdv1\bldg.sde
set PLUTOVERSION=21v1
set NOTIFY=xxxx@yyyy.zzzz.gov
set NOTIFYFROM=aaaa@bbbb.cccc.gov
set SMTPFROM=foo.bar
set TARGETLOGDIR=C:\Temp\logpile\
set BATLOG=%TARGETLOGDIR%geodatabase-buildings-condoetl.log
set ETL=C:\matt_projects\geodatabase-buildings-condoetl\
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
REM SET SDEFILE=%TARGETBLDGSDE%
REM loadcondo.py goes here
%PROPY% %ETL%notify.py ": Successfully loaded condo table in %SDEFILE%" %NOTIFY% "geodatabase-buildings-condoetl"
