spool &1
set timing on

with sales as (
 select *
 from store_sales, household_demographics , time_dim, store
 where ss_sold_time_sk = time_dim.t_time_sk   
     and ss_hdemo_sk = household_demographics.hd_demo_sk 
     and ss_store_sk = s_store_sk
     and ((household_demographics.hd_dep_count = 3 and household_demographics.hd_vehicle_count<=3+2) or
          (household_demographics.hd_dep_count = 0 and household_demographics.hd_vehicle_count<=0+2) or
          (household_demographics.hd_dep_count = 1 and household_demographics.hd_vehicle_count<=1+2)) 
     and store.s_store_name = 'ese')
select  *
from
  (select count(*) h8_30_to_9
  from sales
  where sales.t_hour = 8
     and sales.t_minute >= 30) s1,
  (select count(*) h9_to_9_30
  from sales
  where sales.t_hour = 9 
     and sales.t_minute < 30) s2,
  (select count(*) h9_30_to_10
  from sales
  where sales.t_hour = 9 
     and sales.t_minute >= 30) s3,
  (select count(*) h10_to_10_30
  from sales
  where sales.t_hour = 10 
     and sales.t_minute < 30) s4,
  (select count(*) h10_30_to_11
  from sales
  where sales.t_hour = 10 
     and sales.t_minute >= 30) s5,
  (select count(*) h11_to_11_30
  from sales
  where sales.t_hour = 11 
     and sales.t_minute < 30) s6,
  (select count(*) h11_30_to_12
  from sales
  where sales.t_hour = 11 
     and sales.t_minute >= 30) s7,
  (select count(*) h12_to_12_30
  from sales
  where sales.t_hour = 12 
     and sales.t_minute < 30) s8;

spool off
exit
