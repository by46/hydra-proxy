import pymssql
import time


def main():
    # conn = pymssql.connect('10.16.82.138', user='CTIDbo', password='Dev@CTIdb0', database='CTI', port='1433')
    conn = pymssql.connect('10.16.82.138', user='ehissql-0d95446a', password='9d331a83368a', database='CTI', port='1433')
    # conn = pymssql.connect('scmesos02', user='ehissql-0d95446a', password='9d331a83368a', database='CTI', port='1433')
    # conn = pymssql.connect('S1DSQL01\\ABS_SQL', user='PODBO', password='4DevPO', database='Abs')
    cursor = conn.cursor()
    while True:
        cursor.execute('SELECT * FROM demo')
        for row in cursor.fetchall():
            print row
        time.sleep(1)
    conn.close()


if __name__ == '__main__':
    main()
