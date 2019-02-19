import csv

import MySQLdb



def write2mysql(user, passwd, db, sql_commands):

    try:
        connection = MySQLdb.connect(host = "localhost",
                                     user = user,
                                     passwd = passwd,
                                     db = db)
    except MySQLdb.Error as e:
        print("Error %d: %s" % (e.args[0], e.args[1]))
        sys.exit(1)
    
    cursor = connection.cursor()

    for command in sql_commands:
        cursor.execute(command)

    connection.commit()

    cursor.close()
    connection.close()


def rchop(thestring, ending):
  if thestring.endswith(ending):
    return thestring[:-len(ending)]
  return thestring


def custom_list_join(plist, sep):
    finalstr = ''
    for elem in plist:
        finalstr += elem.__repr__() + sep
    finalstr = rchop(finalstr, sep)
    return finalstr


def load_csv(filepath, castvartypes='str', first_row_is_header=True):
    loaded_csv = []
    casttype = {
    'int': int,
    'str': str,
    'float': float
    }

    values_begin_from_row = 0
    

    with open(filepath, newline='\n') as csvfile:
        csvreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        templist = []
        for row in csvreader:
            templist.append(row)

    if first_row_is_header:
        values_begin_from_row = 1
        loaded_csv.append(templist[0])


        for row_index in range(values_begin_from_row, len(templist)):
            if isinstance(castvartypes, str):
                loaded_csv.append([casttype[castvartypes](templist[row_index][i]) for i in range(len(row))])
            elif isinstance(castvartypes, list):
                loaded_csv.append([casttype[castvartypes[i]](templist[row_index][i]) for i in range(len(row))])
    return loaded_csv

def plist2sql(plist, table, first_row_is_header=True, enum=False):
    sql_command = []
    headers = ''
    values_begin_from_row = 0

    if first_row_is_header:
        values_begin_from_row = 1
        inline_text = ', '.join(plist[0])
        headers = f' ({inline_text})'

    if enum:
        for _id, values in enumerate(plist[values_begin_from_row:]):
            sql_command.append(f"""INSERT INTO {table}{headers} VALUES ({_id}, {custom_list_join(values, ', ')});""")
    else:
        for values in plist[values_begin_from_row:]:
            sql_command.append(f"""INSERT INTO {table}{headers} VALUES ({custom_list_join(values, ', ')});""")
    return sql_command

# for row in plist2sql(load_csv('../names.csv', castvartypes=['str', 'int']), enum=True):
#     print(row)
