from config import host, user, password, db_name
import os
import string
import threading
import psycopg2
import random
import csv

class Color:
    BOLD ='\033[1m'
    OK = '\033[92m'
    FAIL = '\033[91m'
    TLE = '\033[93m'
    END = '\033[0m'

# Funkcia ktora prerusi vykonanie dotazu ak ten bezi viac ako timeout sekund 
def execute_query_with_timeout(connection, cursor, query, timeout):
    result = []
    pid = None

    def get_pid():
        cursor.execute("SELECT pg_backend_pid();")
        nonlocal pid
        pid = cursor.fetchone()[0]

    def target():
        try:
            get_pid()
            cursor.execute(query)
            result.append(cursor.fetchall())           
        except Exception as e:
            print(f"Error when executing student's answer: {e}")

    thread = threading.Thread(target=target)
    thread.start()
    thread.join(timeout)

    if thread.is_alive():
        if pid:
            try:
                with connection.cursor() as cancel_cursor:
                    cancel_cursor.execute(f"SELECT pg_cancel_backend({pid});")
            except Exception as e:
                print(f"Stopped the execution of a student's answer. It has taken longer than {timeout}s: {e}")
        return "TLE"
    else:
        colnames = [desc[0] for desc in cursor.description]
        answer = [dict(zip(colnames, row)) for row in result[0]]
        return answer
    
# Funkcia, ktorá prevedie výsledok na set    
def normalize_result(result):
    normalized_result = set()
    for row in result:
        normalized_row = tuple(sorted((k, v) for k, v in row.items()))
        normalized_result.add(normalized_row)
    return normalized_result

# Funkcia na vykonanie študentských dotazov SQL, porovnanie výsledkov so správnou odpoveďou a kontrola Time Limit
def execute_sql_and_compare_results(connection, sql_file, correct_answer, hasOrderBy):
    with open(sql_file, 'r') as file:
        sql_query = file.read()

    with connection.cursor() as cursor:
        student_answer = execute_query_with_timeout(connection, cursor, sql_query, 0.2)

    if student_answer == "TLE":
        return "TLE"
    
    for row in student_answer:
        print(row)
    print("\n") 
    
    # Ak správny sql dotaz (correctAnswer.sql) neobsahuje ORDER BY, potom poradie riadkov v tabuľke nie je dôležité
    # takže ich môžeme porovnať ako dve množiny.
    if hasOrderBy == 0:
        if normalize_result(correct_answer) == normalize_result(student_answer):
            return "OK"
        else:
            return "FAIL"
        
    # Ak správny sql dotaz (correctAnswer.sql) obsahuje ORDER BY, potom je poradie riadkov dôležité, takže porovnávame odpovede tak, ako sú.    
    if correct_answer == student_answer:
        return "OK"
    else:
        return "FAIL" 
    
    

# Funkcia na zápis výsledkov dotazov študentov do súboru CSV
def write_results_to_csv(results):
   
    current_dir = os.getcwd()
    file_path = os.path.join(current_dir, 'results.csv')
    
    with open(file_path, 'w', newline='') as file:
        writer = csv.writer(file)
        print(f"{Color.BOLD}RESULTS IN results.csv :{Color.END}")
        writer.writerow(['Student name', 'Result'])
        print("Student name     Result")
        for student, result in results.items():
            writer.writerow([student, result])
            
            print(student, end='     ')
            if "OK" in result:
                print(f"   {Color.OK} {result} {Color.END}")
            elif "FAIL" in result:
                print(f"   {Color.FAIL} {result} {Color.END}")
            elif"TLE" in result :
                print(f"   {Color.TLE} {result} {Color.END}")
                
                        
    print("\n")        
            
            
# Funkcia na generovanie slova urcitej dlzky            
def generate_random_word(length):
    letters = string.ascii_lowercase 
    random_word = ''.join(random.choice(letters) for _ in range(length))
    return random_word


# Funkcia na zápis falošných dát do tabuliek
def insert_default_data(connection, table_name, columns):
    connection.autocommit = True
    insert_query = f"INSERT INTO {table_name} ("
    for column in columns:
        if "PRIMARY KEY" not in column:
            insert_query += f"{column.split()[0]}, "
    insert_query = insert_query.rstrip(', ') + ") VALUES ("

    numOfLines = random.randint(500, 1000)
    try:
        for i in range(numOfLines):
            values = []
            for column in columns:
                if "PRIMARY KEY" not in column:
                    if "FOREIGN KEY" in column:
                        try:
                            # Získanie všetkých hodnôt PRIMARY KEY z druhej tabuľky
                            primary_keys = []
                            with connection.cursor() as cursor:
                                cursor.execute(f"SELECT {column.split()[4]} FROM {column.split()[3]};")
                                primary_keys = cursor.fetchall()
                                random_primary_key = random.choice(primary_keys)[0]

                            # Ak je hodnota primary_keys prázdna alebo 
                            # random_primary_key == i + 1 (aby stĺpec nebol vždy úplne vyplnený, pridajme nejakú podmienku) - pridajme hodnotu NULL
                            if not primary_keys or random_primary_key == i + 1:
                                values.append(None)
                            else :
                                values.append(str(random_primary_key))
                            print("FOREIGN KEY added!")

                        except Exception as e:
                            print(f"Error when updating FOREIGN KEY values in {table_name} : {e}")
                    elif 'text' in column:
                        values.append(f"'{generate_random_word(5)}'")
                    elif 'int' in column:
                        values.append(str(random.randint(0, 1000)))   
                        
            values = ["NULL" if v is None else v for v in values]
            full_insert_query = insert_query + ', '.join(values) + ");"

            with connection.cursor() as cursor:
                cursor.execute(full_insert_query, tuple(values))
                print(f"Data were successfully inserted into {table_name}!")
                
                
    except Exception as e:
        print(f"Error when inserting data into the table {table_name}: {e}")
        
        
        
