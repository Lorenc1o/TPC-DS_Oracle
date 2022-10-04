LOAD DATA
INFILE '../tmp/inventory.dat'
TRUNCATE
INTO TABLE INVENTORY
FIELDS TERMINATED BY "|" OPTIONALLY ENCLOSED BY '"' TRAILING NULLCOLS
(
	inv_date_sk,
	inv_item_sk,
	inv_warehouse_sk,
	inv_quantity_on_hand
)