-- start query 65 in stream 0 using template query20.tpl
WHENEVER SQLERROR EXIT 1
SET LINES 32000
SET TERMOUT OFF ECHO OFF NEWP 0 SPA 0 PAGES 0 FEED OFF HEAD OFF TRIMS ON TAB OFF
SET SERVEROUTPUT OFF

spool &1
timing start t

select * from (select  i_item_id
       ,i_item_desc 
       ,i_category 
       ,i_class 
       ,i_current_price
       ,sum(cs_ext_sales_price) as itemrevenue 
       ,sum(cs_ext_sales_price)*100/sum(sum(cs_ext_sales_price)) over
           (partition by i_class) as revenueratio
 from	catalog_sales
     ,item 
     ,date_dim
 where cs_item_sk = i_item_sk 
   and i_category in ('Children', 'Sports', 'Music')
   and cs_sold_date_sk = d_date_sk
 and d_date between to_date('2002-04-01', 'YYYY-MM-DD') 
 				and (to_date('2002-04-01', 'YYYY-MM-DD') + 30)
 group by i_item_id
         ,i_item_desc 
         ,i_category
         ,i_class
         ,i_current_price
 order by i_category
         ,i_class
         ,i_item_id
         ,i_item_desc
         ,revenueratio
 ) where rownum <= 100;

timing stop
spool off
exit
-- end query 65 in stream 0 using template query20.tpl
