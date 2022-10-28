LOAD DATA
INFILE '../tmp/time_dim.dat'
TRUNCATE
INTO TABLE TIME_DIM
FIELDS TERMINATED BY "|" OPTIONALLY ENCLOSED BY '"' TRAILING NULLCOLS
(
	t_time_sk,
	t_time_id,
	t_time,
	t_hour,
	t_minute,
	t_second,
	t_am_pm,
	t_shift,
	t_sub_shift,
	t_meal_time
)
