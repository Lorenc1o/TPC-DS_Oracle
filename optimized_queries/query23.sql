spool &1
timing start t

with cs_ws_union_all as 
 (select cs_quantity quantity, cs_list_price list_price, cs_sold_date_sk sold_date_sk, cs_item_sk item_sk, cs_bill_customer_sk bill_customer_sk
 from catalog_sales
 union all
 select ws_quantity quantity, ws_list_price list_price, ws_sold_date_sk sold_date_sk, ws_item_sk item_sk, ws_bill_customer_sk bill_customer_sk
 from web_sales),
frequent_ss_items as 
 (select substr(i_item_desc,1,30) itemdesc,i_item_sk item_sk,d_date solddate,count(*) cnt
  from store_sales
      ,date_dim 
      ,item
  where ss_sold_date_sk = d_date_sk
    and ss_item_sk = i_item_sk 
    and d_year in (1999,1999+1,1999+2,1999+3)
  group by substr(i_item_desc,1,30),i_item_sk,d_date
  having count(*) >4),
 max_store_sales as
 (select max(csales) tpcds_cmax 
  from (select c_customer_sk,sum(ss_quantity*ss_sales_price) csales
        from store_sales
            ,customer
            ,date_dim 
        where ss_customer_sk = c_customer_sk
         and ss_sold_date_sk = d_date_sk
         and d_year in (1999,1999+1,1999+2,1999+3) 
        group by c_customer_sk)),
 best_ss_customer as
 (select c_customer_sk,sum(ss_quantity*ss_sales_price) ssales
  from store_sales
      ,customer
  where ss_customer_sk = c_customer_sk
  group by c_customer_sk
  having sum(ss_quantity*ss_sales_price) > (95/100.0) * (select
  *
from
 max_store_sales))
 select * from ( select  sum(sales)
 from (select quantity*list_price sales
       from cs_ws_union_all
           ,date_dim 
       where d_year = 1999 
         and d_moy = 1 
         and sold_date_sk = d_date_sk 
         and item_sk in (select item_sk from frequent_ss_items)
         and bill_customer_sk in (select c_customer_sk from best_ss_customer))
  ) where rownum <= 100;
  
with cs_ws_union_all as 
 (select cs_quantity quantity, cs_list_price list_price, cs_sold_date_sk sold_date_sk, cs_item_sk item_sk, cs_bill_customer_sk bill_customer_sk
 from catalog_sales
 union all
 select ws_quantity quantity, ws_list_price list_price, ws_sold_date_sk sold_date_sk, ws_item_sk item_sk, ws_bill_customer_sk bill_customer_sk
 from web_sales),
frequent_ss_items as
 (select substr(i_item_desc,1,30) itemdesc,i_item_sk item_sk,d_date solddate,count(*) cnt
  from store_sales
      ,date_dim
      ,item
  where ss_sold_date_sk = d_date_sk
    and ss_item_sk = i_item_sk
    and d_year in (1999,1999 + 1,1999 + 2,1999 + 3)
  group by substr(i_item_desc,1,30),i_item_sk,d_date
  having count(*) >4),
 max_store_sales as
 (select max(csales) tpcds_cmax
  from (select c_customer_sk,sum(ss_quantity*ss_sales_price) csales
        from store_sales
            ,customer
            ,date_dim 
        where ss_customer_sk = c_customer_sk
         and ss_sold_date_sk = d_date_sk
         and d_year in (1999,1999+1,1999+2,1999+3)
        group by c_customer_sk)),
 best_ss_customer as
 (select c_customer_sk,sum(ss_quantity*ss_sales_price) ssales
  from store_sales
      ,customer
  where ss_customer_sk = c_customer_sk
  group by c_customer_sk
  having sum(ss_quantity*ss_sales_price) > (95/100.0) * (select
  *
 from max_store_sales))
 select * from ( select  c_last_name,c_first_name,sales
 from (select c_last_name,c_first_name,sum(quantity*list_price) sales
        from cs_ws_union_all
            ,customer
            ,date_dim 
        where d_year = 1999 
         and d_moy = 1 
         and sold_date_sk = d_date_sk 
         and item_sk in (select item_sk from frequent_ss_items)
         and bill_customer_sk in (select c_customer_sk from best_ss_customer)
         and bill_customer_sk = c_customer_sk 
       group by c_last_name,c_first_name) 
     order by c_last_name,c_first_name,sales
   ) where rownum <= 100;

timing stop
spool off
exit
