# Module with common functions for TPC-DS queries and data generation
# Path: scripts/tpcds.py
from os import path, system

"""
Function load_files

Description
	load_files calls the Oracle data loader, sqlldr, with the arguments
	previously provided as parameter

Parameters
    filespath: string with the path to the files
    ctlpath: string with the path to the control files
    username: string with the username
    password: string with the password
    svrinstance: string with the server instance
    db: string with the database name
	table_name: string with the name of the table to be populated
	file_name: string with the name of the file containing the data

Output
	None
"""
def load_files(filespath, ctlpath, username, password, svrinstance, db, table_name, file_name):
    full_path = path.join(filespath, file_name)
    ctl_path = path.join(ctlpath, table_name + '.ctl')
    log_path = path.join(filespath, file_name[:-3] + 'log')
    sqlldr = 'sqlldr userid=%s/%s@%s/%s control=%s data=%s log=%s bad=%s' % (
        username, password, svrinstance, db, ctl_path, full_path, log_path, log_path)
    system(sqlldr)


"""
Function run_query

Description
    run_query calls the Oracle SQL*Plus with the arguments previously provided as parameter

Parameters
    filepath: string with the path to the file containing the query
    output: string with the path to the file where the output will be stored
    username: string with the username
    password: string with the password
    svrinstance: string with the server instance
    db: string with the database name

Output
    None
"""
def run_query(filepath, output, username, password, svrinstance, db):
    if output != None:
        sqlplus = 'sqlplus %s/%s@%s/%s @%s %s' % (
            username, password, svrinstance, db, filepath, output)
    else:
        sqlplus = 'sqlplus %s/%s@%s/%s @%s' % (
            username, password, svrinstance, db, filepath)
    system(sqlplus)