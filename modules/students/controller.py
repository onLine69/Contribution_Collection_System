from modules import mysql
import pandas as pd

def displayAll():
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM `students` ORDER BY `program_code` ASC, `year_level` ASC, `full_name` ASC;")
        return cur.fetchall()
    except mysql.connection.Error as e:
        mysql.connection.rollback()  # Rollback in case of error
        raise e
    finally:
        cur.close()  # Ensure the cursor is closed


def search(column :str, param :str):
    try:
        cur = mysql.connection.cursor()
        cur.execute(f"SELECT * FROM `students` WHERE {column} COLLATE utf8mb4_bin LIKE '%{param}%' ORDER BY `program_code` ASC, `year_level` ASC, `full_name` ASC;")
        return cur.fetchall()
    except mysql.connection.Error as e:
        mysql.connection.rollback()  # Rollback in case of error
        raise e
    finally:
        cur.close()  # Ensure the cursor is closed    


def add(student :tuple):
    try:
        cur = mysql.connection.cursor()
        insert_statement =  """
                                INSERT INTO `students` (`full_name`, `id_number`, `gender`, `year_level`, `program_code`, `note`)
                                VALUE (%s, %s, %s, %s, %s, %s) 
                            """
        cur.execute(insert_statement, student)
        mysql.connection.commit()
    except mysql.connection.Error as e:
        mysql.connection.rollback()  # Rollback in case of error
        raise e
    finally:
        cur.close()  # Ensure the cursor is closed


def adds(file_path :str):
    try:
        # Read data based on file extension
        if file_path.endswith('.xls') or file_path.endswith('.xlsx'):
            # Read Excel file
            df = pd.read_excel(file_path, sheet_name=0)
        elif file_path.endswith('.csv'):
            # Read CSV file
            df = pd.read_csv(file_path)
        else:
            raise ValueError("Unsupported file format. Please provide a .xls, .xlsx, or .csv file.")

        # Create a cursor object
        with mysql.connection.cursor() as cur:
            insert_statement = """
                INSERT INTO `students` (`full_name`, `id_number`, `gender`, `year_level`, `program_code`)
                VALUES (%s, %s, %s, %s, %s)
            """

            # Loop through each row in the DataFrame
            for index, row in df.iterrows():
                student = (
                    row['full_name'], 
                    row['id_number'],
                    row['gender'],
                    row['year_level'],
                    row['program_code']
                )

                # Execute the insert statement
                cur.execute(insert_statement, student)

            # Commit the transaction after all inserts
            mysql.connection.commit()
    except mysql.connection.Error as e:
        mysql.connection.rollback()  # Rollback in case of error
        raise e
    except ValueError as ve:
        raise ve
    except Exception as e:
        raise e


def edit(student :tuple):
    try:
        cur = mysql.connection.cursor()
        insert_statement =  """
                                UPDATE `students`
                                SET `full_name` = %s, `id_number` = %s, `gender` = %s, `year_level` = %s, `program_code` = %s, `note` = %s
                                WHERE `id_number` = %s;
                            """
        cur.execute(insert_statement, student)
        mysql.connection.commit()
    except mysql.connection.Error as e:
        mysql.connection.rollback()  # Rollback in case of error
        raise e
    finally:
        cur.close()  # Ensure the cursor is closed


def delete(id_number :str):
    try:
        cur = mysql.connection.cursor()
        delete_statement = """
                        DELETE FROM `students` 
                        WHERE `id_number` = %s;
                        """
        cur.execute(delete_statement, (id_number,))
        mysql.connection.commit()
    except mysql.connection.Error as e:
        mysql.connection.rollback()  # Rollback in case of error
        raise e
    finally:
        cur.close()  # Ensure the cursor is closed

def fetchUnpaid(program_code :str, year_level :str):
    try:
        cur = mysql.connection.cursor()
        fetch_statement =  """
                SELECT `s`.`id_number`, `s`.`full_name`
                FROM `students` AS `s`
                LEFT JOIN `transactions` AS `t` ON `s`.`id_number` = `t`.`payer_id` AND `t`.`status` = "Accepted"
                WHERE `t`.`payer_id` IS NULL AND `program_code` = %s AND `year_level` = %s
                ORDER BY `s`.`full_name`;
            """
        cur.execute(fetch_statement, (program_code, year_level))
        return cur.fetchall()
    except mysql.connection.Error as e:
        mysql.connection.rollback()  # Rollback in case of error
        raise e
    finally:
        cur.close()  # Ensure the cursor is closed

def fetchPaid(program_code :str, year_level :str):
    try:
        cur = mysql.connection.cursor()
        fetch_statement =  """
                SELECT `s`.`id_number`, `s`.`full_name`
                FROM `transactions` AS `t` LEFT JOIN `students` AS `s` ON `t`.`payer_id` = `s`.`id_number`
                WHERE `t`.`status` = "Accepted"
                AND `program_code` = %s AND `year_level` = %s
                ORDER BY `s`.`full_name`;
            """
        cur.execute(fetch_statement, (program_code, year_level))
        return cur.fetchall()
    except mysql.connection.Error as e:
        mysql.connection.rollback()  # Rollback in case of error
        raise e
    finally:
        cur.close()  # Ensure the cursor is closed

def fetchAll(program_code :str, year_level :str):
    try:
        cur = mysql.connection.cursor()
        fetch_statement =  """
                SELECT `id_number`, `full_name`
                FROM `students`
                WHERE `program_code` = %s AND `year_level` = %s
                ORDER BY `full_name`;
            """
        cur.execute(fetch_statement, (program_code, year_level))
        return cur.fetchall()
    except mysql.connection.Error as e:
        mysql.connection.rollback()  # Rollback in case of error
        raise e
    finally:
        cur.close()  # Ensure the cursor is closed

def customErrorMessages(error):
    if (error.args[0] == 1451):
        return "Student with transaction made cannot be deleted."
    
    if (error.args[0] == 1062): # Check the error code first
        value = error.args[1].split("'")[1]
        if (value[4] == '-' and len(value) == 9):   # Check if the value is an id number
            return f"ID number '{value}' already exist."
        else:
            return f"Name '{value}' already exist."
    
    return f"Something is wrong, error with code '{error.args[0]}'. \n Description: '{error.args[1]}'."