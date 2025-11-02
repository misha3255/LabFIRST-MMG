import json
import xml.etree.ElementTree as ET
from xml.dom import minidom
from typing import List

# Создание иерархии пользовательских исключений
class UniversityDataError(Exception):
    """Базовое исключение для всех ошибок связанных с данными университета"""
    pass

class NotFoundError(UniversityDataError):
    """Исключение, возникающее когда сущность не найдена"""
    pass

class DuplicateIDError(UniversityDataError):
    """Исключение, возникающее при попытке создать сущность с уже существующим ID"""
    pass

class InvalidDataError(UniversityDataError):
    """Исключение, возникающее при невалидных данных"""
    pass

# Класс для представления студента
class Student:
    def __init__(self, id: int, name: str, email: str, year: int, faculty: str):
        # Инициализация атрибутов студента
        self.id = id
        self.name = name
        self.email = email
        self.year = year
        self.faculty = faculty

    def to_dict(self):
        """Преобразует объект Student в словарь для сериализации в JSON"""
        return {"id": self.id, "name": self.name, "email": self.email,
                "year": self.year, "faculty": self.faculty}

    def to_xml(self):
        """Преобразует объект Student в XML элемент"""
        element = ET.Element("student")  # Создаем корневой элемент
        for field in ['id', 'name', 'email', 'year', 'faculty']:
            ET.SubElement(element, field).text = str(getattr(self, field))
        return element

# Класс для представления профессора
class Professor:
    def __init__(self, id: int, name: str, email: str, department: str):
        # Инициализация атрибутов профессора
        self.id = id
        self.name = name
        self.email = email
        self.department = department

    def to_dict(self):
        """Преобразует объект Professor в словарь"""
        return {"id": self.id, "name": self.name, "email": self.email,
                "department": self.department}

    def to_xml(self):
        """Преобразует объект Professor в XML элемент"""
        element = ET.Element("professor")
        for field in ['id', 'name', 'email', 'department']:
            ET.SubElement(element, field).text = str(getattr(self, field))
        return element

# Класс для представления курса
class Course:
    def __init__(self, id: int, name: str, code: str, credits: int):
        # Инициализация атрибутов курса
        self.id = id
        self.name = name
        self.code = code
        self.credits = credits

    def to_dict(self):
        """Преобразует объект Course в словарь"""
        return {"id": self.id, "name": self.name, "code": self.code,
                "credits": self.credits}

    def to_xml(self):
        """Преобразует объект Course в XML элемент"""
        element = ET.Element("course")
        for field in ['id', 'name', 'code', 'credits']:
            ET.SubElement(element, field).text = str(getattr(self, field))
        return element

# Класс для представления кафедры
class Department:
    def __init__(self, id: int, name: str, head: str):
        # Инициализация атрибутов кафедры
        self.id = id
        self.name = name
        self.head = head

    def to_dict(self):
        """Преобразует объект Department в словарь"""
        return {"id": self.id, "name": self.name, "head": self.head}

    def to_xml(self):
        """Преобразует объект Department в XML элемент"""
        element = ET.Element("department")
        for field in ['id', 'name', 'head']:
            ET.SubElement(element, field).text = str(getattr(self, field))
        return element

# Класс для представления оценки
class Grade:
    def __init__(self, id: int, student_id: int, course_id: int, grade: float):
        # Инициализация атрибутов оценки
        self.id = id
        self.student_id = student_id
        self.course_id = course_id
        self.grade = grade

    def to_dict(self):
        """Преобразует объект Grade в словарь"""
        return {"id": self.id, "student_id": self.student_id,
                "course_id": self.course_id, "grade": self.grade}

    def to_xml(self):
        """Преобразует объект Grade в XML элемент"""
        element = ET.Element("grade")
        for field in ['id', 'student_id', 'course_id', 'grade']:
            ET.SubElement(element, field).text = str(getattr(self, field))
        return element

# Основной класс для хранения всех данных университета
class UniversityData:
    def __init__(self):
        # Инициализация пустых списков для хранения всех сущностей
        self.students: List[Student] = []
        self.professors: List[Professor] = []
        self.courses: List[Course] = []
        self.departments: List[Department] = []
        self.grades: List[Grade] = []

# Функция для сохранения данных в JSON файл
def save_to_json(data: UniversityData, filename: str):
    try:
        # Создаем словарь, содержащий списки всех сущностей в виде словарей
        json_data = {
            "students": [i.to_dict() for i in data.students],  # Преобразуем каждого студента в словарь
            "professors": [i.to_dict() for i in data.professors],
            "courses": [i.to_dict() for i in data.courses],
            "departments": [i.to_dict() for i in data.departments],
            "grades": [i.to_dict() for i in data.grades]
        }
        # Открываем файл для записи с кодировкой UTF-8
        with open(filename, 'w', encoding='utf-8') as f:
            # Записываем данные в файл с отступами и поддержкой кириллицы
            json.dump(json_data, f, indent=2, ensure_ascii=False)
        print(f"Данные сохранены в {filename}")
    except Exception as e:
        # Обрабатываем любые ошибки при сохранении
        print(f"Ошибка сохранения JSON: {e}")

