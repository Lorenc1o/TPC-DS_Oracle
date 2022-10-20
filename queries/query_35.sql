-- start query 47 in stream 0 using template query35.tpl
WHENEVER SQLERROR EXIT 1
SET LINES 32000
SET TERMOUT OFF ECHO OFF NEWP 0 SPA 0 PAGES 0 FEED OFF HEAD OFF TRIMS ON TAB OFF
SET SERVEROUTPUT OFF

spool &1
timing start t

select * from (select   
  ca_state,
  cd_gender,
  cd_marital_status,
  cd_dep_count,
  count(*) cnt1,
  max(cd_dep_count) max1,
  stddev_samp(cd_dep_count) sum1,
  stddev_samp(cd_dep_count) max2,
  cd_dep_employed_count,
  count(*) cnt2,
  max(cd_dep_employed_count) max3,
  stddev_samp(cd_dep_employed_count) sum2,
  stddev_samp(cd_dep_employed_count) max4,
  cd_dep_college_count,
  count(*) cnt3,
  max(cd_dep_college_count) max5,
  stddev_samp(cd_dep_college_count) sum3,
  stddev_samp(cd_dep_college_count) max6
 from
  customer c,customer_address ca,customer_demographics
 where
  c.c_current_addr_sk = ca.ca_address_sk and
  cd_demo_sk = c.c_current_cdemo_sk and 
  exists (select *
          from store_sales,date_dim
          where c.c_customer_sk = ss_customer_sk and
                ss_sold_date_sk = d_date_sk and
                d_year = 2000 and
                d_qoy < 4) and
   (exists (select *
            from web_sales,date_dim
            where c.c_customer_sk = ws_bill_customer_sk and
                  ws_sold_date_sk = d_date_sk and
                  d_year = 2000 and
                  d_qoy < 4) or 
    exists (select * 
            from catalog_sales,date_dim
            where c.c_customer_sk = cs_ship_customer_sk and
                  cs_sold_date_sk = d_date_sk and
                  d_year = 2000 and
                  d_qoy < 4))
 group by ca_state,
          cd_gender,
          cd_marital_status,
          cd_dep_count,
          cd_dep_employed_count,
          cd_dep_college_count
 order by ca_state,
          cd_gender,
          cd_marital_status,
          cd_dep_count,
          cd_dep_employed_count,
          cd_dep_college_count
  ) where rownum <= 100;

timing stop
spool off
exit
-- end query 47 in stream 0 using template query35.tpl
