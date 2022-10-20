spool &1
timing start t

select * from (select  sum(cs_ext_discount_amt)  as "excess discount amount" 
from 
   catalog_sales 
   ,item 
   ,date_dim
where
i_manufact_id = 269
and i_item_sk = cs_item_sk 
and d_date between to_date('1998-03-18', 'YYYY-MM-DD') and 
        (to_date('1998-03-18', 'YYYY-MM-DD') + 90)
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
          and d_date between to_date('1998-03-18', 'YYYY-MM-DD') and 
                             (to_date('1998-03-18', 'YYYY-MM-DD') + 90)
          and d_date_sk = cs_sold_date_sk 
      ) 
 ) where rownum <= 100;

timing stop
spool off
exit
