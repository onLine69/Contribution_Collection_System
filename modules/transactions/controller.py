from modules import mysql
from datetime import datetime

def displayAll(contribution_name :str, academic_year :str, student_status :str, program_code :str, year_level :str, min_point :str, max_point :str):
    try:
        cur = mysql.connection.cursor()
        fetch_query = """
            SELECT `t`.`id`, `t`.`datetime`, `s`.`id_number`, `s`.`full_name`, `t`.`payment_mode`, `t`.`status`, `t`.`transaction_message`
            FROM `transactions` AS `t` LEFT JOIN `students` AS `s` ON `t`.`payer_id` = `s`.`id_number`
            WHERE `t`.`contribution_name` = %s AND `t`.`contribution_ay` = %s
        """
        fetch_params = [contribution_name, academic_year]

        if student_status != "All":
            fetch_query += " AND `t`.`status` = %s"
            fetch_params.append(student_status)
        
        if program_code:
            fetch_query += " AND `s`.`program_code` = %s"
            fetch_params.append(program_code)

        if year_level:
            fetch_query += " AND `s`.`year_level` = %s"
            fetch_params.append(year_level)

        if min_point:
            min_datetime = datetime.fromisoformat(min_point)
            fetch_query += " AND `t`.`datetime` >= %s"
            fetch_params.append(min_datetime)

        if max_point:
            max_datetime = datetime.fromisoformat(max_point)
            fetch_query += " AND `t`.`datetime` <= %s"
            fetch_params.append(max_datetime)

        fetch_query += " ORDER BY `t`.`id` ASC, `s`.`program_code` ASC, `s`.`year_level` ASC, `s`.`full_name` ASC;"
        
        cur.execute(fetch_query, tuple(fetch_params))
        return cur.fetchall()
    except mysql.connection.Error as e:
        mysql.connection.rollback()  # Rollback in case of error
        raise e
    finally:
        cur.close()  # Ensure the cursor is closed 

def search(column :str, param :str, item_name :str, academic_year :str):
    try:
        cur = mysql.connection.cursor()
        search_query = f"""
            SELECT `t`.`id`, `t`.`datetime`, `s`.`id_number`, `s`.`full_name`, `t`.`payment_mode`, `t`.`status`, `t`.`transaction_message`
            FROM `transactions` AS `t`
            LEFT JOIN `students` AS `s` ON `t`.`payer_id` = `s`.`id_number`
            WHERE `t`.`contribution_name` = %s AND `t`.`contribution_ay` = %s AND `s`.`{column}` COLLATE utf8mb4_bin LIKE %s
            ORDER BY `t`.`id` ASC, `s`.`program_code` ASC, `s`.`year_level` ASC, `s`.`full_name` ASC;
        """

        cur.execute(search_query, (item_name, academic_year, f"%{param}%"))

        return cur.fetchall()
    except mysql.connection.Error as e:
        mysql.connection.rollback()  # Rollback in case of error
        raise e
    finally:
        cur.close()  # Ensure the cursor is closed 