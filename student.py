# Создайте класс студента.
# - Используя дескрипторы проверяйте ФИО на
# первую заглавную букву и наличие только букв.
# - Названия предметов должны загружаться
# из файла CSV при создании экземпляра.
# Другие предметы в экземпляре недопустимы.
# - Для каждого предмета можно хранить оценки (от 2 до 5)
# и результаты тестов (от 0 до 100).
# - Также экземпляр должен сообщать средний балл
# по тестам для каждого предмета и
# по оценкам всех предметов вместе взятых.

import csv
import re
import logging
import argparse


logging.basicConfig(filename='logger.log',
                    encoding='utf-8',
                    level=logging.NOTSET,
                    filemode='a')

logger = logging.getLogger(__name__)

# Создание файла с предметами
subjects = ["Математика", "Физика", "Химия", "Биология", "История",
            "Литература", "Иностранный язык", "Информатика", "География"]
csv_filename = 'subjects.csv'
with open(csv_filename, 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    for subject in subjects:
        writer.writerow([subject])

logging.info(f"Файл {csv_filename} с перечнем предметов успешно создан.")


class NameValidator:
    """
    Класс выполняет проверку корректности ФИО
    """

    def __get__(self, instance, owner):
        return instance.__name

    def __set__(self, instance, value):
        if not re.match(r'^[А-Я][а-яА-Я\s]*$', value):
            message_error = "ФИО должно содержать только буквы кириллицы и начинаться с заглавной буквы"
            logger.error(message_error)
            raise ValueError(message_error)
        instance.__name = value


class Subject:
    """
    Класс содержит методы проверки корректности выставляемых оценок
    и методы расчета среднего арифметического баллов
    """

    def __init__(self, name, middle_name, last_name):
        self.name = name
        self.middle_name = middle_name
        self.last_name = last_name
        self.scores = []
        self.tests = []

    def add_score(self, score):
        if score < 2 or score > 5:
            message_error = "Оценка должна быть в диапазоне от 2 до 5"
            logger.error(message_error)
            raise ValueError(message_error)
        self.scores.append(score)

    def add_test_result(self, result):
        if result < 0 or result > 100:
            message_error = "Баллы за тест должны быть в диапазоне от 0 до 100"
            logger.error(message_error)
            raise ValueError(message_error)
        self.tests.append(result)

    def average_score(self):
        if not self.scores:
            return 0
        return sum(self.scores) / len(self.scores)

    def average_tests_result(self):
        if not self.tests:
            return 0
        return sum(self.tests) / len(self.tests)


class Student:
    name = NameValidator()
    middle_name = NameValidator()
    last_name = NameValidator()

    def __init__(self, csv_filename):
        self.subjects = {}
        self.load_subjects(csv_filename)

    def load_subjects(self, csv_filename):
        with open(csv_filename, 'r', encoding='utf8') as file:
            reader = csv.reader(file)
            for row in reader:
                subject_name = row[0]
                subject = Subject(subject_name, " ", " ")  # Здесь добавляем отчество и фамилию
                self.subjects[subject_name] = subject

    def add_score(self, subject_name, score):
        if subject_name not in self.subjects:
            message_error = "Такого предмета нет в системе"
            logger.error(message_error)
            raise ValueError(message_error)
        self.subjects[subject_name].add_score(score)
        logging.info('Добавлена оценка %d по предмету %s для студента %s %s %s', score, subject_name,
                     self.name, self.middle_name, self.last_name)

    def add_test_result(self, subject_name, result):
        if subject_name not in self.subjects:
            message_error = "Такого предмета нет в системе"
            logger.error(message_error)
            raise ValueError(message_error)
        self.subjects[subject_name].add_test_result(result)
        logging.info('Добавлен результат теста %d по предмету %s для студента %s %s %s', result,
                     subject_name, self.name, self.middle_name, self.last_name)

    def average_score(self):
        total_scores = sum(subject.average_score() for subject in self.subjects.values())
        total_subjects = len(self.subjects)
        return total_scores / total_subjects

    def __str__(self):
        return f"Студент: {self.name}, {self.middle_name} {self.last_name}" \
               f" Предметы: {', '.join(self.subjects.keys())}"

def main():
    parser = argparse.ArgumentParser(description='Управление студентами и предметами.')
    parser.add_argument('--name', required=True, help='Имя студента')
    parser.add_argument('--middle_name', required=True, help='Отчество студента')
    parser.add_argument('--last_name', required=True, help='Фамилия студента')
    parser.add_argument('--subject', required=True, help='Предмет')
    parser.add_argument('--score', type=int, help='Оценка')
    parser.add_argument('--test_result', type=int, help='Результат теста')

    args = parser.parse_args()

    student = Student("subjects.csv")
    student.name = args.name
    student.middle_name = args.middle_name
    student.last_name = args.last_name

    if args.score is not None:
        student.add_score(args.subject, args.score)

    if args.test_result is not None:
        student.add_test_result(args.subject, args.test_result)

    print(student)

    for subject_name, subject in student.subjects.items():
        print(f"Предмет: {subject_name}")
        print(f"Средний балл: {subject.average_score()}")
        print(f"Средний результат теста: {subject.average_tests_result()}")

    print(f"Средний балл по всем предметам: {student.average_score()}")

if __name__ == '__main__':
    main()


#    student = Student("subjects.csv")

 #   student.name = 'Белоусов Ярослав Александрович'

 #   student.add_score("Математика", 5)
 #   student.add_score("Информатика", 5)
 #   student.add_score("Физика", 4)
 #   student.add_score("Информатика", 5)
 #   student.add_test_result("Математика", 94)
 #   student.add_test_result("Информатика", 90)
 #   student.add_test_result("Физика", 100)

#    print(student)
#
#    for subject_name, subject in student.subjects.items():
#        print(f"Предмет: {subject_name}")
#        print(f"Средний балл: {subject.average_score()}")
#        print(f"Средний результат теста: {subject.average_tests_result()}")

#    print(f"Средний балл по всем предметам: {student.average_score()}")