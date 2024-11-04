from modules import mysql
from config import ACADEMIC_YEAR

def displayContributions(organization_code :str, academic_year :str):
    try:
        cur = mysql.connection.cursor()
        search_query = """
            SELECT `name`, `amount`, `academic_year` 
            FROM `contributions` 
            WHERE `collecting_org_code` = %s 
            AND `academic_year` = %s 
            ORDER BY `name` ASC;
        """
        
        cur.execute(search_query, (organization_code, academic_year))
        return cur.fetchall()
    except mysql.connection.Error as e:
        mysql.connection.rollback()  # Rollback in case of error
        raise e
    finally:
        cur.close()  # Ensure the cursor is closed

def editContributions(fname, famount, sname, samount, organization_code):
    try:
        cur = mysql.connection.cursor()

        contributions = displayContributions(organization_code, ACADEMIC_YEAR)
        alter_query = """
            UPDATE `contributions`
            SET `name` = %s, `amount` = %s
            WHERE `name` = %s AND `collecting_org_code` = %s;
        """

        cur.execute(alter_query, (fname, famount, contributions[0][0], organization_code))
        mysql.connection.commit()
        
        cur.execute(alter_query, (sname, samount, contributions[1][0], organization_code))
        mysql.connection.commit()
    except mysql.connection.Error as e:
        mysql.connection.rollback()  # Rollback in case of error
        raise e
    finally:
        cur.close()  # Ensure the cursor is closed


def searchContributions(column :str, param :str, organization_code :str, academic_year :str):
    try:
        cur = mysql.connection.cursor()
        search_query = f"""
            SELECT `name`, `amount`, `academic_year` 
            FROM `contributions` 
            WHERE `collecting_org_code` = %s 
            AND `academic_year` = %s 
            AND {column} COLLATE utf8mb4_bin LIKE %s
            ORDER BY `name` ASC;
        """

        param_with_wildcards = f'%{param}%'
        cur.execute(search_query, (organization_code, academic_year, param_with_wildcards))
        return cur.fetchall()
    except mysql.connection.Error as e:
        mysql.connection.rollback()  # Rollback in case of error
        raise e
    finally:
        cur.close()  # Ensure the cursor is closed 

def programCodes(organization_code :str):
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT `code` FROM `programs` WHERE `organization_code` = %s ORDER BY `code` ASC;", (organization_code,))
        return cur.fetchall()
    except mysql.connection.Error as e:
        mysql.connection.rollback()  # Rollback in case of error
        raise e
    finally:
        cur.close()  # Ensure the cursor is closed 

def fetchPaid(contribution_name :str, month :int, program_code :str, year :str):
    try:
        cur = mysql.connection.cursor()
        year_levels = ['1', '2', '3', '4']
        count = []
        chosen_year = int(year)
        fetch_query =   """
                        SELECT COUNT(*) FROM `transactions` AS `t` LEFT JOIN `students` AS `s` 
                        ON `t`.`payer_id` = `s`.`id_number`
                        WHERE `t`.`contribution_name` = %s
                        AND `t`.`contribution_ay` = %s
                        AND (YEAR(`t`.`datetime`) < %s OR (YEAR(`t`.`datetime`) = %s AND MONTH(`t`.`datetime`) <= %s)) 
                        AND `t`.`status` = "Accepted" 
                        AND `s`.`program_code` = %s 
                        AND `s`.`year_level` = %s;
                        """
        for year_level in year_levels:
            cur.execute(fetch_query, (contribution_name, ACADEMIC_YEAR, chosen_year, chosen_year, month, program_code, year_level))
            count.append(cur.fetchall()[0][0])
        
        return count
    except mysql.connection.Error as e:
        mysql.connection.rollback()  # Rollback in case of error
        raise e
    finally:
        cur.close()  # Ensure the cursor is closed

def fetchUnpaid(program_code :str, paid_count : int):
    try:
        year_levels = ['1', '2', '3', '4']
        count = []

        cur = mysql.connection.cursor()
        fetch_query =   """
                        SELECT COUNT(*) FROM `students` WHERE `program_code` = %s AND `year_level` = %s;
                        """
        for s in range(0, 4):
            cur.execute(fetch_query, (program_code, year_levels[s]))
            count.append(cur.fetchall()[0][0] - paid_count[s])
        
        return count
    except mysql.connection.Error as e:
        mysql.connection.rollback()  # Rollback in case of error
        raise e
    finally:
        cur.close()  # Ensure the cursor is closed

def checkCode(code):
    try:
        cur = mysql.connection.cursor()
        fetch_query =   """
                SELECT `code` FROM `organizations` WHERE `code` = %s;
            """
        cur.execute(fetch_query, (code,))
        return cur.fetchone()
    except mysql.connection.Error as e:
        mysql.connection.rollback()  # Rollback in case of error
        raise e
    finally:
        cur.close()  # Ensure the cursor is closed


def getOrganization(code :str):
    try:
        cur = mysql.connection.cursor()
        fetch_query =   """
                SELECT * FROM `organizations` WHERE `code` = %s;
            """
        cur.execute(fetch_query, (code,))
        return cur.fetchone()
    except mysql.connection.Error as e:
        mysql.connection.rollback()  # Rollback in case of error
        raise e
    finally:
        cur.close()  # Ensure the cursor is closed