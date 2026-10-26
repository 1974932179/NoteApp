from app import get_db
from comment_crypto import PREFIX, decrypt_comment, encrypt_comment


def main():
    conn = get_db()
    conn.autocommit = False
    migrated = 0

    try:
        with conn.cursor() as cur:
            cur.execute("LOCK TABLE notes IN SHARE ROW EXCLUSIVE MODE")
            cur.execute("SELECT id, comment FROM notes ORDER BY id")
            rows = cur.fetchall()

            for row in rows:
                comment = row["comment"]

                if comment is None:
                    continue

                if comment.startswith(PREFIX):
                    decrypt_comment(comment)
                    continue

                cur.execute(
                    "UPDATE notes SET comment = %s WHERE id = %s",
                    (encrypt_comment(comment), row["id"]),
                )
                migrated += 1

        conn.commit()
        print(f"Migrated {migrated} comments")

    except Exception:
        conn.rollback()
        raise

    finally:
        conn.close()


if __name__ == "__main__":
    main()