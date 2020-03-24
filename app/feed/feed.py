import psycopg2
import json
import uuid

class Feed():

    def __init__(self, user_key):
        self.db_conn = psycopg2.connect(user = "postgres", host = "localhost", port = "5432", database = "anonimus")
        self.db_cursor = self.db_conn.cursor()
        self.user_key = user_key
    
    def submit_post(self, post_content):
        try:
            insert_post_query = """
                    INSERT INTO posts (post_id, user_id, post_content) 
                    VALUES (
                        '{}',
                        (SELECT user_id from users where user_key='{}'),
                        '{}'
                    )
                """.format(str(uuid.uuid4().hex), self.user_key, post_content)
            print(insert_post_query)
            self.db_cursor.execute(insert_post_query)
            self.db_conn.commit()
            return False, "post has been submitted" 
        except Exception as err:
            print("Error when submitting new post: ", str(err))
            return False, str(err)
    
    def get_feed(self):
        get_post_query = "SELECT * FROM posts LIMIT 25"
        self.db_cursor.execute(get_post_query)
        posts = self.db_cursor.fetchall()
        feed = []
        for post in posts:
            feed.append({
                "post_id": post[0],
                "user_id": post[1],
                "post_content": post[2],
                "posted_at": str(post[3]),
                "likes": post[4]
            })
        return feed