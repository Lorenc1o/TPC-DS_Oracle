-- start query 31 in stream 0 using template query37.tpl
WHENEVER SQLERROR EXIT 1
SET LINES 32000
SET TERMOUT OFF ECHO OFF NEWP 0 SPA 0 PAGES 0 FEED OFF HEAD OFF TRIMS ON TAB OFF
SET SERVEROUTPUT OFF

spool &1
timing start t

select * from (select  i_item_id
       ,i_item_desc
       ,i_current_price
 from item, inventory, date_dim, catalog_sales
 where i_current_price between 26 and 26 + 30
 and inv_item_sk = i_item_sk
 and d_date_sk=inv_date_sk
 and d_date between to_date('2001-06-09', 'YYYY-MM-DD') and (to_date('2001-06-09', 'YYYY-MM-DD') +  60)
 and i_manufact_id in (744,884,722,693)
 and inv_quantity_on_hand between 100 and 500
 and cs_item_sk = i_item_sk
 group by i_item_id,i_item_desc,i_current_price
 order by i_item_id
  ) where rownum <= 100;

timing stop
spool off
exit
-- end query 31 in stream 0 using template query37.tpl