# Функция для загрузки данных из JSON файла
def load_from_json(filename: str):
    # Создаем новый экземпляр UniversityData
    data = UniversityData()
    try:
        # Открываем файл для чтения
        with open(filename, 'r', encoding='utf-8') as f:
            # Загружаем данные из JSON файла
            json_data = json.load(f)

        # Используем распаковку словарей для создания объектов
        # Student(**i) эквивалентно Student(id=i['id'], name=i['name'], ...)
        data.students = [Student(**i) for i in json_data.get("students", [])]
        data.professors = [Professor(**j) for j in json_data.get("professors", [])]
        data.courses = [Course(**k) for k in json_data.get("courses", [])]
        data.departments = [Department(**l) for l in json_data.get("departments", [])]
        data.grades = [Grade(**m) for m in json_data.get("grades", [])]

        print(f"Данные загружены из {filename}")
    except FileNotFoundError:
        # Если файл не найден, создаем пустой набор данных
        print(f"Файл {filename} не найден")
    except Exception as e:
        # Обрабатываем другие ошибки
        print(f"Ошибка загрузки JSON: {e}")
    return data

# Функция для сохранения данных в XML файл
def save_to_xml(data: UniversityData, filename: str):
    try:
        # Создаем корневой элемент XML
        root = ET.Element("university")
        # Для каждого типа сущностей создаем соответствующий раздел
        for lst, name in [
            (data.students, "students"), (data.professors, "professors"),
            (data.courses, "courses"), (data.departments, "departments"),
            (data.grades, "grades")
        ]:
            # Создаем элемент для текущего типа сущностей
            elem = ET.SubElement(root, name)
            # Добавляем каждую сущность в виде XML элемента
            for item in lst:
                elem.append(item.to_xml())

        # Форматируем XML для красивого вывода
        xml_str = minidom.parseString(ET.tostring(root)).toprettyxml(indent="  ")
        # Записываем XML в файл
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(xml_str)
        print(f"Данные сохранены в {filename}")
    except Exception as e:
        print(f"Ошибка сохранения XML: {e}")

# Функция для загрузки данных из XML файла
def load_from_xml(filename: str) -> UniversityData:
    data = UniversityData()
    try:
        # Парсим XML файл
        tree = ET.parse(filename)
        root = tree.getroot()  # Получаем корневой элемент

        # Внутренняя функция для загрузки элементов определенного типа
        def load_items(element_name, class_type, fields):
            # Ищем элемент с заданным именем
            elem = root.find(element_name)
            if elem is not None:
                # Для каждого элемента нужного типа
                for item_elem in elem.findall(class_type.__name__.lower()):
                    field_values = []
                    # Для каждого поля извлекаем значение
                    for field in fields:
                        field_elem = item_elem.find(field)
                        if field_elem is not None and field_elem.text is not None:
                            # Преобразуем типы данных в зависимости от поля
                            if field in ["id", "year", "credits", "student_id", "course_id"]:
                                field_values.append(int(field_elem.text))
                            elif field == "grade":
                                field_values.append(float(field_elem.text))
                            else:
                                field_values.append(field_elem.text)
                    # Создаем объект и добавляем в соответствующий список
                    data.__dict__[element_name].append(class_type(*field_values))

        # Загружаем все типы сущностей
        load_items("students", Student, ["id", "name", "email", "year", "faculty"])
        load_items("professors", Professor, ["id", "name", "email", "department"])
        load_items("courses", Course, ["id", "name", "code", "credits"])
        load_items("departments", Department, ["id", "name", "head"])
        load_items("grades", Grade, ["id", "student_id", "course_id", "grade"])

        print(f"Данные загружены из {filename}")
    except FileNotFoundError:
        print(f"Файл {filename} не найден")
    except Exception as e:
        print(f"Ошибка загрузки XML: {e}")
    return data

# Вспомогательная функция для проверки уникальности ID
def _check_unique_id(data: UniversityData, entity_type: str, new_id: int):
    """Проверяет, что ID является уникальным для данного типа сущности"""
    # Словарь для связи типа сущности с соответствующим списком
    entity_map = {
        "student": data.students,
        "professor": data.professors,
        "course": data.courses,
        "department": data.departments,
        "grade": data.grades
    }
    # Проверяем, существует ли уже сущность с таким ID
    if entity_type in entity_map and new_id in [item.id for item in entity_map[entity_type]]:
        raise DuplicateIDError(f"ID {new_id} уже существует")

