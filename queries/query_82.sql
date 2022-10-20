-- start query 67 in stream 0 using template query82.tpl
WHENEVER SQLERROR EXIT 1
SET LINES 32000
SET TERMOUT OFF ECHO OFF NEWP 0 SPA 0 PAGES 0 FEED OFF HEAD OFF TRIMS ON TAB OFF
SET SERVEROUTPUT OFF

spool &1
timing start t

select * from (select  i_item_id
       ,i_item_desc
       ,i_current_price
 from item, inventory, date_dim, store_sales
 where i_current_price between 69 and 69+30
 and inv_item_sk = i_item_sk
 and d_date_sk=inv_date_sk
 and d_date between to_date('1998-06-06', 'YYYY-MM-DD') and (to_date('1998-06-06', 'YYYY-MM-DD') +  60)
 and i_manufact_id in (105,513,180,137)
 and inv_quantity_on_hand between 100 and 500
 and ss_item_sk = i_item_sk
 group by i_item_id,i_item_desc,i_current_price
 order by i_item_id
  ) where rownum <= 100;

timing stop
spool off
exit
-- end query 67 in stream 0 using template query82.tpl
