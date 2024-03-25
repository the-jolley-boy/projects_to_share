import psycopg
from psycopg import sql
import pandas as pd
import logging
import os
from datetime import datetime
from dotenv import load_dotenv, find_dotenv

from global_vars.global_vars import GlobalVariables

load_dotenv(find_dotenv())

log_file_path = os.path.join('logs', 'dblog.log')
logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"), filename=log_file_path, filemode='a', format='%(asctime)s - [Line:%(lineno)d - Function:%(funcName)s In:%(filename)s From:%(name)s] \n[%(levelname)s] - %(message)s \n', datefmt='%d-%b-%y %H:%M:%S')

DBTable = os.environ.get('DBTable')
DBHost = os.environ.get('DBHost')
DBUsr = os.environ.get('DBUsr')
DBPass = os.environ.get('DBPass')
DBPort = os.environ.get('DBPort')

async def get_current_date_str():
    curr_month = datetime.now().month
    curr_year = str(datetime.now().year)[-2:]  # Get last two digits of the year
    return f"{curr_month}_{curr_year}"

# Returns wanted information as a df from the database given a query.
async def get_data_as_dataframe(query):
    records = None
    async with await psycopg.AsyncConnection.connect(dbname=DBTable, user=DBUsr, password=DBPass, host=DBHost, port=DBPort) as conn:
        try:
            logging.info("Opened database successfully")
            async with conn.cursor() as curr:
                # Execute the query to fetch the specific data
                await curr.execute(query)
                records = await curr.fetchall()
                logging.info("Pulled values")

                # Execute a separate query to get the total number of rows in the table
                total_query = "SELECT COUNT(*) FROM ticketsurvey"
                await curr.execute(total_query)
                total_rows = await curr.fetchone()
                total_rows = total_rows[0] if total_rows else 0
                logging.info("Fetched total rows")

        except Exception as e:
            logging.error(e)
            return pd.DataFrame(), 0  # Return an empty DataFrame and total rows 0 in case of error

    # Convert fetched records into a DataFrame
    df = pd.DataFrame(records)  # Specify column names
    return df, total_rows

async def create_tables():
    async with await psycopg.AsyncConnection.connect(dbname=DBTable, user=DBUsr, password=DBPass, host=DBHost, port=DBPort) as conn:
        try:
            async with conn.cursor() as curr:
                # Check if the unique constraint already exists
                check_constraint_query = (
                    "SELECT EXISTS ("
                    "SELECT 1 FROM information_schema.table_constraints "
                    "WHERE constraint_name = 'notify_unique_nameid_cat_id' AND table_name = 'notify_staff_message_data'"
                    ");"
                )
                await curr.execute(check_constraint_query)
                constraint_exists_row = await curr.fetchone()
                constraint_exists = constraint_exists_row[0]

                if not constraint_exists:
                    # Add unique constraint on (nameid, cat_id)
                    add_constraint_query = (
                        "ALTER TABLE notify_staff_message_data "
                        "ADD CONSTRAINT notify_unique_nameid_cat_id UNIQUE (nameid, cat_id);"
                    )
                    await curr.execute(add_constraint_query)
                    logging.info("Unique constraint added successfully")

        except Exception as e:
            logging.error(f"Error creating table or adding constraint: {e}")

async def add_new_cols(date):
    column_queries = [
        f"ALTER TABLE notify_staff_message_data ADD COLUMN IF NOT EXISTS msg_{date} BIGINT DEFAULT 0 NOT NULL",
        f"ALTER TABLE notify_staff_message_data ADD COLUMN IF NOT EXISTS word_{date} BIGINT DEFAULT 0 NOT NULL",
        f"ALTER TABLE notify_staff_message_data ADD COLUMN IF NOT EXISTS char_{date} BIGINT DEFAULT 0 NOT NULL"
    ]
    async with await psycopg.AsyncConnection.connect(dbname=DBTable, user=DBUsr, password=DBPass, host=DBHost, port=DBPort) as conn:
        try:
            async with conn.cursor() as curr:
                for query in column_queries:
                    await curr.execute(query)
                    logging.info(f"Added/Checked new column for '{date}'.")

        except Exception as e:
            logging.error(e)

# Returns wanted information from the database given a query. Set value to None if you aren't passing in data.
async def get_data(query, val):
    records = None
    async with await psycopg.AsyncConnection.connect(dbname=DBTable, user=DBUsr, password=DBPass, host=DBHost, port=DBPort) as conn:
        try:
            async with conn.cursor() as curr:
                if val != None:
                    await curr.execute(query, val)
                else:
                    await curr.execute(query)
                records = await curr.fetchall()
                logging.info("Pulled values")

        except Exception as e:
            logging.error(e)
            
    return records

# Returns wanted information from the database given a query. Set value to None if you aren't passing in data.
async def get_data_role_puller(query, val):
    records = None
    async with await psycopg.AsyncConnection.connect(dbname=DBTable, user=DBUsr, password=DBPass, host=DBHost, port=DBPort) as conn:
        try:
            async with conn.cursor(row_factory=psycopg.rows.dict_row) as curr:
                if val != None:
                    await curr.execute(query, val)
                else:
                    await curr.execute(query)
                records = await curr.fetchall()
                logging.info("Pulled values")

        except Exception as e:
            logging.error(e)
            
    return records

async def write_data(query, data):
    async with await psycopg.AsyncConnection.connect(dbname = DBTable, user = DBUsr, password = DBPass, host = DBHost, port = DBPort) as conn:
        try:
            async with conn.cursor() as curr:
                await curr.execute(query, data)
                await conn.commit()
                logging.info("Written values and closed")

        except Exception as e:
            logging.error(e)

async def write_to_db(query1, query2, payload, user):
    async with await psycopg.AsyncConnection.connect(dbname = DBTable, user = DBUsr, password = DBPass, host = DBHost, port = DBPort) as conn:
        try:
            logging.info("Opened database successfully")
            async with conn.cursor() as curr:

                await curr.execute(query1, user)
                ticketsurvey = await curr.fetchall()

                for row in ticketsurvey:
                    chid = row[0]

                #data for the %s value
                data = (chid, user, payload)
                await curr.execute(query2, data)
                await conn.commit()
                logging.info("Written values and closed")

        except Exception as e:
            logging.error(e)

async def delete_all_rows():
    async with await psycopg.AsyncConnection.connect(dbname = DBTable, user = DBUsr, password = DBPass, host = DBHost, port = DBPort) as conn:
        try:
            logging.info("Opened database successfully")
            async with conn.cursor() as curr:
                sql = "DELETE FROM supporttickets"
                await curr.execute(sql)
                sql = "DELETE FROM staffcategory"
                await curr.execute(sql)
                sql = "DELETE FROM generalcategory"
                await curr.execute(sql)
                sql = "DELETE FROM generalcategory2"
                await curr.execute(sql)
                sql = "DELETE FROM importantcategory"
                await curr.execute(sql)
                sql = "DELETE FROM sneakerinfocategory"
                await curr.execute(sql)
                sql = "DELETE FROM sneakerreleasescategory"
                await curr.execute(sql)
                sql = "DELETE FROM canadacategory"
                await curr.execute(sql)
                await conn.commit()
                logging.info("Updated and closed")

        except Exception as e:
            logging.error(e)
