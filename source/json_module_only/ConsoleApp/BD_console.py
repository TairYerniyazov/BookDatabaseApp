# ========================================== BAZA DANYCH KSIĄŻEK ===================================================
# ============================ <IMPLEMENTACJA>: BEZPOŚREDNIA PRACA Z JSON'em =======================================
# ====================================== <WERSJA>: KONSOLA (bez GUI) ===============================================

import json

# Ścieżka do pliku, w którum przechowujemy listę książek
data_source = "../../../data/books.json"


def load_json(filepath):
    """Funkcja zwracające listę książek pobraną z pliku JSON"""
    with open(filepath, "r", encoding='utf-8') as file:
        data = json.load(file)
        return data


def upload_json(filepath, data):
    """Funkcja zapisująca zaktualizowaną listę książek do pliku JSON"""
    with open(filepath, "w") as file:
        json.dump(data, file, indent=2)


def show_books():
    """Funkcja wyświetlająca listę wszystkich książek zawartych w bazie danych"""
    books = load_json(data_source)
    print("")
    for index in range(0, len(books)):
        show_book(books[index], index, True)


def show_book(book, index, index_display):
    """Funkcja wyświetlająca dane książki podanej jako argument w postaci elementu"""
    if index_display:
        print(f'\033[4mKsiążka #{index + 1}:\033[0m')
    print(f'\t\033[1mNazwa:\033[0m {book["Nazwa"]}\n'
          f'\t\033[1mAutor\033[0m: {book["Autor"]}\n'
          f'\t\033[1mRok wydania\033[0m: {book["Rok wydania"]}\n'
          f'\t\033[1mISBN\033[0m: {book["ISBN"]}')


def get_book(books, name):
    """Funkcja wyszukująca książkę po nazwie. Zwraca książkę jako element
    lub None w przypadku, gdy szukanej książki nie ma w bazie danych"""
    foundBook = None
    for book in books:
        if book["Nazwa"] == name:
            foundBook = book
    return foundBook


def find_book():
    """Funkcja próbująca znaleść książkę, by wyświetlić jej szczegółowe dane"""
    books = load_json(data_source)
    name = input("\nProszę wprowadzić nazwę książki: ")
    foundBook = get_book(books, name)
    if foundBook is None :
        print(f"Nie udało się znaleść książki o nazwie {name}.")
    else:
        print(f"\n\033[4m\033[1mZnaleziono książkę:\033[0m\033[0m\n")
        show_book(foundBook, 0, False)


def insert_book():
    """Funkcja dodająca nową książkę do bazy danych"""
    books = load_json(data_source)
    newBook = {}
    print("\n\033[4m\033[1mWprowadź dane nowej książki:\033[0m\033[0m")
    newBook["Nazwa"] = input("Nazwa: ")
    newBook["Autor"] = input("Autor: ")
    newBook["Rok wydania"] = int(input("Rok wydania: "))
    newBook["ISBN"] = input("ISBN: ")
    books.append(newBook)
    upload_json(data_source, books)


def remove_book():
    """Funkcja usuwająca książkę z listy na podstawie wskazanego numera"""
    books = load_json(data_source)
    while True:
        if len(books) == 0:
            print("\nLista jest pusta")
            return None
        try:
            number = int(input("\nWprowadź numer książki, którą chcesz usunąć lub 0,\n"
                                          "by wrócić do listy dostępnych operacji: "))
            if number < 0 or number > len(books):
                print(f"\nTrzeba wprowadzić numer od 0 do {len(books)}")
            elif number != 0:
                index = 0
                number = number - 1
                for book in books:
                    if number == index:
                        name = book["Nazwa"]
                        del books[index]
                        upload_json(data_source, books)
                        print(f'\nKsiążka o nazwie "{name}" została usunięta.\n'
                              'Numery są zaktualizowane.')
                        return None
                    index = index + 1
            else:
                break
        except:
            print("\nTrzeba wprowadzić numer książki na liście.\n"
                  "Sprawdź numer za pomocą \"Listowania\" lub \"Wyszukiwania\".")


def info_prompt():
    """Funkcja wyświetlająca dostępne komendy w terminalu"""
    print("\nDostępne działania:"
          "\n\t[1] -> Listowanie"
          "\n\t[2] -> Wyszukiwanie"
          "\n\t[3] -> Wstawianie"
          "\n\t[4] -> Usuwanie"
          "\n\t[5] -> Zamknięcie bazy danych\n")


def main():
    """Główna funkcja uruchamiająca cały program"""
    while True:
        print("\n============== BAZA DANYCH KSIĄŻEK ==============")
        info_prompt()
        userChoice = 0
        try:
            userChoice = int(input("Wybierz działanie na bazie danych: "))
        except:
            print("Trzeba wprowadzić liczbę (1-4) odpowiadającą działaniu.\n"
                  "Spróbuj ponownie.")
        match userChoice:
            case 1:
                show_books()
            case 2:
                find_book()
            case 3:
                insert_book()
            case 4:
                remove_book()
            case 5:
                break
            case _:
                pass


# Uruchomienie funkcji main() po uruchomieniu programu
if __name__ == "__main__":
    main()