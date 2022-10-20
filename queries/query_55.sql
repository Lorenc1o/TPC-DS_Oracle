-- start query 82 in stream 0 using template query55.tpl
WHENEVER SQLERROR EXIT 1
SET LINES 32000
SET TERMOUT OFF ECHO OFF NEWP 0 SPA 0 PAGES 0 FEED OFF HEAD OFF TRIMS ON TAB OFF
SET SERVEROUTPUT OFF

spool &1
timing start t

select * from (select  i_brand_id brand_id, i_brand brand,
 	sum(ss_ext_sales_price) ext_price
 from date_dim, store_sales, item
 where d_date_sk = ss_sold_date_sk
 	and ss_item_sk = i_item_sk
 	and i_manager_id=20
 	and d_moy=12
 	and d_year=1998
 group by i_brand, i_brand_id
 order by ext_price desc, i_brand_id
 ) where rownum <= 100 ;

timing stop
spool off
exit
-- end query 82 in stream 0 using template query55.tpl
