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
  1. Download [TPC-DS Tools](https://www.tpc.org/tpc_documents_current_versions/current_specifications5.asp).
  2. Build Tools as described in 'tools\How_To_Guide-DS-V2.0.0.docx'.
  3. Create DB.
  4. Take the DB schema described in tpcds.sql and tpcds_ri.sql (they are located in the 'tools' - folder).
  5. Generate data to be stored to the database.
  
    # Windows
    dsdgen.exe /scale 1 /dir .\tmp
    
    # Linux
    dsdgen -scale 1 -dir /tmp
    
  6. Upload data to DB using Oracle SQL Loader. Control files can be found here in the ctl folder.

    sqlldr userid=username/password@SID control='item.ctl'
