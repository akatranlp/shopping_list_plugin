import sqlite3


def main():
    with sqlite3.connect('../../../files/db.sqlite3') as con:
        con.execute("INSERT INTO shoppinglistplugin_unit(id, unit)"
                    f"VALUES (1, 'g'),"
                    f"(2, 'kg'),"
                    f"(3, 'ml'),"
                    f"(4, 'L'),"
                    f"(5, 'stk'),"
                    f"(6, 'pck')")
        con.commit()


if __name__ == '__main__':
    main()
