from connect import get_connection

def search(pattern):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM search_contacts(%s)", (pattern,))
    rows = cur.fetchall()
    for row in rows:
        print(row)
    cur.close()
    conn.close()

def paginate(limit, offset):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM get_contacts_paginated(%s, %s)", (limit, offset))
    rows = cur.fetchall()
    for row in rows:
        print(row)
    cur.close()
    conn.close()

def insert_or_update(name, phone):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("CALL insert_or_update_user(%s, %s)", (name, phone))
    conn.commit()
    cur.close()
    conn.close()

def insert_many():
    names = ["Ali", "Test", "Bad"]
    phones = ["8700123", "abc123", "999999"]
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("CALL insert_many_users(%s, %s)", (names, phones))
    conn.commit()
    cur.close()
    conn.close()

def delete(value):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("CALL delete_user(%s)", (value,))
    conn.commit()
    cur.close()
    conn.close()

def main():
    while True:
        print("\n1.Search\n2.Insert/Update\n3.Insert Many\n4.Paginate\n5.Delete\n0.Exit")
        choice = input("Choice: ")

        if choice == "1":
            search(input("Pattern: "))
        elif choice == "2":
            insert_or_update(input("Name: "), input("Phone: "))
        elif choice == "3":
            insert_many()
        elif choice == "4":
            paginate(int(input("Limit: ")), int(input("Offset: ")))
        elif choice == "5":
            delete(input("Name or phone: "))
        elif choice == "0":
            break

if __name__ == "__main__":
    main()