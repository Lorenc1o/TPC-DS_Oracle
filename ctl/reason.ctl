LOAD DATA
INFILE '../tmp/reason.dat'
TRUNCATE
INTO TABLE REASON
FIELDS TERMINATED BY "|" OPTIONALLY ENCLOSED BY '"' TRAILING NULLCOLS
(
	r_reason_sk,
	r_reason_id,
	r_reason_desc
)