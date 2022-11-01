# TPC-DS_Oracle
Repository for development of the first project of the course DATA WAREHOUSES (INFO-H-419) from the program BDMA, Fall 2022.

Development of a TPC-DS Benchmark in Oracle with several scale factors.

Group members:
- [Ivanović, Nikola](https://github.com/ivanovicnikola)
- [Lorencio Abril, Jose Antonio](https://github.com/Lorenc1o)
- [Yusupov, Sayyor](https://github.com/SYusupov)
- [Živković, Bogdana](https://github.com/zivkovicbogdana)

Professor: Zimányi, Esteban

## Structure of the repo

### TPC-DS_Oracle_Report.pdf
This file is the report of the project, where all the details and information about the project and this repository can be found.

### Folder queries
In this folder you will find the generated queries for Oracle in **original_queries**, the optimized versions of them in **optimized_queries** and some queries that we tried to optimize but couldn't can be found in **unsuccessful_queries**.

In **oracle_templates** are located the templates for the queries.

### Folder scripts
In this folder the scripts you will find the python scripts that we have developed to perform the different tests. In **side_files** there are files that are needed for the execution of the scripts, such as the tpcds.sql file, that creates the schema of the database.

In **utils** there are scripts that are useful for us, but not a strict part of the TPC-DS tests. For example, there are functions to generate the queries, to separate them in different files or to generate graphs from data.

In **test** is where the important scripts are located:

- Load_test: this script performs the Load Test of the TPC-DS benchmark.

- Power_test: this script performs the Power Test of the TPC-DS benchmark. That is, it executes all the queries and measures the elapsed time for each of them, as well as for the whole process. It can be also used to execute individual queries and obtain its execution time if wanted.

- Throughput_test: this script performs the Throughput Test of the TPC-DS benchmark. 

### Folder results
In this folder we dump the output of the different tests for further analysis.

## Base steps
  1. Download [TPC-DS Tools](https://www.tpc.org/tpc_documents_current_versions/current_specifications5.asp) or the [TPC-DS Kit](https://github.com/gregrahn/tpcds-kit) which solves some common errors.
  2. Build Tools as described in 'tools\How_To_Guide-DS-V2.0.0.docx'.
  3. Create DB.
  4. Take the DB schema described in tpcds.sql and tpcds_ri.sql (they are located in the 'side_files' folder). Do not run tpcds_ri.sql until the data has been loaded.
  5. Generate data to be stored to the database.
  
    # Windows
    dsdgen.exe /scale 1 /dir .\tmp
    
    # Linux
    dsdgen -scale 1 -dir /tmp
    
  6. Execute the Load Test. The load test uses Oracle SQL Loader to load the data using multiple processor cores. Control files can be found in the scripts/side_files/ctl folder.
  
    python3 Load_test.py -S [server] -D [database] -U [username] -P [password] -L [data directory] -C [ctl directory] -O [output file]

Or it can be done manually:

    sqlldr userid=username/password@SID control='item.ctl'
    
  7. Generate queries. The following command can be used to generate all 99 queries in numerical order. We suggest using the modified templates located in the queries/oracle_templates folder because they fix numerous occuring syntax errors.
  
    # Windows
    dsqgen /directory [path to oracle_templates] /input [path to query_templates] /templates.lst /verbose y /qualify y /scale 1 /dialect oracle /output_dir [output directory (original_queries in our case)]
    
    # Linux
    ./dsqgen -directory [path to oracle_templates] -input [path to query_templates] -templates.lst -verbose y -qualify y -scale 1 -dialect oracle /output_dir [output directory (original_queries in our case)]
    
  8. Put each query to a separate file and set preferences for execution time recording and saving the results. The separate_queries.py script is located in the scripts/utils folder.
  
    python3 separate_queries.py [path to queries]
    
Run all queries with the execute_queries.py script located in the scripts/test folder. Generated queries used for testing can be found in the queries/original_queries and queries/optimized_queries folders.

    python3 execute_queries.py -S [server] -D [database] -U [username] -P [password] -L [query directory] -C [ctl directory] -O [output file]
    
  9. Execute the Power Test. The query stream containing optimized queries is located in the queries/power_test_stream folder.
  
    python3 Power_test.py -S [server] -D [database] -U [username] -P [password] -Q [path to queries] /query_0.sql -O [output file]
  
  10. Execute the throughput test. To be able to perform the throughput test you need to generate 4 query streams using the dsqgen or use the 4 query streams provided in the queries/throughput_test_streams folder that contain optimized versions of the queries. Then, run the throughput_test.py script.
  
    python3 throughput_test.py -S [server] -D [database] -U [username] -P [password] -L [path to queries] -O [output file]
