#!/usr/bin/env bash
# For running a query in tpcds database.
# USAGE: ./execute_query.sh <QUERY FILE PATH> <DB USERNAME> <DB PW>

# psql -d $DB_NAME -A -F "," < $q_file > "$OUTPUT_DIR/`basename ${q_file%.*}`.res" 2> "$OUTPUT_DIR/`basename ${q_file%.*}`.err"

q_file=$1
db_username=$2
db_password=$3

echo "Started executing `basename ${q_file%.*}`"
sqlplus $db_username/$db_password @$q_file
echo "Ended executing `basename ${q_file%.*}`"
