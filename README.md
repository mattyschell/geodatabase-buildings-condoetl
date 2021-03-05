# geodatabase-buildings-condoetl

Refreshes the condo dataset in [geodatabase-buildings](https://github.com/mattyschell/geodatabase-buildings) 
using inputs from the NYC Dept. of Finance [Digital Tax Map](http://gis.nyc.gov/taxmap/map.htm)
and NYC Dept. of City Planning [PLUTO](https://github.com/NYCPlanning/db-pluto). 
Friends, this our condo dataset refresh using two agency inputs, our rules, the 
trick is never to be afraid.

We will refresh the DoITT condo dataset once a month with each PLUTO release. We
update buildings with mappluto_bbls every day, so DoITT buildings will always 
reflect the latest legal PLUTO values. 

## Inputs and Dependencies

* SDE file connection to the source DOF_READONLY oracle schema
* SDE file connection to the target [geodatabase-buildings](https://github.com/mattyschell/geodatabase-buildings) 
* [ESRI ArcGIS Pro python 3.x](https://pro.arcgis.com/en/pro-app/arcpy/get-started/installing-python-for-arcgis-pro.htm) 
* Internet access to the Department of City Planning downloads page like:
    * https://www1.nyc.gov/assets/planning/download/zip/data-maps/open-data/nyc_pluto_YYvX_csv.zip


## Full ETL

Update the variables at the beginning of geodatabase-scripts\sample_etl.bat and
execute it.

```
> \geodatabase-scripts\sample_etl.bat
```

### 1. Extract Taxmap Base BBL, Condo Billing BBLs

```
> set SDEFILE=T:\GIS\Internal\Connections\oracle11g\dev\dof_readonly.sde
> set PYTHONPATH=C:\geodatabase-toiler\src\py
> c:\Progra~1\ArcGIS\Pro\bin\Python\scripts\propy.bat extractcondo.py
```

### 2. Extract PLUTO Condo BBLs

```
> c:\Progra~1\ArcGIS\Pro\bin\Python\scripts\propy.bat extractpluto.py 21V1
```

### 3. Finalize BBL List and Load to Geodatabase Buildings Schema

```
> set SDEFILE=T:\GIS\Internal\Connections\oracle19c\dev\GIS-ditGSdv1\bldg.sde
> set PYTHONPATH=C:\geodatabase-toiler\src\py
> c:\Progra~1\ArcGIS\Pro\bin\Python\scripts\propy.bat loadcondo.py
```
