-- start query 44 in stream 0 using template query92.tpl
WHENEVER SQLERROR EXIT 1
SET LINES 32000
SET TERMOUT OFF ECHO OFF NEWP 0 SPA 0 PAGES 0 FEED OFF HEAD OFF TRIMS ON TAB OFF
SET SERVEROUTPUT OFF

spool &1
timing start t

select * from (select  
   sum(ws_ext_discount_amt)  as "Excess Discount Amount" 
from 
    web_sales 
   ,item 
   ,date_dim
where
i_manufact_id = 914
and i_item_sk = ws_item_sk 
and d_date between to_date('2001-01-25', 'YYYY-MM-DD') and 
        (to_date('2001-01-25', 'YYYY-MM-DD') + 90)
and d_date_sk = ws_sold_date_sk 
and ws_ext_discount_amt  
     > ( 
         SELECT 
            1.3 * avg(ws_ext_discount_amt) 
         FROM 
            web_sales 
           ,date_dim
         WHERE 
              ws_item_sk = i_item_sk 
          and d_date between to_date('2001-01-25', 'YYYY-MM-DD') and
                             (to_date('2001-01-25', 'YYYY-MM-DD') + 90)
          and d_date_sk = ws_sold_date_sk 
      ) 
order by sum(ws_ext_discount_amt)
 ) where rownum <= 100;

timing stop
spool off
exit
-- end query 44 in stream 0 using template query92.tpl
