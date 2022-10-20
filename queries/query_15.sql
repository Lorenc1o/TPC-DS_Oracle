-- start query 57 in stream 0 using template query15.tpl
WHENEVER SQLERROR EXIT 1
SET LINES 32000
SET TERMOUT OFF ECHO OFF NEWP 0 SPA 0 PAGES 0 FEED OFF HEAD OFF TRIMS ON TAB OFF
SET SERVEROUTPUT OFF

spool &1
timing start t

select * from (select  ca_zip
       ,sum(cs_sales_price)
 from catalog_sales
     ,customer
     ,customer_address
     ,date_dim
 where cs_bill_customer_sk = c_customer_sk
 	and c_current_addr_sk = ca_address_sk 
 	and ( substr(ca_zip,1,5) in ('85669', '86197','88274','83405','86475',
                                   '85392', '85460', '80348', '81792')
 	      or ca_state in ('CA','WA','GA')
 	      or cs_sales_price > 500)
 	and cs_sold_date_sk = d_date_sk
 	and d_qoy = 2 and d_year = 2002
 group by ca_zip
 order by ca_zip
  ) where rownum <= 100;

timing stop
spool off
exit
-- end query 57 in stream 0 using template query15.tpl
