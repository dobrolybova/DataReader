import psycopg2
from db import DATABASE

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
                            user=DATABASE["username"],
                            password=DATABASE["password"],
                            host=DATABASE["host"],
                            port=DATABASE["port"])
    conn.autocommit = True
    cursor = conn.cursor()
    for command in commands:
        cursor.execute(command)
    conn.commit()
    conn.close()


if __name__ == "__main__":
    create_db(sql_commands)
