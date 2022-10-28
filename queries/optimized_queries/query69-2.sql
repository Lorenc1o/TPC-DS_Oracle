spool &1
timing start t

select * from (select  
  cd_gender,
  cd_marital_status,
  cd_education_status,
  count(*) cnt1,
  cd_purchase_estimate,
  count(*) cnt2,
  cd_credit_rating,
  count(*) cnt3
 from
  customer c,customer_address ca,customer_demographics,
   ((select ss_customer_sk customer_sk
          from store_sales,date_dim
          where ss_sold_date_sk = d_date_sk and
                d_year = 1999 and
                d_moy between 1 and 1+2)
    minus
    (select ws_bill_customer_sk customer_sk
            from web_sales,date_dim
            where ws_sold_date_sk = d_date_sk and
                  d_year = 1999 and
                  d_moy between 1 and 1+2)
    minus
    (select cs_ship_customer_sk customer_sk 
            from catalog_sales,date_dim
            where cs_sold_date_sk = d_date_sk and
                  d_year = 1999 and
                  d_moy between 1 and 1+2))
 where
  c.c_current_addr_sk = ca.ca_address_sk and
  ca_state in ('CO','IL','MN') and
  cd_demo_sk = c.c_current_cdemo_sk and
  c.c_customer_sk = customer_sk
 group by cd_gender,
          cd_marital_status,
          cd_education_status,
          cd_purchase_estimate,
          cd_credit_rating
 order by cd_gender,
          cd_marital_status,
          cd_education_status,
          cd_purchase_estimate,
          cd_credit_rating
  ) where rownum <= 100;
  
timing stop
spool off
exit
