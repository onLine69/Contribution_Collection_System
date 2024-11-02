from modules import mysql


def displayAll(contribution_name, academic_year, program_code, year_level):
    try:
        cur = mysql.connection.cursor()
        fetch_query = """
            SELECT `t`.`id`, `t`.`datetime`, `s`.`id_number`, `s`.`full_name`, `t`.`payment_mode`, `t`.`transaction_message`
            FROM `transactions` AS `t`
            LEFT JOIN `students` AS `s` ON `t`.`payer_id` = `s`.`id_number`
            WHERE `t`.`status` = "Pending" 
            AND `t`.`contribution_name` = %s 
            AND `t`.`contribution_ay` = %s 
            AND `s`.`id_number` NOT IN (
                SELECT `st`.`id_number`
                FROM `transactions` AS `tr`
                LEFT JOIN `students` AS `st` ON `tr`.`payer_id` = `st`.`id_number`
                WHERE (`tr`.`status` = "Accepted") 
                AND `tr`.`contribution_name` = %s 
                AND `tr`.`contribution_ay` = %s
            )
        """
        fetch_params = [contribution_name, academic_year, contribution_name, academic_year]
        
        if program_code:
            fetch_query += " AND `s`.`program_code` = %s"
            fetch_params.append(program_code)

        if year_level:
            fetch_query += " AND `s`.`year_level` = %s"
            fetch_params.append(year_level)

        fetch_query += " ORDER BY `t`.`id` ASC, `s`.`program_code` ASC, `s`.`year_level` ASC, `s`.`full_name` ASC;"

        cur.execute(fetch_query, tuple(fetch_params))
        return cur.fetchall()
    except mysql.connection.Error as e:
        mysql.connection.rollback()  # Rollback in case of error
        raise e
    finally:
        cur.close()  # Ensure the cursor is closed 

def search(column, param, item_name, academic_year):
    try:
        cur = mysql.connection.cursor()
        search_query = f"""
            SELECT `t`.`id`, `t`.`datetime`, `s`.`id_number`, `s`.`full_name`, `t`.`payment_mode`
            FROM `transactions` AS `t`
            LEFT JOIN `students` AS `s` ON `t`.`payer_id` = `s`.`id_number`
            WHERE `t`.`contribution_name` = %s 
            AND `t`.`status` = "Pending"
            AND `t`.`contribution_ay` = %s 
            AND `s`.`{column}` COLLATE utf8mb4_bin LIKE %s
            AND `s`.`id_number` NOT IN (
                SELECT `st`.`id_number`
                FROM `transactions` AS `tr`
                LEFT JOIN `students` AS `st` ON `tr`.`payer_id` = `st`.`id_number`
                WHERE (`tr`.`status` = "Accepted" OR `tr`.`status` = "Rejected")
            )
            ORDER BY `t`.`id` ASC, `s`.`program_code` ASC, `s`.`year_level` ASC, `s`.`full_name` ASC;
        """

        cur.execute(search_query, (item_name, academic_year, f"%{param}%"))

        return cur.fetchall()
    except mysql.connection.Error as e:
        mysql.connection.rollback()  # Rollback in case of error
        raise e
    finally:
        cur.close()  # Ensure the cursor is closed 

def verifyTransactions(name, acad_year, amount, payer_ids, transaction_messages):
    try:
        cur = mysql.connection.cursor()
        transact_query =   """
                        INSERT INTO `transactions` (`contribution_name`, `contribution_ay`, `payer_id`, `payment_mode`, `amount`, `transaction_message`, `status`)
                        VALUES (%s, %s, %s, "Cash", %s, %s, "Accepted");
                        """
        check_query = """
            SELECT COUNT(`payer_id`) 
            FROM `transactions` 
            WHERE  `payer_id` = %s AND `contribution_name` = %s AND `contribution_ay` = %s AND `status` = "Accepted"
        """ 
        
        for n in range(0, len(payer_ids)):
            cur.execute(check_query, (payer_ids[n], name, acad_year))
            recorded = cur.fetchone()[0]
            print(recorded)
            if recorded == 0:
                cur.execute(transact_query, (name, acad_year, payer_ids[n], amount, transaction_messages[n]))
                mysql.connection.commit()
        
    except mysql.connection.Error as e:
        mysql.connection.rollback()  # Rollback in case of error
        raise e
    finally:
        cur.close()  # Ensure the cursor is closed
