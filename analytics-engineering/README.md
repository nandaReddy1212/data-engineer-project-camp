## analyses

 -  A Place for SQL files for data quality checks

## dbt_project.yml
    - The most important file in dbt where you have project name and profile name and variables and project-wide defaults.

## macros
 -  They are reusable logic mostly SQL.  ex: datatime conversion 

## models
    - 
## seeds
    - A place to upload csv and flat files for testing of data before loading into data warehouse.

## snapsheets
    -  snapshot takes a "picture" of a table at a point in time. Each time you run it,
  if a value has changed, a new row is recorded with a timestamp — without overwriting the previous value.

## tests
    - place for singular tests written as SQL assertions and if it returns more than zero rows then dbt build fails. it is good for custom 
        business rules.

