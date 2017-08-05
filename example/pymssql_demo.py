import pymssql


def main():
    conn = pymssql.connect('10.16.82.138', user='CTIDbo', password='Dev@CTIdb0', database='CTI', port='1433')
    # conn = pymssql.connect('S1DSQL04\\EHISSQL', user='CTIDbo', password='Dev@CTIdb0',database='CTI')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM demo')
    for row in cursor.fetchall():
        print row
    cursor.execute('SELECT * FROM demo')
    for row in cursor.fetchall():
        print row

    conn.close()


if __name__ == '__main__':
    main()
