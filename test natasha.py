from natasha import MorphVocab, NamesExtractor
from natasha.doc import Doc, Token

morph_vocab = MorphVocab()
names_extractor = NamesExtractor(morph_vocab)


def get_gender_from_name(full_name: str):
    """Определяет пол человека по ФИО с помощью Natasha"""
    doc = Doc(full_name)
    doc.segment(morph_vocab)
    doc.tag_morph(morph_vocab)
    doc.parse_syntax(morph_vocab)
    matches = names_extractor(doc)

    for match in matches:
        if hasattr(match.fact, 'gender'):
            return match.fact.gender
    return None


def decline_fio(full_name: str, case: str = 'gent'):
    """Склоняет ФИО в указанный падеж"""
    doc = Doc(full_name)
    doc.segment(morph_vocab)
    doc.tag_morph(morph_vocab)

    for token in doc.tokens:
        # Если токен является именем собственным (имя, фамилия, отчество)
        if 'Name' in token.pos or 'Surn' in token.pos or 'Patr' in token.pos:
            parsed = morph_vocab.parse(token.text)
            if parsed:
                # Пробуем просклонять
                forms = parsed.lexeme
                for form in forms:
                    if case in form.feats.get('case', []):
                        token.text = form.word
                        break
    return ' '.join(token.text for token in doc.tokens)


def get_student_form(full_name: str):
    """Возвращает правильную форму слова 'обучающийся' с учетом пола"""
    gender = get_gender_from_name(full_name)

    if gender == 'male':
        return 'обучающийся'
    elif gender == 'female':
        return 'обучающаяся'
    else:
        return 'обучающийся'  # по умолчанию мужской род


# Примеры использования
examples = [
    "Иванов Иван Иванович",
    "Петрова Мария Сергеевна",
    "Сидоров Дмитрий",
    "Коваленко Анна",
    "Абдурахман ибн Хоттаб",
    "ООО 'Рога и копыта'"
]

for name in examples:
    declined_name = decline_fio(name, 'gent')  # родительный падеж
    student_form = get_student_form(name)
    print(f"Исходное: {name}")
    print(f"Склоненное: {declined_name}")
    print(f"Форма: {student_form}")
    print()