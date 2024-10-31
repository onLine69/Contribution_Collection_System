from modules import mysql

def displayAll(item_name, academic_year, student_status, program_code, year_level):
    try:
        cur = mysql.connection.cursor()

        fetch_students_query = """
            SELECT `full_name`, `id_number` 
            FROM `students` 
            WHERE 1=1
        """
        fetch_students_params = []

        if program_code:
            fetch_students_query += " AND `program_code` = %s"
            fetch_students_params.append(program_code)

        if year_level:
            fetch_students_query += " AND `year_level` = %s"
            fetch_students_params.append(year_level)

        fetch_students_query += " ORDER BY `program_code` ASC, `year_level` ASC, `full_name` ASC;"

        # Get the students
        cur.execute(fetch_students_query, tuple(fetch_students_params))
        student_list = cur.fetchall()
        # Get the price/amount of the item
        get_item_amount_query = """
            SELECT `amount` 
            FROM `contributions` 
            WHERE `name` = %s AND `academic_year` = %s;
        """
        cur.execute(get_item_amount_query, (item_name, academic_year))

        item_amount_result = cur.fetchone()
        item_amount = item_amount_result[0] if item_amount_result else 0  # Default to 0 if not found

        # Initialize an empty list for students with balance
        updated_students = []

        get_balance_query = """
            SELECT `amount` 
            FROM `transactions` 
            WHERE `payer_id` = %s AND `contribution_name` = %s AND `contribution_ay` = %s AND `status` = %s;
        """

        for student in student_list:
            student_id = student[1]  # Get the student's ID
            cur.execute(get_balance_query, (student_id, item_name, academic_year, "Accepted"))
            payment_amount = cur.fetchone()

            # Initialize balance to the item's amount
            balance = item_amount

            # Determine the payment status
            if payment_amount:
                status = "Paid"
                balance -= payment_amount[0]  # Subtract the payment amount from the balance
            else:
                # Check for pending transactions
                cur.execute("""
                    SELECT `status` 
                    FROM `transactions` 
                    WHERE `payer_id` = %s AND `contribution_name` = %s AND `contribution_ay` = %s AND `status` = %s 
                    ORDER BY `datetime` DESC;
                """, (student_id, item_name, academic_year, "Pending"))
                fetched = cur.fetchone()

                # Determine status based on fetched result
                if fetched:
                    status = "Pending" if fetched[0] == "Pending" else "Unpaid"
                else:
                    status = "Unpaid"  # Default to "Unpaid" if no transactions are found

            # Append the balance and status to the student tuple based on the desired status
            if student_status == "All" or status == student_status:
                updated_students.append(student + (balance, status))

        # Close the cursor (optional but recommended)
        cur.close()

        return updated_students

    except mysql.connection.Error as e:
        mysql.connection.rollback()  # Rollback in case of error
        raise e
    finally:
        cur.close()  # Ensure the cursor is closed

def search(column, param, item_name, academic_year):
    try:
        cur = mysql.connection.cursor()

        # Get the students
        cur.execute(f"SELECT `full_name`, `id_number` FROM `students` WHERE {column} COLLATE utf8mb4_bin LIKE '%{param}%' ORDER BY `full_name` ASC;")
        student_list = cur.fetchall()

        # Get the price/amount of the item
        get_item_amount_query = "SELECT `amount` FROM `contributions` WHERE `name` = %s AND `academic_year` = %s;"
        cur.execute(get_item_amount_query, (item_name, academic_year))
        item_amount = cur.fetchone()[0]

        # Initialize an empty list for students with balance
        updated_students = []

        get_balance_query = "SELECT `amount` FROM `transactions` WHERE `payer_id` = %s AND `contribution_name` = %s AND `contribution_ay` = %s AND `status` = %s;"

        for student in student_list:
            cur.execute(get_balance_query, (student[1], item_name, academic_year, "Accepted"))
            payment_amounts = cur.fetchall()

            # Initialize balance to the item's amount
            balance = item_amount if item_amount else 0

            status = None
            if payment_amounts:
                status = "Paid"
                balance = balance - payment_amounts[0][0]
            else:
                cur.execute("SELECT `status` FROM `transactions` WHERE `payer_id` = %s AND `contribution_name` = %s AND `contribution_ay` = %s AND `status` = %s ORDER BY `datetime` DESC;", (student[1], item_name, academic_year, "Pending"))
                fetched = cur.fetchone()

                # Check if fetched is not None and extract the status
                if fetched:
                    status = "Pending" if fetched[0] == "Pending" else "Unpaid"
                else:
                    status = "Unpaid"  # Default to "Unpaid" if no transactions are found
            # Append the balance to the student tuple
            updated_students.append(student + (balance, status))

        return updated_students
    except mysql.connection.Error as e:
        mysql.connection.rollback()  # Rollback in case of error
        raise e
    finally:
        cur.close()  # Ensure the cursor is closed 

