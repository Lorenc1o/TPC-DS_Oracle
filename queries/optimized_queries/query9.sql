spool &1
set timing on

with ss_bucket_1 as 
 (select *
 from store_sales
 where ss_quantity between 1 and 20),
ss_bucket_2 as 
 (select *
 from store_sales
 where ss_quantity between 21 and 40),
ss_bucket_3 as 
 (select *
 from store_sales
 where ss_quantity between 41 and 60),
ss_bucket_4 as 
 (select *
 from store_sales
 where ss_quantity between 61 and 80),
ss_bucket_5 as 
 (select *
 from store_sales
 where ss_quantity between 81 and 100)
select case when (select count(*) from ss_bucket_1) > 25437
            then (select avg(ss_ext_discount_amt) from ss_bucket_1)
            else (select avg(ss_net_profit) from ss_bucket_1) end bucket1,
        case when (select count(*) from ss_bucket_2) > 22746
            then (select avg(ss_ext_discount_amt) from ss_bucket_2)
            else (select avg(ss_net_profit) from ss_bucket_2) end bucket2,
        case when (select count(*) from ss_bucket_3) > 9387
            then (select avg(ss_ext_discount_amt) from ss_bucket_3)
            else (select avg(ss_net_profit) from ss_bucket_3) end bucket3,
        case when (select count(*) from ss_bucket_4) > 10098
            then (select avg(ss_ext_discount_amt) from ss_bucket_4)
            else (select avg(ss_net_profit) from ss_bucket_4) end bucket4,
        case when (select count(*) from ss_bucket_5) > 18213
            then (select avg(ss_ext_discount_amt) from ss_bucket_5)
            else (select avg(ss_net_profit) from ss_bucket_5) end bucket5
from reason
where r_reason_sk = 1;

spool off
exit
