import pymorphy2

morph = pymorphy2.MorphAnalyzer()

def decline_name(name, case='gent'):
    """Склоняет имя/фамилию/отчество в нужный падеж."""
    parsed = morph.parse(name)[0]
    if parsed.inflect({case}):
        return parsed.inflect({case}).word.capitalize()
    return name  # если не получилось, возвращаем исходное

# Пример использования
full_name = "Криворотова Полина Александровна"
last, first, middle = full_name.split()

# Родительный падеж (кого?)
last_gen = decline_name(last, 'gent')  # Иванова
first_gen = decline_name(first, 'gent')  # Ивана
middle_gen = decline_name(middle, 'gent')  # Ивановича

print(f"{last_gen} {first_gen} {middle_gen}")  # "Иванова Ивана Ивановича"