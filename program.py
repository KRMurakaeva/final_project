from docxtpl import DocxTemplate
import pymorphy2
import re
# Инициализация анализатора
morph = pymorphy2.MorphAnalyzer()

#Функция получения инициалов
def initials (name):
    fio = name.split(' ')
    initials = fio[0]+' '+fio[1][0]+'.'
    if len (fio) > 2:
        return ' ' + initials + fio[2][0]
    else:
        return initials

#Функция определения пола по ФИО
def define_gender(fio):
    fio_split = fio.split(' ')
    #если есть отчетство, проверяем, на что заканчивается:
    if len (fio_split)>2:
        #Если на а, то пол женский
        if fio_split[2].endswith('а'):
            return 'femn'
        else:
            return 'masc'
    #Если отчества нет, проверим фамилию
    else:
        if fio_split[0].endswith(("ова", "ева", "ина", "ая")):
            return 'femn'
        else:
            return 'masc'

#Функция склонения слова
def change_case(word, target_case, gender=None):
    # Сохраняем оригинальный регистр первой буквы
    was_upper = word[0].isupper()
    word_lower = word.lower()
    parsed = morph.parse(word_lower)[0]

    # Формируем набор грамматических характеристик
    gram_features = {target_case}

    # Добавляем род, если он указан
    if gender:
        gram_features.add(gender)

    # Пробуем просклонять с родом, если он есть
    if parsed.inflect(gram_features):
        result = parsed.inflect(gram_features).word
    else:
        # Если не получилось - пробуем без указания рода
        if gender and parsed.inflect({target_case}):
            result = parsed.inflect({target_case}).word
        else:
            result = word_lower
    # Восстанавливаем регистр
    return result.capitalize() if was_upper else result

#Функция для разбивания фраз (имена, названия)по словам
def change_phrase(phrase, target_case, gender=None):
    # Разбиваем текст на части, сохраняя содержимое в кавычках
    parts = re.split('("[^"]*")', phrase)
    processed_parts = []

    for part in parts:
        if part.startswith('"') and part.endswith('"'):
            # Оставляем текст в кавычках без изменений
            processed_parts.append(part)
        else:
            # Обрабатываем остальной текст
            words = part.split()
            processed_words = []

            for word in words:
                # Обрабатываем каждое слово, пропуская предлоги, союзы и аббревиатуры
                if word.lower() in ["и", "на", "в", "с", "для"] or word.isupper():
                    processed_words.append(word)
                else:
                    # Обрабатываем части слов, разделенные дефисами
                    if '-' in word:
                        subwords = word.split('-')
                        processed_subwords = [change_case(sw, target_case, gender) for sw in subwords]
                        processed_words.append('-'.join(processed_subwords))
                    else:
                        processed_words.append(change_case(word, target_case, gender))

            processed_parts.append(' '.join(processed_words))

    return ' '.join(processed_parts)


practice_type = "производственная"
faculty = "Институт управления, экономики и финансов"
program  = "Экономическая безопасность"
place_of_practice = 'Компания ООО "Рога и копыта"'
student_name = "Муракаева Карина Равилевна"
course_number = "3"
group_number = "14.1-282"
start_date = "03.03.2025"
end_date = "31.05.2025"
practice_director_full = "Зюзина Светлана Васильевна"
practice_director_initials = initials (practice_director_full)
student_name_initials = initials (student_name)

student_gender = define_gender(student_name)
director_gender = define_gender(practice_director_full)


individual_task = {
    "practice_type": change_phrase(practice_type, 'accs').lower(),
    "faculty": faculty,
    "program": program,
    "place_of_practice": place_of_practice,
    "student_name": student_name,
    "course_number": course_number,
    "group_number": group_number,
    "start_date": start_date,
    "end_date": end_date,
    "practice_director_full": practice_director_full,
    "practice_director_initials": practice_director_initials,
    "student_name_initials": student_name_initials,
    "student_gender": "Обучающаяся" if student_gender == "femn" else "Обучающийся"
}

application = {
    "of_faculty": change_phrase(faculty, 'gent'),
    "to_practice_directior": change_phrase(practice_director_full,'datv', director_gender),
    "student_gender": "обучающейся" if student_gender == "femn" else "обучающегося",
    "from_student_name":change_phrase(student_name, 'gent', student_gender),
    "course_number": course_number,
    "group_number":group_number,
    "to_practice_type": change_phrase(practice_type, 'gent').lower(),
    "start_date":start_date,
    "finish_date": end_date,
    "practice_directior_initials":  practice_director_initials,
    "student_name_initials": student_name_initials,
    "in_place_of_practice": change_phrase(place_of_practice, 'loct')
}

doc = DocxTemplate("Individual task template.docx")
doc.render(individual_task)
doc.save(f"{student_name_initials} Индивидуальное задание.docx")
#
doc1 = DocxTemplate("Application template.docx")
doc1.render(application)
doc1.save(f"{student_name_initials} Заявление.docx")

