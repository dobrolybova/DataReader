import psycopg2

sql_commands = (
        # """
        # CREATE USER yulia WITH SUPERUSER PASSWORD 'yulia'
        # """,
        """
        CREATE database messages
        """,
)


def create_db(commands: tuple[str]):
    conn = psycopg2.connect(database="postgres",
                            user='yulia',
                            password='yulia',
                            host='127.0.0.1',
                            port='5432')
    conn.autocommit = True
    cursor = conn.cursor()
    for command in commands:
        cursor.execute(command)
    conn.commit()
    conn.close()


if __name__ == "__main__":
    create_db(sql_commands)
