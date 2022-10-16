# TPC-DS_Oracle
Repository for development of the first project of the course DATA WAREHOUSES (INFO-H-419) from the program BDMA, Fall 2022.

Development of a TPC-DS Benchmark in Oracle with several scale factors.

Group members:
- [Ivanović, Nikola](https://github.com/ivanovicnikola)
- [Lorencio Abril, Jose Antonio](https://github.com/Lorenc1o)
- [Yusupov, Sayyor](https://github.com/SYusupov)
- [Živković, Bogdana](https://github.com/zivkovicbogdana)

Professor: Zimányi, Esteban

## Base steps
  1. Download [TPC-DS Tools](https://www.tpc.org/tpc_documents_current_versions/current_specifications5.asp) or the [TPC-DS Kit](https://github.com/gregrahn/tpcds-kit) which solves some common errors.
  2. Build Tools as described in 'tools\How_To_Guide-DS-V2.0.0.docx'.
  3. Create DB.
  4. Take the DB schema described in tpcds.sql and tpcds_ri.sql (they are located in the 'tools' folder).
  5. Generate data to be stored to the database.
  
    # Windows
    dsdgen.exe /scale 1 /dir .\tmp
    
    # Linux
    dsdgen -scale 1 -dir /tmp
    
  6. Upload data to DB using Oracle SQL Loader. Control files can be found here in the ctl folder.

    sqlldr userid=username/password@SID control='item.ctl'
    
  7. Generate queries. The following command can be used to generate all 99 queries in numerical order (/qualify) for the 1GB scale factor (/scale) using the Oracle    dialect template (/dialect) with the output going to ../queries/query_0.sql (/output_dir). If you are using the official TPC-DS Tools the 'query_templates\oracle.tpl' file needs to be replaced with the one provided here.
  
    #Windows
    dsqgen /directory ../query_templates /input ../query_templates/templates.lst /verbose y /qualify y /scale 1 /dialect oracle /output_dir ../queries
    
    # Linux
    ./dsqgen -directory ../query_templates -input ../query_templates/templates.lst -verbose y -qualify y -scale 1 -dialect oracle -output_dir ../queries
    
  8. Put each query to a separate file and set preferences for execution time recording and saving the results by running:
    ```python separate_queries ../queries```
    Run an individual query with the bash script:
    ```sh execute_query.sh ../queries/query_1.sql```
