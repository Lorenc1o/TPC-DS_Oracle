LOAD DATA
INFILE '../tmp/household_demographics.dat'
TRUNCATE
INTO TABLE HOUSEHOLD_DEMOGRAPHICS
FIELDS TERMINATED BY "|" OPTIONALLY ENCLOSED BY '"' TRAILING NULLCOLS
(
	hd_demo_sk,
	hd_income_band_sk,
	hd_buy_potential,
	hd_dep_count,
	hd_vehicle_count
)