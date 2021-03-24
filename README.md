# geodatabase-buildings-condoetl

Refreshes the condo dataset in [geodatabase-buildings](https://github.com/mattyschell/geodatabase-buildings) 
using inputs from the NYC Dept. of Finance [Digital Tax Map](http://gis.nyc.gov/taxmap/map.htm)
and NYC Dept. of City Planning [PLUTO](https://github.com/NYCPlanning/db-pluto). 
Friends, this our condo dataset refresh using two agency inputs, our rules, the 
trick is never to be afraid.

We will refresh the DoITT condo dataset with each PLUTO release from the Dept.
of City Planning, matching PLUTO to current Dept. of Finance Condos. We
update DoITT's live buildings with all condominium "billing" boro/block/lots 
daily, so DoITT buildings will always reflect the latest legal MapPLUTO values. 

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

The source Dept. of Finance data may move, so this step is remain loosely coupled.

```
> set SDEFILE=X:\gis\connections\oracle11g\dev\dof_readonly.sde
> set TARGETLOGDIR=X:\gis\geodatabase-scripts\logs\condoetl
> c:\Progra~1\ArcGIS\Pro\bin\Python\scripts\propy.bat extractcondo.py
```

### 2. Extract PLUTO Condo BBLs

Assumes that PLUTO will be available as a comma-separated file at a URL that we can retrieve.

```
> set PLUTOVERSION=21v1
> set TARGETLOGDIR=X:\gis\geodatabase-scripts\logs\condoetl
> c:\Progra~1\ArcGIS\Pro\bin\Python\scripts\propy.bat extractpluto.py
```

### 3. Finalize BBL List and Load to Geodatabase Buildings Schema

Refresh the DoITT condo table with Dept. of Finance condos that also exist in PLUTO. Requires a target schema and the [geodatabase-toiler](https://github.com/mattyschell/geodatabase-toiler) utilities.

```
> set SDEFILE=X:\gis\connections\xx\xxx.sde
> set TOILER=X:\gis\geodatabase-toiler\
> set PYTHONPATH=%PYTONPATH%;%TOILER%\src\py
> c:\Progra~1\ArcGIS\Pro\bin\Python\scripts\propy.bat loadcondo.py
```
