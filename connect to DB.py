import psycopg2

# Создаем соединение с базой данных
connection = psycopg2.connect(
    database="testdb",
    user="username",
    password="password",
    host="localhost",
    port="5432"
)

# Создаем курсор для выполнения SQL-запросов
cursor = connection.cursor()

# Создаем таблицу
cursor.execute('''CREATE TABLE IF NOT EXISTS users (id SERIAL PRIMARY KEY, name VARCHAR(255), age INTEGER)''')



# Закрываем соединение
connection.close()