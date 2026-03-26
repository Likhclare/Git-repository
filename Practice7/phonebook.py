import csv
from connect import get_connection, create_table

create_table()

def insert_from_csv(filename):
    conn = get_connection()
    if conn is None:
        return
    cur = conn.cursor()
    with open(filename, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            cur.execute(
                "INSERT INTO contacts (name, phone) VALUES (%s, %s)",
                (row['name'], row['phone'])
            )
    conn.commit()
    cur.close()
    conn.close()
    print("Данные из CSV добавлены.")

def insert_from_console():
    name = input("Введите имя: ")
    phone = input("Введите телефон: ")
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO contacts (name, phone) VALUES (%s, %s)",
        (name, phone)
    )
    conn.commit()
    cur.close()
    conn.close()
    print("Контакт добавлен.")

def update_contact():
    name = input("Введите имя контакта для обновления: ")
    new_name = input("Новое имя (оставьте пустым, если не менять): ")
    new_phone = input("Новый телефон (оставьте пустым, если не менять): ")

    conn = get_connection()
    cur = conn.cursor()
    if new_name:
        cur.execute("UPDATE contacts SET name=%s WHERE name=%s", (new_name, name))
    if new_phone:
        cur.execute("UPDATE contacts SET phone=%s WHERE name=%s", (new_phone, name))
    conn.commit()
    cur.close()
    conn.close()
    print("Контакт обновлен.")

def query_contacts():
    print("1. По имени\n2. По префиксу телефона\n3. Все контакты")
    choice = input("Выберите фильтр: ")
    conn = get_connection()
    cur = conn.cursor()
    if choice == "1":
        name = input("Введите имя: ")
        cur.execute("SELECT * FROM contacts WHERE name=%s", (name,))
    elif choice == "2":
        prefix = input("Введите префикс телефона: ")
        cur.execute("SELECT * FROM contacts WHERE phone LIKE %s", (prefix+'%',))
    else:
        cur.execute("SELECT * FROM contacts")
    rows = cur.fetchall()
    for row in rows:
        print(row)
    cur.close()
    conn.close()

def delete_contact():
    print("Удалить по имени или телефону?")
    choice = input("Введите 'name' или 'phone': ")
    value = input("Введите значение: ")
    conn = get_connection()
    cur = conn.cursor()
    if choice == "name":
        cur.execute("DELETE FROM contacts WHERE name=%s", (value,))
    else:
        cur.execute("DELETE FROM contacts WHERE phone=%s", (value,))
    conn.commit()
    cur.close()
    conn.close()
    print("Контакт удален.")

def main():
    while True:
        print("\n--- PhoneBook ---")
        print("1. Добавить контакт из CSV")
        print("2. Добавить контакт вручную")
        print("3. Обновить контакт")
        print("4. Показать контакты")
        print("5. Удалить контакт")
        print("0. Выход")
        choice = input("Выберите действие: ")

        if choice == "1":
            insert_from_csv("contacts.csv")
        elif choice == "2":
            insert_from_console()
        elif choice == "3":
            update_contact()
        elif choice == "4":
            query_contacts()
        elif choice == "5":
            delete_contact()
        elif choice == "0":
            break
        else:
            print("Неверный выбор!")

if __name__ == "__main__":
    main()