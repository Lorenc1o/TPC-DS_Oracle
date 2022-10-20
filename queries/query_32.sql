-- start query 7 in stream 0 using template query32.tpl
WHENEVER SQLERROR EXIT 1
SET LINES 32000
SET TERMOUT OFF ECHO OFF NEWP 0 SPA 0 PAGES 0 FEED OFF HEAD OFF TRIMS ON TAB OFF
SET SERVEROUTPUT OFF

spool &1
timing start t

select * from (select  sum(cs_ext_discount_amt)  as "excess discount amount" 
from 
   catalog_sales 
   ,item 
   ,date_dim
where
i_manufact_id = 283
and i_item_sk = cs_item_sk 
and d_date between to_date('1999-02-22', 'YYYY-MM-DD') and 
        (to_date('1999-02-22', 'YYYY-MM-DD') + 90)
and d_date_sk = cs_sold_date_sk 
and cs_ext_discount_amt  
     > ( 
         select 
            1.3 * avg(cs_ext_discount_amt) 
         from 
            catalog_sales 
           ,date_dim
         where 
              cs_item_sk = i_item_sk 
          and d_date between to_date('1999-02-22', 'YYYY-MM-DD') and 
                             (to_date('1999-02-22', 'YYYY-MM-DD') + 90)
          and d_date_sk = cs_sold_date_sk 
      ) 
 ) where rownum <= 100;

timing stop
spool off
exit
-- end query 7 in stream 0 using template query32.tpl
