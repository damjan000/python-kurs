import sqlite3
from sqlite3 import Error


class Osoba:
    def __init__(self, id, ime, prezime):
        self.id = id
        self.ime = ime
        self.prezime = prezime

    def __str__(self):
        return "Ime: " + self.ime + ", prezime: " + self.prezime


def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return conn


def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        cursor = conn.cursor()
        cursor.execute(create_table_sql)
    except Error as e:
        print(e)


def create_osoba(conn, osoba):
    """
    Create a new osoba into the osoba table
    :param conn:
    :param osoba:
    :return: osoba id
    """
    try:
        sql = ''' INSERT INTO osobas(id,ime,prezime)
                  VALUES(?,?,?) '''
        cur = conn.cursor()
        params = (osoba.id, osoba.ime, osoba.prezime)
        cur.execute(sql, params)
        conn.commit()
    except Error as e:
        print(e)


def select_all_osoba(conn):
    sql = ''' SELECT * FROM osobas;'''
    cur = conn.cursor()
    cur.execute(sql)
    ans = cur.fetchall()
    return ans


if __name__ == '__main__':
    sql_create_osoba_table = """ CREATE TABLE IF NOT EXISTS osobas (
                                           id integer PRIMARY KEY,
                                           ime text NOT NULL,
                                           prezime text NOT NULL
                                       ); """

    # create a database connection
    conn = create_connection("db2.db")

    if conn is not None:
        # create projects table
        create_table(conn, sql_create_osoba_table)

        while True:
            izbor = int(input("Unesite 0 za kraj programa, 1 za unos nove osobe, 2 za brisanje osobe, 3 za update osobe..."))
            if izbor == 0:
                break
            elif izbor == 1:
                id_osobe = int(input("Unesite ID osobe:"))
                ime_osobe = input("Unesite ime osobe:")
                prezime_osobe = input("Unesite prezime osobe:")
                o = Osoba(id_osobe, ime_osobe, prezime_osobe)
                create_osoba(conn, o)
            elif izbor == 4:
                r = select_all_osoba(conn)
                for i in r:
                    print(i)

    else:
        print("Error! cannot create the database connection.")
