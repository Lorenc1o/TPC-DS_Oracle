LOAD DATA
INFILE '../tmp/income_band.dat'
TRUNCATE
INTO TABLE INCOME_BAND
FIELDS TERMINATED BY "|" OPTIONALLY ENCLOSED BY '"' TRAILING NULLCOLS
(
	ib_income_band_sk,
	ib_lower_bound,
	ib_upper_bound
)