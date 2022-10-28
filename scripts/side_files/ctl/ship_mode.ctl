LOAD DATA
INFILE '../tmp/ship_mode.dat'
TRUNCATE
INTO TABLE SHIP_MODE
FIELDS TERMINATED BY "|" OPTIONALLY ENCLOSED BY '"' TRAILING NULLCOLS
(
	sm_ship_mode_sk,
	sm_ship_mode_id,
	sm_type,
	sm_code,
	sm_carrier,
	sm_contract
)