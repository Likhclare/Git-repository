import json
import psycopg2
from connect import get_connection

# =========================
# ADD CONTACT (FULL)
# =========================
def add_contact():
    name = input("Name: ")
    email = input("Email: ")
    birthday = input("Birthday (YYYY-MM-DD): ")
    group = input("Group: ")

    conn = get_connection()
    cur = conn.cursor()

    # create/update contact
    cur.execute("CALL upsert_contact(%s, %s, %s, %s)", (name, email, birthday, group))

    # add phones
    while True:
        phone = input("Phone (or empty to stop): ")
        if not phone:
            break
        p_type = input("Type (home/work/mobile): ")
        cur.execute("CALL add_phone(%s, %s, %s)", (name, phone, p_type))

    conn.commit()
    cur.close()
    conn.close()
    print("Contact added.")


# =========================
# SEARCH
# =========================
def search_contacts():
    query = input("Search: ")
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM search_contacts(%s)", (query,))
    rows = cur.fetchall()

    for row in rows:
        print(row)

    cur.close()
    conn.close()


# =========================
# FILTER BY GROUP
# =========================
def filter_by_group():
    group = input("Enter group: ")
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT c.name, c.email, g.name
        FROM contacts c
        JOIN groups g ON c.group_id = g.id
        WHERE g.name = %s
    """, (group,))

    rows = cur.fetchall()
    for row in rows:
        print(row)

    cur.close()
    conn.close()


# =========================
# SORT
# =========================
def sort_contacts():
    print("1. Name\n2. Birthday")
    choice = input("Sort by: ")

    conn = get_connection()
    cur = conn.cursor()

    if choice == "1":
        cur.execute("SELECT name, email FROM contacts ORDER BY name")
    else:
        cur.execute("SELECT name, birthday FROM contacts ORDER BY birthday")

    rows = cur.fetchall()
    for row in rows:
        print(row)

    cur.close()
    conn.close()


# =========================
# PAGINATION LOOP
# =========================
def pagination_loop():
    limit = int(input("Limit: "))
    offset = 0

    conn = get_connection()
    cur = conn.cursor()

    while True:
        cur.execute("SELECT * FROM get_contacts_paginated(%s, %s)", (limit, offset))
        rows = cur.fetchall()

        print("\n--- PAGE ---")
        for row in rows:
            print(row)

        action = input("next / prev / quit: ").lower()

        if action == "next":
            offset += limit
        elif action == "prev":
            offset = max(0, offset - limit)
        elif action == "quit":
            break

    cur.close()
    conn.close()


# =========================
# EXPORT TO JSON
# =========================
def export_json():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT c.id, c.name, c.email, c.birthday, g.name
        FROM contacts c
        LEFT JOIN groups g ON c.group_id = g.id
    """)

    contacts = []

    for row in cur.fetchall():
        contact_id = row[0]

        contact = {
            "name": row[1],
            "email": row[2],
            "birthday": str(row[3]),
            "group": row[4],
            "phones": []
        }

        cur.execute("""
            SELECT phone, type FROM phones
            WHERE contact_id = %s
        """, (contact_id,))

        phones = cur.fetchall()
        for p in phones:
            contact["phones"].append({
                "number": p[0],
                "type": p[1]
            })

        contacts.append(contact)

    with open("contacts.json", "w", encoding="utf-8") as f:
        json.dump(contacts, f, indent=4)

    cur.close()
    conn.close()
    print("Exported to JSON.")


# =========================
# IMPORT FROM JSON
# =========================
def import_json():
    with open("contacts.json", encoding="utf-8") as f:
        data = json.load(f)

    conn = get_connection()
    cur = conn.cursor()

    for contact in data:
        name = contact["name"]

        cur.execute("SELECT id FROM contacts WHERE name=%s", (name,))
        exists = cur.fetchone()

        if exists:
            action = input(f"{name} exists. skip/overwrite? ")
            if action == "skip":
                continue

        cur.execute(
            "CALL upsert_contact(%s, %s, %s, %s)",
            (
                name,
                contact["email"],
                contact["birthday"],
                contact["group"]
            )
        )

        for phone in contact["phones"]:
            cur.execute(
                "CALL add_phone(%s, %s, %s)",
                (name, phone["number"], phone["type"])
            )

    conn.commit()
    cur.close()
    conn.close()
    print("Imported from JSON.")


# =========================
# DELETE
# =========================
def delete_contact():
    choice = input("Delete by name/phone: ")
    value = input("Value: ")

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("CALL delete_contact_proc(%s, %s)", (value, choice))

    conn.commit()
    cur.close()
    conn.close()
    print("Deleted.")


# =========================
# MAIN MENU
# =========================
def main():
    while True:
        print("\n--- PHONEBOOK TSIS ---")
        print("1. Add contact")
        print("2. Search")
        print("3. Filter by group")
        print("4. Sort")
        print("5. Pagination")
        print("6. Export JSON")
        print("7. Import JSON")
        print("8. Delete")
        print("0. Exit")

        choice = input("Choose: ")

        if choice == "1":
            add_contact()
        elif choice == "2":
            search_contacts()
        elif choice == "3":
            filter_by_group()
        elif choice == "4":
            sort_contacts()
        elif choice == "5":
            pagination_loop()
        elif choice == "6":
            export_json()
        elif choice == "7":
            import_json()
        elif choice == "8":
            delete_contact()
        elif choice == "0":
            break
        else:
            print("Invalid choice")


if __name__ == "__main__":
    main()