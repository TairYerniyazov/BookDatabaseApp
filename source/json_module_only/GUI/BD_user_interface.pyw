# ========================================== BAZA DANYCH KSIĄŻEK ===================================================
# ============================ <IMPLEMENTACJA>: BEZPOŚREDNIA PRACA Z JSON'em =======================================
# ====================================== <WERSJA>: GUI (CUSTOM_TKINTER) ============================================

# Import biblioteki CustomTkinter
import customtkinter

# Import biblioteki umożliwającej pracę ze zdjęciami
from PIL import Image, ImageTk

# Moduł pozwalający na interakcję z plikami formatu JSON
import json

# Ścieżka do pliku, w którym przechowujemy listę książek
data_source = "../../../data/books.json"

# Typ operacji (ustawiany przez przyciski)
mode = "default"

# Zmienna pomocnicza
newBook = {}


def ask_to_enter_input(option):
    """Funkcja prosząca użytkownika o wprowadzenie danych"""
    global mode
    mode = option
    unlock_and_clear_text_box(info_widget)
    match option:
        case "find":
            info_widget.insert("0.0", "Proszę wprowadzić nazwę książki,\n którą należy znaleźć", "centerAlignment")
        case "add_name":
            info_widget.insert("0.0", "Proszę wprowadzić nazwę", "centerAlignment")
        case "add_author":
            info_widget.insert("0.0", "Proszę wprowadzić autora", "centerAlignment")
        case "add_year":
            info_widget.insert("0.0", "Proszę wprowadzić rok wydania", "centerAlignment")
        case "add_ISBN":
            info_widget.insert("0.0", "Proszę wprowadzić ISBN", "centerAlignment")
        case "delete":
            info_widget.insert("0.0", "Proszę wprowadzić numer książki,\n którą należy usunąć", "centerAlignment")
            show_books()
        case "default":
            info_widget.insert("0.0", "Proszę wybrać działanie", "centerAlignment")

    lock_text_box(info_widget)


def change_database():
    """Funkcja wykonująca różne akcje po naciśnięciu przycisku OK"""
    global mode
    global newBook
    books = load_json(data_source)
    user_input = entry.get()
    unlock_and_clear_text_box(info_widget)
    match mode:
        case "find":
            found_book = get_book(books, user_input)
            if found_book is None:
                info_widget.insert("0.0", "Nie ma książki o takiej nazwie", "centerAlignment")
            else:
                info_widget.insert("0.0", "Znaleziono", "centerAlignment")
                unlock_and_clear_text_box(text_widget)
                show_book(found_book, 0, False)
                lock_text_box(text_widget)
            mode = "default"
            entry.delete('0', 'end')
        case "add_name":
            newBook.clear()
            newBook["Nazwa"] = user_input
            mode = "add_author"
            entry.delete('0', 'end')
            ask_to_enter_input(mode)
        case "add_author":
            newBook["Autor"] = user_input
            mode = "add_year"
            entry.delete('0', 'end')
            ask_to_enter_input(mode)
        case "add_year":
            newBook["Rok wydania"] = int(user_input)
            mode = "add_ISBN"
            entry.delete('0', 'end')
            ask_to_enter_input(mode)
        case "add_ISBN":
            newBook["ISBN"] = user_input
            mode = "default"
            entry.delete('0', 'end')
            books.append(newBook)
            upload_json(data_source, books)
            info_widget.insert("0.0", "Dodano nową książkę", "centerAlignment")
            newBook = ""
        case "delete":
            if len(books) == 0:
                info_widget.insert("0.0", "Lista jest pusta", "centerAlignment")
                mode = "default"
                lock_text_box(info_widget)
                entry.delete('0', 'end')
                return None
            try:
                number = int(user_input)
                if number < 0 or number > len(books):
                    info_widget.insert("0.0", f"Trzeba wprowadzić numer od 0 do {len(books)}", "centerAlignment")
                elif number != 0:
                    index = 0
                    number = number - 1
                    for book in books:
                        if number == index:
                            name = book["Nazwa"]
                            del books[index]
                            upload_json(data_source, books)
                            info_widget.insert("0.0", f'Książka o nazwie "{name}" została usunięta. '
                                                      'Numery są zaktualizowane.', "centerAlignment")
                            show_books()
                            mode = "default"
                            lock_text_box(info_widget)
                            entry.delete('0', 'end')
                            return None
                        index = index + 1
            except:
                info_widget.insert("0.0", "Trzeba wprowadzić numer książki na liście. "
                      "Sprawdź numer za pomocą \"Listowania\" lub \"Wyszukiwania\".")
        case "default":
            ask_to_enter_input(mode)

    lock_text_box(info_widget)


def entry_shortcut(event):
    """Funkcja obsługująca zdarzenie naciśnięcia klawisza Return"""
    if event.keysym == "Return":
        change_database()


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
    unlock_and_clear_text_box(text_widget)
    for index in range(0, len(books)):
        show_book(books[index], index, True)
    lock_text_box(text_widget)


def unlock_and_clear_text_box(text_box):
    """Funkcja, która odblokowuje i wyczyszcza wskazane pole tekstowe"""
    text_box.configure(state='normal')
    text_box.delete('1.0', 'end')


def lock_text_box(text_box):
    """Funkcja blokująca wskazane pole tekstowe"""
    text_box.configure(state='disabled')


def show_book(book, index, index_display):
    """Funkcja wyświetlająca dane książki podanej jako argument w postaci elementu"""
    if index_display:
        stringWithIndex = f'Książka #{index + 1}:\n'
        text_widget.insert(customtkinter.END, stringWithIndex)
    stringWithData = f'Nazwa: {book["Nazwa"]}\n' \
                     f'Autor: {book["Autor"]}\n' \
                     f'Rok wydania: {book["Rok wydania"]}\n' \
                     f'ISBN: {book["ISBN"]}\n\n'
    text_widget.insert(customtkinter.END, stringWithData)