# Вспомогательная функция для валидации ID
def _validate_id(entity_id: int):
    """Проверяет, что ID является положительным целым числом"""
    if not isinstance(entity_id, int) or entity_id <= 0:
        raise InvalidDataError("ID должен быть положительным целым числом")

# CRUD операции для студентов

def create_student(data: UniversityData, **kwargs):
    """Создает нового студента"""
    try:
        # Проверяем уникальность ID
        _check_unique_id(data, "student", kwargs['id'])
        # Валидируем ID
        _validate_id(kwargs['id'])
        # Создаем объект студента с распаковкой аргументов
        student = Student(**kwargs)
        # Добавляем студента в список
        data.students.append(student)
        print(f"Студент {kwargs['name']} создан")
        return student
    except Exception as e:
        print(f"Ошибка создания студента: {e}")
    return None

def delete_student(data: UniversityData, student_id: int):
    """Удаляет студента по ID"""
    try:
        # Валидируем ID
        _validate_id(student_id)
        # Ищем студента в списке
        for i, student in enumerate(data.students):
            if student.id == student_id:
                # Удаляем студента по индексу
                data.students.pop(i)
                print(f"Студент с ID {student_id} удален")
                return True
        # Если студент не найден, вызываем исключение
        raise NotFoundError(f"Студент с ID {student_id} не найден")
    except Exception as e:
        print(f"Ошибка удаления студента: {e}")
    return False

def find_student(data: UniversityData, student_id: int):
    """Находит студента по ID"""
    try:
        # Валидируем ID
        _validate_id(student_id)
        # Используем генератор для поиска студента
        student = next((i for i in data.students if i.id == student_id), None)
        if not student:
            raise NotFoundError(f"Студент с ID {student_id} не найден")
        return student
    except Exception as e:
        print(f"Ошибка поиска студента: {e}")
    return None

def update_student(data: UniversityData, student_id: int, **kwargs):
    """Обновляет данные студента"""
    try:
        # Валидируем ID
        _validate_id(student_id)
        # Находим студента
        student = find_student(data, student_id)
        if not student:
            raise NotFoundError(f"Студент с ID {student_id} не найден")

        # Обновляем каждое переданное поле
        for key, value in kwargs.items():
            if hasattr(student, key):  # Проверяем, что поле существует
                if key == 'id':  # Особый случай - проверяем уникальность нового ID
                    _check_unique_id(data, "student", value)
                # Устанавливаем новое значение поля
                setattr(student, key, value)

        print(f"Студент с ID {student_id} обновлен")
        return True
    except Exception as e:
        print(f"Ошибка обновления студента: {e}")
    return False

# Аналогичные CRUD операции для профессоров

def create_professor(data: UniversityData, **kwargs):
    """Создает нового профессора"""
    try:
        _check_unique_id(data, "professor", kwargs['id'])
        _validate_id(kwargs['id'])
        professor = Professor(**kwargs)
        data.professors.append(professor)
        print(f"Профессор {kwargs['name']} создан")
        return professor
    except Exception as e:
        print(f"Ошибка создания профессора: {e}")
    return None

def delete_professor(data: UniversityData, professor_id: int):
    """Удаляет профессора по ID"""
    try:
        _validate_id(professor_id)
        for i, professor in enumerate(data.professors):
            if professor.id == professor_id:
                data.professors.pop(i)
                print(f"Профессор с ID {professor_id} удален")
                return True
        raise NotFoundError(f"Профессор с ID {professor_id} не найден")
    except Exception as e:
        print(f"Ошибка удаления профессора: {e}")
    return False

def find_professor(data: UniversityData, professor_id: int):
    """Находит профессора по ID"""
    try:
        _validate_id(professor_id)
        professor = next((p for p in data.professors if p.id == professor_id), None)
        if not professor:
            raise NotFoundError(f"Профессор с ID {professor_id} не найден")
        return professor
    except Exception as e:
        print(f"Ошибка поиска профессора: {e}")
    return None

def update_professor(data: UniversityData, professor_id: int, **kwargs):
    """Обновляет данные профессора"""
    try:
        _validate_id(professor_id)
        professor = find_professor(data, professor_id)
        if not professor:
            raise NotFoundError(f"Профессор с ID {professor_id} не найден")

        for key, value in kwargs.items():
            if hasattr(professor, key):
                if key == 'id':
                    _check_unique_id(data, "professor", value)
                setattr(professor, key, value)

        print(f"Профессор с ID {professor_id} обновлен")
        return True
    except Exception as e:
        print(f"Ошибка обновления профессора: {e}")
    return False

# Аналогичные CRUD операции для курсов

def create_course(data: UniversityData, **kwargs):
    """Создает новый курс"""
    try:
        _check_unique_id(data, "course", kwargs['id'])
        _validate_id(kwargs['id'])
        course = Course(**kwargs)
        data.courses.append(course)
        print(f"Курс {kwargs['name']} создан")
        return course
    except Exception as e:
        print(f"Ошибка создания курса: {e}")
    return None

