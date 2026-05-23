
from collections import UserDict
from datetime import datetime, timedelta
import pickle

def save_data(book, filename="addressbook.pkl"):
    with open(filename, "wb") as f:
        pickle.dump(book, f)

def load_data(filename="addressbook.pkl"):
    try:
        with open(filename, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return AddressBook()  # Повернення нової адресної книги, якщо файл не знайдено

# Базовий клас для полів запису.
class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

# Клас для зберігання імені контакту. Обов'язкове поле.
class Name(Field):
    # реалізація класу
		pass

# Клас для зберігання номера телефону. Має валідацію формату (10 цифр).
class Phone(Field):
    # Реалізовано валідацію номера телефону (має бути перевірка на 10 цифр).
    def __init__(self, value):
             if len(value) == 10:
                  self.value = value
             else:
                  raise Exception("Phone must be 10 digits only")
                  
class Birthday(Field):
    def __init__(self, value):
        try:
            # перевірка коректності даних та перетворення рядка на об'єкт datetime
            self.value = datetime.strptime(value, "%d.%m.%Y")
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")

# Клас для зберігання інформації про контакт, включно з іменем та списком телефонів.
class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones: list[Phone] = []
        self.birthday = None # Birthday
        
    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"
    
# Додавання записів add_phone
    def add_phone(self, phone):
        self.phones.append(Phone(phone)) 

    # редагування — edit_phone
    def edit_phone(self, old_phone, new_phone):
         for p in self.phones:
            if p.value == old_phone:
                 index = self.phones.index(p)
                 self.phones[index] = Phone(new_phone)
                 
    # пошуку об'єктів Phone — find_phone.      
    def find_phone(self, phone):
          for p in self.phones:
               if p.value == phone:
                    return p.value
    
    # видалення — remove_phone
    def remove_phone(self, phone):
          for p in self.phones:
               if p.value == phone:
                     self.phones.remove(p)
           
    # Додайте функціонал роботи з Birthday у клас Record, а саме функцію add_birthday,
    #  яка додає день народження до контакту.
    def add_birthday(self, value):
        self.birthday = Birthday(value)

# AddressBook: Клас для зберігання записів та керування ними.
class AddressBook(UserDict):
    
    # Реалізовано метод add_record, який додає запис до self.data.
    def add_record(self, info: Record):
        self.data[info.name.value] = info
    
    # Реалізовано метод find, який знаходить запис за ім'ям.
    def find(self, name):
         return self.data.get(name)    
         
    # Реалізовано метод delete, який видаляє запис за ім'ям.
    def delete(self, name):
          if self.data[name]:
            del self.data[name]
            return "Record has been deleted"
          else:
              return "No such name in the book"

    # Реалізовано метод, який для контактів адресної книги повертає список користувачів,
    #  яких потрібно привітати по днях на наступному тижні.
    
# Функція визначає дні народження на наступні 7 днів включаючи поточний день. 
# Якщо день народження припадає на вихідний, дата привітання переноситься на наступний понеділок.

    def get_upcoming_birthdays(self):
     # Створення порожнього списку для зберігання результатів.
        list = []
    # Визначення поточної дати
        today = datetime.today().date() 

        # Для встановлення дати самостійно (для перевірки , замість поперодньої)
        #today = datetime(year=2026, month=12, day=26).date()

        # Aналізування дати народження для кожного користувача
        for key, record in self.data.items():
            # Конвертування дати народження із рядка у datetime об'єкт, без часу.
            birthday = datetime.strptime(str(record.birthday), "%Y-%m-%d %H:%M:%S").date()
            #
            birthday_date = birthday.strftime("%Y-%m-%d")
            # Визначення дня народження у цьому році
            birthday_this_year = birthday.replace(year=today.year)
            # Отримання номера дня тижня,  Поверне число від 0 (понеділок) до 6 (неділя)
            day_of_week = birthday_this_year.weekday()


            # Перевірка, якщо день народження у цьому році ще не наступив
            if birthday_this_year > today:
                # Визначення різниці між днем народження та поточним днем
                diff_days = birthday_this_year - today
                # Перевірка, чи день народження у найближчи 7 днів
                if diff_days < timedelta(days=7):
                    # Перевірка чи день народження у суботу
                    if day_of_week == 5:
                        # Перенос дати привітання на два дня(на понеділок)
                        datetime_object = birthday_this_year + timedelta(days=2)
                        congratulation_date = datetime_object.strftime("%Y-%m-%d")
                        
                    # Перевірка чи день народження у неділю
                    if day_of_week == 6:
                        # Перенос дати привітання на один день(на понеділок)
                        datetime_object = birthday_this_year + timedelta(days=1)
                        congratulation_date = datetime_object.strftime("%Y-%m-%d")
                        
                    # Якщо, день народження в інші дні тижня(крім суботи та неділі)
                    else:
                        datetime_object= birthday_this_year + timedelta(days=0)
                        congratulation_date = datetime_object.strftime("%Y-%m-%d")
                    # Додавання у список ногого словника, з ключами name, birthday, day_of_week та congratulation_date
                    list.append({"name": key, "birthday": birthday_date, "day_of_week": day_of_week, "congratulation_date": congratulation_date})


            # Якщо  вже минув день народження у цьому році(але поточна дата перевірки з 26 грудня до кінця року та день народження в наступному році) 
            else:
                # Розглядання дати народження на наступний рік
                birthday_next_year = birthday.replace(year=today.year+1)
                # Визначення різниці між днем народження та поточним днем 
                diff_days = birthday_next_year - today
                # Перевірка, чи день народження у найближчи 7 днів, для випадку якщо поточна дата перевірки з 26 грудня до кінця року.
                if diff_days < timedelta(days=7):
                    # Отримання номера дня тижня,  Поверне число від 0 (понеділок) до 6 (неділя)
                    day_of_week = birthday_this_year.weekday()
                    # Перевірка чи день народження у суботу
                    if day_of_week == 5:
                        # Перенос дати привітання на два дня(на понеділок)
                        datetime_object = birthday_this_year + timedelta(days=2)
                        congratulation_date = datetime_object.strftime("%Y-%m-%d")
                        
                    # Перевірка чи день народження у неділю
                    if day_of_week == 6:
                        # Перенос дати привітання на один день(на понеділок)
                        datetime_object = birthday_this_year + timedelta(days=1)
                        congratulation_date = datetime_object.strftime("%Y-%m-%d")
                    # Якщо, день народження в інші дні тижня(крім суботи та неділі)
                    else:
                        datetime_object= birthday_this_year + timedelta(days=0)
                        congratulation_date = datetime_object.strftime("%Y-%m-%d")

                    # Додавання у список ногого словника, з ключами name, birthday, day_of_week та congratulation_date
                    list.append({"name": key, "birthday": birthday_date, "day_of_week": day_of_week, "congratulation_date": congratulation_date})

                    
        # Повернення списку словників, де кожен словник містить ключі name, birthday, day_of_week
        #  та congratulation_date, якщо виконуються умови 
        return list

def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError as e:
            return repr(e)
        except ValueError as e:
            return repr(e)
        except IndexError as e :
            return repr(e)
        except Exception as e:
            return repr(e)
    return inner

# Бот не чутливий до регістру введених команд.
def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args

# Параметри функції — це список аргументів args і сама адресна книга book.
# Додати або новий контакт з іменем і телефонним номером,
#  або телефонний номер до контакту, який уже існує.
@input_error
def add_contact(args, book: AddressBook):
    name, phone, *_ = args
    record = book.find(name)
    message = "Contact updated."
    if record is None:
        record = Record(name)
        book.add_record(record)
        message = "Contact added."
    if phone:
        record.add_phone(phone)
    return message

# Виведення всіx контактів в адресній книзі.
@input_error
def show_all(book: AddressBook):
    for name, record in book.data.items():
         print(record)

# Виведення телефонних номерів для вказаного контакту.
@input_error
def show_phone(args, book):
    name, *_ = args
    for key, record in book.data.items():
        if key == name:
            return record
    else:
        return "No such contact."
    
# Змінити телефонний номер для вказаного контакту.
@input_error
def change_contact(args, book):
    name, old_phone, new_phone, *_ = args
    record = book.find(name)
    if record is None:
        return "No such contact."
    else:
        record.edit_phone(old_phone, new_phone)
        return "Contact updated."

# Додає дату народження для вказаного контакту.
@input_error
def add_birthday(args, book):
    name, birthday, *_  = args
    record = book.find(name)
    if record is not None:
        record.add_birthday(birthday)
        message = "Birthday added."
    else:
        message = "No such contact."
    return message

# Показує дату народження для вказаного контакту.
@input_error
def show_birthday(args, book):
    name, *_  = args
    record = book.find(name)
    if record is not None:
        for key, record in book.data.items():
            if key == name:
                date_object = datetime.strptime(str(record.birthday), "%Y-%m-%d %H:%M:%S")
                return date_object.strftime("%d.%m.%Y")
    else:
        return "No such contact."
    
#  Показує дні народження, які відбудуться протягом наступного тижня.
@input_error
def birthdays(args, book):
    return book.get_upcoming_birthdays()


# Програма повинна мати функцію main(), яка управляє основним циклом обробки команд.
def main():
    book = load_data()
    print("Welcome to the assistant bot!")
    # Бот повинен перебувати в нескінченному циклі, чекаючи команди користувача.
    while True:
        try:
            user_input = input("Enter a command: ")
            command, *args = parse_input(user_input)
        # Бот завершує свою роботу, якщо зустрічає слова: "close" або "exit".
            if command in ["close", "exit"]:
                print("Good bye!")
                save_data(book)  
                break
            
            elif command == "hello":
                print("How can I help you?")

            elif command == "add":
                print(add_contact(args, book))
                
            elif command == "change":
                print(change_contact(args, book))

            elif command == "phone":
                print(show_phone(args, book))

            elif command == "all":
                show_all(book)
                
            elif command == "add-birthday":
                print(add_birthday(args, book))

            elif command == "show-birthday":
                print(show_birthday(args, book))
                
            elif command == "birthdays":
                print(birthdays(args, book))
                
            else:
                print("Invalid command.")
        except KeyboardInterrupt:
            save_data(book) 

if __name__ == "__main__":
    main()