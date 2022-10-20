-- start query 14 in stream 0 using template query21.tpl
WHENEVER SQLERROR EXIT 1
SET LINES 32000
SET TERMOUT OFF ECHO OFF NEWP 0 SPA 0 PAGES 0 FEED OFF HEAD OFF TRIMS ON TAB OFF
SET SERVEROUTPUT OFF

spool &1
timing start t

select * from (select  *
 from(select w_warehouse_name
            ,i_item_id
            ,sum(case when (to_date(d_date) < to_date('2000-05-19', 'YYYY-MM-DD'))
	                then inv_quantity_on_hand 
                      else 0 end) as inv_before
            ,sum(case when (to_date(d_date) >= to_date('2000-05-19', 'YYYY-MM-DD'))
                      then inv_quantity_on_hand 
                      else 0 end) as inv_after
   from inventory
       ,warehouse
       ,item
       ,date_dim
   where i_current_price between 0.99 and 1.49
     and i_item_sk          = inv_item_sk
     and inv_warehouse_sk   = w_warehouse_sk
     and inv_date_sk    = d_date_sk
     and d_date between (to_date('2000-05-19', 'YYYY-MM-DD') - 30)
                    and (to_date('2000-05-19', 'YYYY-MM-DD') + 30)
   group by w_warehouse_name, i_item_id) x
 where (case when inv_before > 0 
             then inv_after / inv_before 
             else null
             end) between 2.0/3.0 and 3.0/2.0
 order by w_warehouse_name
         ,i_item_id
  ) where rownum <= 100;

timing stop
spool off
exit
-- end query 14 in stream 0 using template query21.tpl
