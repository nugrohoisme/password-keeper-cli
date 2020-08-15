import os
import sqlite3

# Check if file exists
if os.path.exists('password.db'):
    requireInit = False
else:
    requireInit = True

conn = sqlite3.connect('password.db')
encoding = 'utf-32'

def init():
    sql = """ CREATE TABLE `credentials` ( 
                `item` TEXT NOT NULL, 
                `username` TEXT, 
                `password` BLOB, 
                PRIMARY KEY(`item`) 
            ) WITHOUT ROWID; """

    c = conn.cursor()
    c.execute(sql)

def add_data(item, user, pswd):
    pswd = pswd.strip('"')
    pswd = bytearray(pswd, encoding)

    conn.execute("INSERT INTO credentials VALUES (?,?,?)", (item, user, pswd))
    conn.commit()

def edit_data(item, user, pswd):
    fields = []
    params = []

    if len(user) > 0:
        fields.append("username = ?")
        params.append(user)

    if len(pswd) > 0:
        fields.append("password = ?")

        pswd = pswd.strip('"')
        pswd = bytearray(pswd, encoding)
        params.append(pswd)
    
    params.append(item)

    conn.execute("UPDATE credentials SET {0} WHERE item = ?".format(', '.join(fields)), tuple(params))
    conn.commit()

def delete_data(item):
    conn.execute("DELETE FROM credentials WHERE item = ?", item)
    conn.commit()

def list_data(item=None):
    if item is None:
        cur = conn.execute("SELECT item FROM credentials")
    else:
        cur = conn.execute("SELECT item FROM credentials WHERE item LIKE '%{0}%'".format(item))

    return [row[0] for row in cur]

def get_data(item, mode='a'):
    if mode == 'a':
        select = ['username', 'password']
    elif mode == 'p':
        select = ['password']
    elif mode == 'u':
        select = ['username']

    cur = conn.execute("SELECT %s FROM credentials WHERE item = '%s' LIMIT 1" % (', '.join(select), item))
    for row in cur:
        if mode == 'a':
            return {'username':row[0], 'password':row[1].decode(encoding)}
        elif mode == 'p':
            return {'password':row[0].decode(encoding)}
        elif mode == 'u':
            return {'username':row[0]}

    return None

def get_all_data():
    cur = conn.execute("SELECT item, username, password FROM credentials")

    return [{
        'item': row[0],
        'username': row[1],
        'password': row[2].decode(encoding)
    } for row in cur]

if __name__ == '__main__':
    # init DB if required
    if requireInit:
        print('Initalize database...')
        init()

    # Get user input
    cmd = input('Insert command or item name: ')

    cmd_arr = cmd.split('|')

    try:
        ###### Add Data ######

        if cmd_arr[0] == 'add':
            if len(cmd_arr) != 4:
                raise Exception

            add_data(cmd_arr[1], cmd_arr[2], cmd_arr[3])

            print('Add successfully!')
        
        ###### Edit Data ######

        elif cmd_arr[0] == 'edit':
            if len(cmd_arr) != 4:
                raise Exception

            edit_data(cmd_arr[1], cmd_arr[2], cmd_arr[3])
            print('Edit successfully!')

        ###### Delete Item ######

        elif cmd_arr[0] == 'delete':
            if len(cmd_arr) != 2:
                raise Exception

            delete_data(cmd_arr[1])
            print('Delete successfully!')

        ###### List Data ######

        elif cmd_arr[0] == 'list':
            if len(cmd_arr) > 2:
                raise Exception

            if len(cmd_arr) == 1:
                result = list_data()
            else:
                result = list_data(cmd_arr[1])

            for r in result:
                print('+ {0}'.format(r))

        ###### Export Data ######

        elif cmd_arr[0] == 'export':
            if len(cmd_arr) > 2:
                raise Exception

            fname = 'password.txt' if len(cmd_arr) == 1 else cmd_arr[1]

            with open(fname, 'w') as f:
                for row in get_all_data():
                    f.write("%s\n" % row['item'])

                    if len(row['username']) > 0:
                        f.write("%s\n" % row['username'])
                    
                    f.write("%s\n\n" % row['password'])

            print('Export successfully to {0}!'.format(fname))

        ###### Help ######

        elif cmd_arr[0] == 'help':
            if len(cmd_arr) != 1:
                raise Exception

            print('')
            print('[Add Data]')
            print('> add|{item}|{username}|{password}')
            print('')
            print('[Edit Data]')
            print('> edit|{item}|{username}|{password}')
            print('')
            print('[Delete Data]')
            print('> delete|{item}')
            print('')
            print('[List Data]')
            print('> list')
            print('> list|{item}')
            print('')
            print('[Get Data]')
            print('> {item}')
            print('> {item}|username')
            print('> {item}|password')
            print('> {item}|all')
            print('')
            print('[Export Data]')
            print('> export')
            print('> export|{filename}')

        ###### Get Data ######

        else:
            if len(cmd_arr) > 2:
                raise Exception

            if len(cmd_arr) == 1:
                result = get_data(cmd_arr[0], 'p')
            else:
                if cmd_arr[1] == 'password':
                    result = get_data(cmd_arr[0], 'p')
                elif cmd_arr[1] == 'username':
                    result = get_data(cmd_arr[0], 'u')
                elif cmd_arr[1] == 'all':
                    result = get_data(cmd_arr[0], 'a')
                else:
                    raise Exception

            if result is None:
                print('Item is not found')
            else:
                if 'password' in result:
                    import clipboard
                    clipboard.copy(result['password'])
                    print('Password is copied to clipboard')
                
                if 'username' in result:
                    print('Username: %s' % result['username'])
    except ImportError as e:
        print(e)
        print('Please install required libraries')
    except:
        print('Unrecognized command')

    conn.close()
