import re
import csv


dirty_names_list = []
names_list = []
lastname_list = []
firstname_list = []
surname_list = []
org_list = []
position_list = []
phone_list = []
new_phone_list = []
email_list = []
contacts = []
final_list = []


def split_names():
    for contact in contacts_list:
        name = contact[0] + ' ' + contact[1] + ' ' + contact[2]
        dirty_names_list.append(name)

    for name in dirty_names_list:
        result = re.split('\s', name)
        names_list.append(result)

    for name in names_list:
        lastname_list.append(name[0])
        firstname_list.append(name[1])
        surname_list.append(name[2])


def split_other():
    for row in contacts_list:
        org_list.append(row[3])
        position_list.append(row[4])
        phone_list.append(row[5])
        email_list.append(row[6])


def change_phone_format():
    pattern = re.compile(r'(\+7|8)\s*\(?(\d+)\)?[\s-]?(\d+)[-]?(\d+)[-]?(\d+)\s*\(?(доб.)?\s*(\d+)?\)?')
    for item in phone_list:
        if '(' and ')' in item:
            if 'доб' in item:
                result = pattern.sub(r'+7(\2)\3-\4-\5 доб. \7', item)
                new_phone_list.append(result)
            else:
                result = pattern.sub(r'+7(\2)\3-\4-\5', item)
                new_phone_list.append(result)
        else:
        # если скобки отсутствуют или сочетаются с дефисом, во избежании попадания в код города
        # некорректной группы цифр, прописываем паттерн без скобок
            if 'доб' in item:
                result = pattern.sub(r'+7\2\3\4\5 доб. \7', item)
                new_phone_list.append(result)
            else:
                result = pattern.sub(r'+7\2\3\4\5', item)
                new_phone_list.append(result)


def remove_doubles():
    i = 0
    while i < len(contacts):
        j = i + 1
        while j < len(contacts):
            contacts[i].merge_doubles(contacts[j])
            j += 1
        i += 1


def final_list_input():
    final_list.append(['lastname', 'firstname', 'surname', 'org', 'position', 'phone', 'email'])
    for i in range(0, len(contacts)):
        final_list.append([contacts[i].lastname,
                           contacts[i].firstname,
                           contacts[i].surname,
                           contacts[i].org,
                           contacts[i].position,
                           contacts[i].phone,
                           contacts[i].email])


class Contact:
    def __init__(self, i):
        self.firstname = firstname_list[i]
        self.lastname = lastname_list[i]
        self.surname = surname_list[i]
        self.org = org_list[i]
        self.position = position_list[i]
        self.phone = new_phone_list[i]
        self.email = email_list[i]

    def __eq__(self, other):
        if self.lastname == other.lastname and self.firstname == other.firstname:
            return True
        else:
            return False

    def merge_doubles(self, other):
        if self.__eq__(other) == True:
            if other.position == '':
                setattr(other, 'position', self.position)
            if other.surname == '':
                other.surname = self.surname
            if other.phone == '':
                setattr(other, 'phone', self.phone)
            if other.email == '':
                other.email = self.email
            if other.org == '':
                other.org = self.org
            return contacts.remove(self)


if __name__ == '__main__':

    with open('docs/phonebook_raw.csv', encoding='utf-8') as f:
        rows = csv.reader(f, delimiter=',')
        contacts_list = list(rows)

    split_names()
    split_other()
    change_phone_format()

    for i in range(1, len(lastname_list)):
        contacts.append(Contact(i))

    remove_doubles()
    final_list_input()

# код для записи файла в формате CSV
    with open('docs/phonebook.csv', "w", encoding='utf-8') as f:
      datawriter = csv.writer(f, delimiter=',')
      datawriter.writerows(final_list)
