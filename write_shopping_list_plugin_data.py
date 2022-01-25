import sqlite3


def main():
    with sqlite3.connect('../../../db.sqlite3') as con:
        con.execute("INSERT INTO shoppinglistpluginunit(unit)"
                    f"VALUES ('g'),"
                    f"('kg'),"
                    f"('ml'),"
                    f"('L'),"
                    f"('stk'),"
                    f"('pck')")
        con.commit()


if __name__ == '__main__':
    main()