# Funkcia na vytvaranie jednej tabulky
def create_table(connection, table_name, columns):
    create_table_query = f"CREATE TABLE {table_name} ("
    array = []
    
    for column in columns:
        
        if "FOREIGN KEY" in column:
            # Ak je v tabuľke FOREIGN KEY, vytvorme príslušný kľúč
            foreign_key = column.split()[0]
            referenced_column = column.split()[4]
            referenced_table = column.split()[3]
            array.append(f"ALTER TABLE {table_name} ADD CONSTRAINT fk_{table_name}_{referenced_table} FOREIGN KEY ({foreign_key}) REFERENCES {referenced_table}({referenced_column});")
            
            create_table_query += f"{column.split()[0]} "
            create_table_query += "int, "
        elif "PRIMARY KEY" in column:
            create_table_query += f"{column.split()[0]} "
            create_table_query += "SERIAL "
            create_table_query += f"{column.split()[1]} "
            create_table_query += f"{column.split()[2]}, "
        else :
            create_table_query += f"{column}, "    

    create_table_query = create_table_query.rstrip(', ') + ");"

    try:
        with connection.cursor() as cursor:
            cursor.execute(create_table_query)
                
            # Ak je v tabuľke aspon jeden FOREIGN KEY, pridame ho do tabulky
            if array:
               for query in array:
                    cursor.execute(query)
                    print(f"Foreign key for {table_name} successfully added!")
                    
            print(f"Table {table_name} successfully created!")        
                
    except Exception as e:
        print(f"Error when creating a table {table_name}: {e}")
        

# Funkcia na vytvorenie všetkých tabuliek zo súboru
def create_tables_from_file(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    num_tables = int(lines[0])

    current_line = 1
    for _ in range(num_tables):
        while not lines[current_line].startswith('table_name:'):
            current_line += 1
        table_name = lines[current_line].split(':')[1].strip()

        current_line += 1
        length = 0
        while current_line + length < len(lines) and not lines[current_line + length].startswith('table_name:'):
            length += 1
        
        columns = [col.strip() for col in lines[current_line:current_line + length - 1]]
        
        try:
            connection = psycopg2.connect(
                host=host,
                user=user,
                password=password,
                database=db_name
            )
            connection.autocommit = True
            print(f"{Color.BOLD}CREATION TABLE {table_name} HAS STARTED{Color.END}")
            
            create_table(connection, table_name, columns)
            
            # INSERT FAKE DATA
            insert_default_data(connection, table_name, columns)

            print(f"{Color.BOLD}DATA IN TABLE {table_name} :{Color.END}")
            with connection.cursor() as cursor:
                cursor.execute(f"SELECT * FROM {table_name};")
                rows = cursor.fetchall()
                for row in rows:
                    print(row)
            print("\n") 
            
        except Exception as e:
            print(f"Error when creating a table {table_name}: {e}")
        finally:
            if connection:
                connection.close()

        current_line += length



if __name__ == "__main__":
    
    # NOTE: Je potrebné zmeniť username na meno používateľa.
    username = 'ekaterina'
    
    file_path = f'/home/{username}/createTable/createTables.txt'
    create_tables_from_file(file_path)

    with open(f'/home/{username}/correctAnswer/correctAnswer.sql', 'r') as file:
        correct_answer_query = file.read()

    try:
            connection1 = psycopg2.connect(
                host=host,
                user=user,
                password=password,
                database=db_name
            )
            connection1.autocommit = True
            
            # Spracovanie vzorovej odpoveďi
            hasOrderBy = 0
            with connection1.cursor() as cursor:
                cursor.execute(correct_answer_query)
                correct_answer = cursor.fetchall()
                colnames = [desc[0] for desc in cursor.description]
                correct_answer = [dict(zip(colnames, row)) for row in correct_answer]
                
                if 'ORDER BY' in correct_answer_query:
                    hasOrderBy = 1
                        
                print(f"{Color.BOLD}CORRECT ANSWER:{Color.END}")
                for row in correct_answer:
                    print(row)
                print("\n")   

            # Spracovanie súborov s odpoveďami študentov
            students_results = {}
            file_path = f'/home/{username}/pathesToStudents/pathesToStudents.txt'

            with open(file_path, 'r') as file:
                for line in file:
                    student_answer_file = line.strip()
                    if student_answer_file.endswith('.sql') and os.path.exists(student_answer_file):
                        student_name = os.path.splitext(os.path.basename(student_answer_file))[0]
                        
                        print(f"{Color.BOLD}{student_name} ANSWER:{Color.END}")
                        result = execute_sql_and_compare_results(connection1, student_answer_file, correct_answer, hasOrderBy)
                        
                        students_results[student_name] = result

            # Zapís výsledkov do súboru CSV
            write_results_to_csv(students_results)
            
            # Vymazanie všetkych tabuľiek
            cur = connection1.cursor()
            cur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'")
            table_names = cur.fetchall()
            for table_name in table_names:
                cur.execute("DROP TABLE IF EXISTS %s CASCADE" % (table_name[0]))
                print(f"[INFO] Table {Color.BOLD}{table_name[0]}{Color.END} was deleted.")
            connection1.commit()

    except Exception as e:
        print(f"Error when executing sql queries or deleting tables from the database : {e}")
    finally:
        if connection1:
            connection1.close()