def delete_course(data: UniversityData, course_id: int):
    """Удаляет курс по ID"""
    try:
        _validate_id(course_id)
        for i, course in enumerate(data.courses):
            if course.id == course_id:
                data.courses.pop(i)
                print(f"Курс с ID {course_id} удален")
                return True
        raise NotFoundError(f"Курс с ID {course_id} не найден")
    except Exception as e:
        print(f"Ошибка удаления курса: {e}")
    return False

def find_course(data: UniversityData, course_id: int):
    """Находит курс по ID"""
    try:
        _validate_id(course_id)
        course = next((i for i in data.courses if i.id == course_id), None)
        if not course:
            raise NotFoundError(f"Курс с ID {course_id} не найден")
        return course
    except Exception as e:
        print(f"Ошибка поиска курса: {e}")
    return None

def update_course(data: UniversityData, course_id: int, **kwargs):
    """Обновляет данные курса"""
    try:
        _validate_id(course_id)
        course = find_course(data, course_id)
        if not course:
            raise NotFoundError(f"Курс с ID {course_id} не найден")

        for key, value in kwargs.items():
            if hasattr(course, key):
                if key == 'id':
                    _check_unique_id(data, "course", value)
                setattr(course, key, value)

        print(f"Курс с ID {course_id} обновлен")
        return True
    except Exception as e:
        print(f"Ошибка обновления курса: {e}")
    return False

# Основная функция программы
def main():
    try:
        print("=== СИСТЕМА УПРАВЛЕНИЯ УНИВЕРСИТЕТОМ ===\n")

        # Создание начальных данных
        data = UniversityData()
        create_student(data, id=1, name="Илья Белов", email="elez2006t@gmail.com", year=2, faculty="ИИТ")
        create_professor(data, id=1, name="Владислав Александрович Чеканин", email="vladchekanin@rambler.ru", department="ИИТ")
        create_course(data, id=1, name="Прикладная информатика", code="09.03.03", credits=4)

        data.departments.append(Department(1, "ИИТ", "Владислав Александрович Чеканин"))
        data.grades.append(Grade(1, 1, 1, 54))
        data.grades.append(Grade(2, 1, 1, 25))
        data.grades.append(Grade(3, 1, 1, 26))
        data.grades.append(Grade(4, 1, 1, 27))

        print(f"\nСоздано: Студентов: {len(data.students)}, Профессоров: {len(data.professors)}, Курсов: {len(data.courses)}, Руководств: {len(data.departments)}, Оценок: {len(data.grades)}")

        # Сохранение данных в файлы
        save_to_json(data, "university.json")
        save_to_xml(data, "university.xml")

        # Загрузка данных из JSON для демонстрации
        json_data = load_from_json("university.json")
        print(f"Загружено из JSON: {len(json_data.students)} студентов")

        print("\n=== Демонстрация CRUD операций ===")

        # Демонстрация поиска и обновления
        student = find_student(json_data, 1)
        if student:
            print(f"Найден студент: {student.name} (год: {student.year})")
            update_student(json_data, 1, name="Илья Орешников", year=4)
            save_to_json(json_data, "university.json")  # Сохраняем изменения

        # Демонстрация создания нового студента
        create_student(json_data, id=2, name="Павел Брусиловский", email="pashkakakashka228@yandex.ru", year=1, faculty="ИИТ")
        save_to_json(json_data, "university.json")
        save_to_xml(json_data, "university.xml")

        # Проверка создания
        check_data = load_from_json("university.json")
        print(f"Теперь студентов: {len(check_data.students)}")

        # Демонстрация удаления
        delete_student(json_data, 1)
        save_to_json(json_data, "university.json")
        save_to_xml(json_data, "university.xml")

        # Финальная проверка
        final_data = load_from_json("university.json")
        print(f"Финальное количество студентов: {len(final_data.students)}")

        # Проверка загрузки из XML
        xml_data = load_from_xml("university.xml")
        print(f"Данные в XML: {len(xml_data.students)} студентов")

        # Демонстрация обработки ошибок
        print("\n=== Демонстрация обработки ошибок ===")
        create_student(json_data, id=2, name="Платон Буревестников", email="poseidon2025@mail.ru", year=1, faculty="ИИТ")  # Дублирование ID
        find_student(json_data, 999)  # Поиск несуществующего студента
        update_student(json_data, 999, name="Новое имя")  # Обновление несуществующего студента

        print("\n=== ПРОГРАММА ЗАВЕРШЕНА ===")

    except Exception as e:
        # Обработка критических ошибок
        print(f"Критическая ошибка: {e}")

# Точка входа в программу
if __name__ == "__main__":
    main()
