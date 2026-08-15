from collections import UserDict
from datetime import datetime, timedelta

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    # реалізація класу
		pass

class Phone(Field):
     def __init__(self, value):
          if not (len(value) == 10 and value.isdigit()):
            raise ValueError('Номер телефону має містити 10 цифр')
          super().__init__(value)

class Birthday(Field):
    def __init__(self, value):
        try:
            valid_date = datetime.strptime(value, '%d-%m-%Y').date()
            super().__init__(valid_date.strftime('%d.%m.%Y'))
        except ValueError:
            raise ValueError("Invalid date format. Use DD-MM-YYYY")        

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone_number):
         self.phones.append(Phone(phone_number))

    def remove_phone(self, phone_nunber):
         self.phones = [p for p in self.phones if p.value != phone_nunber]

    def edit_phone(self, old_number, new_number):
         phone_obj = self.find_phone(old_number)
         if not phone_obj:
              raise ValueError(f"Номер {old_number} не знайдено")

         new_phone = Phone(new_number)

         idx = self.phones.index(phone_obj)
         self.phones[idx] = new_phone

    def find_phone(self, phone_number):
         for p in self.phones:
              if p.value == phone_number:
                   return p
         return None

    def add_birthday(self, birthday_string):
        self.birthday = Birthday(birthday_string)
         
    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"

class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record  

    def find(self, name):
        return self.data.get(name)

    def delete(self, name):
        if name in self.data:
            del self.data[name]

    def get_upcoming_birthdays(self):
        today = datetime.today().date()
        upcoming_birthdays = []

        for record in self.data.values():
            if record.birthday is None:
                continue
            birthday = (record.birthday.value)
            
            # Беремо день народження в цьому році
            birthday_date = datetime.strptime(record.birthday.value, "%d.%m.%Y").date()
            birthday_this_year = birthday_date.replace(year=today.year)  

            
            # Якщо ДН у цьому році вже минув, беремо наступний рік
            if birthday_this_year < today:
                birthday_this_year = birthday_this_year.replace(year=today.year + 1)
                
            # Рахуємо різницю в днях
            days_until = (birthday_this_year - today).days
            
            # Перевіряємо, чи ДН протягом наступних 7 днів (включаючи сьогодні)
            if 0 <= days_until <= 6:
                congratulation_date = birthday_this_year
                
                # Якщо припадає на суботу (5) або неділю (6) — переносимо на понеділок
                if congratulation_date.weekday() == 5:
                    congratulation_date += timedelta(days=2)
                elif congratulation_date.weekday() == 6:
                    congratulation_date += timedelta(days=1)
                    
                # Додаємо у фінальний список
                upcoming_birthdays.append({
                    "name": record.name.value,
                    "congratulation_date": congratulation_date.strftime("%Y.%m.%d")
                })

        return upcoming_birthdays



def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            return "Give me name and phone please."
        except IndexError:
            return "Enter the argument for the command."
        except KeyError:
            return "Contact not found."

    return inner

def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args

@input_error
def add_contact(args, book):
    name, phone = args
    record = book.find(name)
    if record is None:
        record = Record(name)
        record.add_phone(phone)
        book.add_record(record)
        return('Contact added')
    else:
        record.add_phone(phone)
        return ('Phone added')


@input_error
def change_contact(args, book):
    name, old_phone, new_phone = args

    record = book.find(name)

    if record is None:
        raise KeyError

    record.edit_phone(old_phone, new_phone)

    return "Contact updated!"
    


@input_error
def show_phone(args, book):
    name = args[0]

    record = book.find(name)

    if record is None:
        raise KeyError

    return record


def show_all(args, book):
    if not book.data:
        return "No contacts saved."

    lines = []

    for name, record in book.data.items():
        lines.append(str(record))

    return "\n".join(lines)

@input_error
def add_birthday(args, book):
    name, birthday = args 
    record = book.find(name)
    if record is not None:
        record.add_birthday(birthday)
        return('Birthday added')
    else:
        return('Contact not found')

@input_error
def show_birthday(args, book):
    name = args[0]
    contact = book.find(name)
    if contact and contact.birthday:
        return contact.birthday.value
    else:
        return("Birthday not set for this contact.")

@input_error
def birthdays(args, book):
    return book.get_upcoming_birthdays()


def main():
    book = AddressBook()
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Good bye!")
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
            print(show_all(args, book))
        elif command == "add-birthday":
            print(add_birthday(args,book))
        elif command == "show-birthday":
            print(show_birthday(args, book))
        elif command == "birthdays":
            print(birthdays(args, book))
        else:
            print("Invalid command.")

if __name__ == "__main__":
    main()