# geodatabase-buildings-condoetl

Refreshes the condo dataset in [geodatabase-buildings](https://github.com/mattyschell/geodatabase-buildings) using inputs from the NYC Dept. of Finance [Property Information Portal](https://propertyinformationportal.nyc.gov/) and NYC Dept. of City Planning [PLUTO](https://github.com/NYCPlanning/db-pluto). 
Friends, this our condo dataset refresh using two agency inputs, our rules, the trick is never to be afraid.

We will refresh the NYC Office of Technology and Innovation condo dataset with each PLUTO release from the Dept. of City Planning, matching PLUTO to current Dept. of Finance Condos. We update OTI's live buildings with all condominium "billing" boro/block/lots daily, so OTI's buildings will always reflect the latest legal MapPLUTO values. 

## Inputs and Dependencies

* Access to the Department of Finance hosted feature table CONDO
* SDE file connection to the target [geodatabase-buildings](https://github.com/mattyschell/geodatabase-buildings) 
* [ESRI ArcGIS Pro python 3.x](https://pro.arcgis.com/en/pro-app/arcpy/get-started/installing-python-for-arcgis-pro.htm) 
* [Geodatabase Toiler](https://github.com/mattyschell/geodatabase-toiler) repository
* Internet access to the Department of City Planning downloads page like:
    * https://www1.nyc.gov/assets/planning/download/zip/data-maps/open-data/nyc_pluto_YYvX_csv.zip


## Full ETL

Update the variables at the beginning of geodatabase-scripts\sample_etl.bat and execute it.  See below for a breakdown of individual steps.

```
> \geodatabase-scripts\sample_etl.bat
```

## Tests

This is a poorly designed combination of integration tests and regression tests. You probably only want to run this if you have all of the usual licensing, connection files, and data available. 

Update the variables at the beginning of the batch file.


```
> REM Test teardown will drop tables so do not run this anywhere important
> testall.bat
```

## First time schema setup

Execute sql_oracle\definition\schema.sql in the target schema.  For example, sqlplus-ified:

```
sqlplus bldg/ILuvEsri247@database @sql_oracle\definition\initschema.sql
```

## 1. Extract Taxmap Base BBL, Condo Billing BBLs

The source Dept. of Finance data may move so this step must be loosely coupled.

```
> set SDEFILE=https://services6.arcgis.com/yG5s3afENB5iO9fj/arcgis/rest/services/v_PIP_SCAR_Tables_view/FeatureServer/
> set TARGETLOGDIR=X:\xxx\geodatabase-scripts\logs\condoetl
> c:\Progra~1\ArcGIS\Pro\bin\Python\scripts\propy.bat extractcondo.py
```
Output: condo.csv

## 2. Extract PLUTO Condo BBLs

Assumes that [PLUTO](https://github.com/NYCPlanning/db-pluto) will be available as a comma-separated file at a URL that we can retrieve.

```
> set PLUTOVERSION=21v2
> set TARGETLOGDIR=X:\gis\geodatabase-scripts\logs\condoetl
> c:\Progra~1\ArcGIS\Pro\bin\Python\scripts\propy.bat extractpluto.py
```
Output: plutocondo.sql

## 3. Finalize BBL List and Load to Geodatabase Buildings Schema

Refresh the database condo table with Dept. of Finance condos that also exist in PLUTO. Requires a target schema and utilites in [geodatabase-toiler](https://github.com/mattyschell/geodatabase-toiler).

```
> set SDEFILE=X:\gis\connections\xx\xxx.sde
> set TOILER=X:\gis\geodatabase-toiler\
> set PYTHONPATH=%PYTONPATH%;%TOILER%\src\py
> c:\Progra~1\ArcGIS\Pro\bin\Python\scripts\propy.bat loadcondo.py
```
Output: Database table "condo"

