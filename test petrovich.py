def define_gender(fio):
    fio_split = fio.split(' ')
    #если есть отчетство, проверяем, на что заканчивается:
    if len (fio_split)>2:
        #Если на а, то пол женский
        if fio_split[2].endswith('а'):
            return 'Female'
        else:
            return 'Male'
    #Если отчества нет, проверим фамилию
    else:
        if fio_split[0].endswith(("ова", "ева", "ина", "ая")):
            return 'Female'
        else:
            return 'Male'

print (define_gender('Муракаев Карина'))