def fetchPaid(contribution_name :str, year_level :str, program_code :str, academic_year :str):
    try:
        years = academic_year.split("-")
        cur = mysql.connection.cursor()
        fetch_query =   """
            SELECT COUNT(*) FROM `transactions` AS `t` LEFT JOIN `students` AS `s` 
            ON `t`.`payer_id` = `s`.`id_number`
            WHERE `t`.`contribution_name` = %s
            AND `t`.`contribution_ay` = %s
            AND (YEAR(`t`.`datetime`) >= %s AND YEAR(`t`.`datetime`) <= %s) 
            AND `t`.`status` = "Accepted"
        """
        
        fetch_params = [contribution_name, academic_year, int(years[0]), int(years[1])]

        if year_level:
            fetch_query += " AND `s`.`year_level` = %s"
            fetch_params.append(year_level)

        if program_code:
            fetch_query += " AND `s`.`program_code` = %s"
            fetch_params.append(program_code)

        fetch_query += ";"

        cur.execute(fetch_query, tuple(fetch_params))
        
        return cur.fetchone()[0]
    except mysql.connection.Error as e:
        mysql.connection.rollback()  # Rollback in case of error
        raise e
    finally:
        cur.close()  # Ensure the cursor is closed

def fetchUnpaid(year_level :str, program_code :str, paid_count : int):
    try:
        cur = mysql.connection.cursor()
        fetch_query =   """
            SELECT COUNT(*) FROM `students` WHERE 1 = 1
        """
        
        fetch_params =[]

        if year_level:
           fetch_query += " AND `year_level` = %s"
           fetch_params.append(year_level)
        
        if program_code:
            fetch_query += " AND `program_code` = %s"
            fetch_params.append(program_code)
        
        fetch_query += ";"

        if len(fetch_params) > 0:
            cur.execute(fetch_query, tuple(fetch_params))
        else:
            cur.execute(fetch_query)
        
        return cur.fetchone()[0] - paid_count
    except mysql.connection.Error as e:
        mysql.connection.rollback()  # Rollback in case of error
        raise e
    finally:
        cur.close()  # Ensure the cursor is closed

def createTransaction(name, acad_year, amount, payer_ids, transaction_messages):
    try:
        cur = mysql.connection.cursor()
        transact_query =   """
            INSERT INTO `transactions` (`contribution_name`, `contribution_ay`, `payer_id`, `payment_mode`, `amount`, `transaction_message`, `status`)
            VALUES (%s, %s, %s, "Cash", %s, %s, "Pending");
        """
        
        for n in range(0, len(payer_ids)):
            cur.execute(transact_query, (name, acad_year, payer_ids[n], amount, transaction_messages[n]))
            mysql.connection.commit()
        
    except mysql.connection.Error as e:
        mysql.connection.rollback()  # Rollback in case of error
        raise e
    finally:
        cur.close()  # Ensure the cursor is closed


def customErrorMessages(error):
    if (error.args[0] == 1062): # Check the error code first
        value = error.args[1].split("'")[1]
        if (value[4] == '-' and len(value) == 9):   # Check if the value is an id number
            return f"ID number '{value}' already exist."
        else:
            return f"Name '{value}' already exist."
    
    return f"Something is wrong, error with code '{error.args[0]}'. \n Description: '{error.args[1]}'."