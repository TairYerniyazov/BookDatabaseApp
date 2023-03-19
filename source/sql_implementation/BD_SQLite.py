# ========================================== BAZA DANYCH KSIĄŻEK ===================================================
# ======================================= <IMPLEMENTACJA>: SQLite ==================================================
# ====================================== <WERSJA>: KONSOLA (bez GUI) ===============================================
# Importujemy bibliotekę SQLite
import sqlite3
import json

defaultTable = "main"
json_file = "../../data/booksExportedFromSQL.json"

def initiate_table(connection):
    """Funkcja inicjalizująca tabelę """
    query = f"CREATE TABLE {defaultTable} (" \
            f"name text," \
            f"author text," \
            f"year integer," \
            f"isbn text UNIQUE);"
    execute_query(query, connection)


def execute_query(query, connection):
    """Funkcja wykonująca polecenia SQL """
    # Tworzenia kursora do zmiany bazy
    cursor = connection.cursor()
    cursor.execute(query)
    # Zatwierdzamy zmiany
    connection.commit()
    return cursor


def show_books(connection, collection):
    """Funkcja wyświetlająca wszystkie książki"""
    query = f"SELECT * FROM {collection};"
    books = execute_query(query, connection).fetchall()
    if len(books) == 0:
        print(f'\n\033[1mNa liście nie ma żadnych książek.\033[0m')
    else:
        index = 1
        for book in books:
            print(f'\n\033[4m\033[1mKsiążka #{index}:\033[0m\033[0m\n'
                  f'Nazwa: {book[0]}\n'
                  f'Autor: {book[1]}\n'
                  f'Rok wydania: {book[2]}\n'
                  f'ISBN: {book[3]}')
            index += 1
        print("")


def find_book(connection, collection):
    """Funkcja znajdująca książkę w bazie danych"""
    name = input("\nWprowadź nazwę książki, którą należy znaleść: ")
    query = f"SELECT * FROM {collection} WHERE name LIKE '{name}' LIMIT 1;"
    result = execute_query(query, connection).fetchall()
    if len(result) == 0:
        print(f'\n\033[1mNie znaleziono książki o nazwie "{name}"\033[0m')
    else:
        book = result[0]
        print(f'\n\033[4m\033[1mZnaleziono książkę:\033[0m\033[0m\n'
              f'Nazwa: {book[0]}\n'
              f'Autor: {book[1]}\n'
              f'Rok wydania: {book[2]}\n'
              f'ISBN: {book[3]}\n')


def insert_book(connection, collection):
    """Funkcja dodająca nową książkę do bazy danych"""
    name = input("\nWprowadź nazwę nowej książki: ")
    author = input("Wprowadź autora: ")
    try:
        year = int(input("Wprowadź rok wydania: "))
    except:
        print(">>> Niepoprawne dane wejściowe.")
        return None
    isbn = input("Wprowadź identyfikator ISBN: ")
    if not isbn.isnumeric():
        print(">>> Niepoprawne dane wejściowe.")
        return None
    query = f"INSERT INTO {collection} VALUES {name, author, year, isbn};"
    try:
        execute_query(query, connection)
        print(f"\n\033[4m\033[1mDodano nową książkę o nazwie \"{name}\".\033[0m\033[0m\n")
    except:
        print(">>> Książka o podanym numerze ISBN znajduje się już na liście.\n")


def remove_book(connection, collection):
    """Funkcja usuwająca książkę z bazy danych"""
    name = input("\nWprowadź nazwę książki, którą należy usunąć: ")
    query = f"DELETE FROM {collection} WHERE name LIKE '{name}';"
    result = execute_query(query, connection).rowcount
    if result < 1:
        print(f'\n\033[1mNie znaleziono książki o nazwie "{name}".\033[0m')
    else:
        print(f'\n\033[1mUsunięto książkę o nazwie "{name}".\033[0m')


def export_to_json(connection, collection):
    """Funkcja eksportująca dane do pliku JSON"""
    query = f"SELECT * FROM {collection};"
    books = execute_query(query, connection).fetchall()
    if len(books) == 0:
        print(f'\n\033[1mNie ma danych do eksportu.\033[0m')
    else:
        with open(json_file, "w") as file:
            json.dump(books, file, indent=2)
        print(f'\n\033[1mDane zostały zapisane do pliku JSON.\n\033[0m')


def info_prompt():
    """Funkcja wyświetlająca dostępne komendy w terminalu"""
    print("\nDostępne działania:"
          "\n\t[1] -> Listowanie"
          "\n\t[2] -> Wyszukiwanie"
          "\n\t[3] -> Wstawianie"
          "\n\t[4] -> Usuwanie"
          "\n\t[5] -> Eksport kolekcji do pliku JSON"
          "\n\t[6] -> Zamknięcie bazy danych\n")


def main():
    """Główna funkcja uruchamiająca cały program"""

    # Obiekt reprezuntający połączenie z bazą danych przechowywaną w lokalnym pliku
    connection = sqlite3.connect('../../data/books.db')

    # ======== Pierwotna inicjalizacja tablicy ======
    # initiate_table(connection)
    # ===============================================

    while True:
        print("\n============== BAZA DANYCH KSIĄŻEK ==============")
        print("================ SQLite (sqlite3) ===============")

        info_prompt()
        userChoice = 0
        try:
            userChoice = int(input("Wybierz działanie na bazie danych: "))
        except:
            print("Trzeba wprowadzić liczbę (1-4) odpowiadającą działaniu.\n"
                  "Spróbuj ponownie.")
        match userChoice:
            case 1:
                show_books(connection, defaultTable)
            case 2:
                find_book(connection, defaultTable)
            case 3:
                insert_book(connection, defaultTable)
            case 4:
                remove_book(connection, defaultTable)
            case 5:
                export_to_json(connection, defaultTable)
            case 6:
                break
            case _:
                pass

    # Zamykamy bazę danych (połączenie)
    connection.close()

# Uruchomienie funkcji main() po uruchomieniu programu
if __name__ == "__main__":
    main()