def get_book(books, name):
    """Funkcja wyszukująca książkę po nazwie. Zwraca książkę jako element
    lub None w przypadku, gdy szukanej książki nie ma w bazie danych"""
    foundBook = None
    for book in books:
        if book["Nazwa"] == name:
            foundBook = book
    return foundBook


# Definiowanie trybu wyświetlania (tryb ciemny, kolor zielony)
customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue")

# Generowanie oraz konfigurowanie głównego okna
root = customtkinter.CTk()
root.resizable(0,0)
root.geometry("800x600")
root.title("Baza danych książek")

# Tworzenie głównej ramki
wrapper_frame = customtkinter.CTkFrame(master=root, fg_color=("white", "black"), border_color=("#0E4C92", "black"),
                                       border_width=2)
wrapper_frame.pack(pady=20, padx=50, fill="both", expand=True)
wrapper_frame_first_child = customtkinter.CTkFrame(master=wrapper_frame, fg_color="transparent")
wrapper_frame_second_child = customtkinter.CTkFrame(master=wrapper_frame, fg_color="transparent")
wrapper_frame_first_child.pack(padx=5, fill="x", expand=True)
wrapper_frame_first_child.columnconfigure(0, weight=1)
wrapper_frame_first_child.columnconfigure(1, weight=1)
wrapper_frame_second_child.pack(padx=5, fill="x", expand=True)

# Tworzenie napisu głównego
custom_font_bold = ("Comic Sans MS", 20, "bold")
main_label = customtkinter.CTkLabel(master=wrapper_frame_first_child, text="BAZA DANYCH KSIĄŻEK", font=custom_font_bold)
main_label.grid(row=0, column=1, sticky=customtkinter.W, padx=(20, 5), pady=(10, 0))

# Tworzenie pola do wyświetlania danych
text_widget = customtkinter.CTkTextbox(wrapper_frame_second_child, width=350, height=395, wrap='word', fg_color=("#0E4C92", "black"),
                                       border_color="white", border_width=1, text_color=("white", "white"))
text_widget.pack(side="left", pady=(0, 5), padx=(10, 0))
text_widget.configure(state='disabled')

# Tworzenie ramki zawierającej przyciski
button_frame = customtkinter.CTkFrame(master=wrapper_frame_second_child, width=200, height=450, corner_radius=10,
                                      fg_color=("#0E4C92", "black"))
button_frame.pack(side="top", padx=10)
button_frame.columnconfigure(0, weight=1)
button_frame.columnconfigure(1, weight=1)

# Tworzenie przycisków
button1 = customtkinter.CTkButton(master=button_frame, text="Listowanie", command=show_books, fg_color=("transparent"),
                                  border_color="white", border_width=2, corner_radius=10)
button1.grid(row=0, column=0, sticky=customtkinter.W+customtkinter.E, padx=(20, 5), pady=(15, 5))

button2 = customtkinter.CTkButton(master=button_frame, text="Wyszukiwanie", command= lambda: ask_to_enter_input("find"),
                                  fg_color=("transparent"), border_color="white", border_width=2, corner_radius=10)
button2.grid(row=0, column=1, sticky=customtkinter.W+customtkinter.E, padx=(10, 20), pady=(15, 5))

button3 = customtkinter.CTkButton(master=button_frame, text="Dodawanie", command= lambda: ask_to_enter_input("add_name"),
                                  fg_color=("transparent"), border_color="white", border_width=2, corner_radius=10)
button3.grid(row=1, column=0, sticky=customtkinter.W+customtkinter.E, padx=(20, 5), pady=5)

button4 = customtkinter.CTkButton(master=button_frame, text="Usuwanie", command= lambda: ask_to_enter_input("delete"),
                                  fg_color=("transparent"), border_color="white", border_width=2, corner_radius=10)
button4.grid(row=1, column=1, sticky=customtkinter.W+customtkinter.E, padx=(10, 20), pady=5)

button5 = customtkinter.CTkButton(master=button_frame, text="Ok", command=change_database,
                                  fg_color=("transparent"), border_color="white", border_width=2, corner_radius=10)
button5.grid(row=5, column=0, columnspan=2, sticky=customtkinter.W+customtkinter.E, padx=20, pady=(5, 20))

# Tworzenie pola do wprowadzenia danych
entry = customtkinter.CTkEntry(master=button_frame, placeholder_text="")
entry.bind("<KeyPress>", entry_shortcut)
entry.grid(row=4, column=0, columnspan=2, sticky=customtkinter.W+customtkinter.E, pady=(0, 5), padx=10)

# Tworzenie napisu informacyjnego
custom_font_light = ("Comic Sans MS", 15)
info_widget = customtkinter.CTkTextbox(button_frame, width=300, height=100, fg_color=("white", "#3E4149"),
                                       font=custom_font_light, wrap='word')
info_widget.grid(row=3, column=0, columnspan=2, sticky=customtkinter.W+customtkinter.E, pady=(10, 10), padx=10)
info_widget.configure(state='disabled')
info_widget.tag_config("centerAlignment", justify="center")

# Zdjęcie (logo UJ)
logo_image = customtkinter.CTkImage(light_image=Image.open("Images/Light_logo.png"),
                                    dark_image=Image.open("Images/Dark_logo.png"), size=(100, 100))
logo_image_object = customtkinter.CTkLabel(master=wrapper_frame_first_child, image=logo_image, text="")
logo_image_object.grid(row=0, column=0, sticky=customtkinter.W+customtkinter.E, padx=(30, 5), pady=(20, 0))

root.mainloop()
