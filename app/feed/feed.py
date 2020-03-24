import psycopg2
import json
import uuid
from app.models import db, Users, Posts

class Feed():

    def __init__(self, token):
        self.db_conn = psycopg2.connect(user = "postgres", host = "localhost", port = "5432", database = "anonimus")
        self.db_cursor = self.db_conn.cursor()
        self.token = token
    
    def submit_post(self, post_content):
        try:
            user = db.session.query(Users).filter_by(token=self.token).first()
            post = Posts(id=str(uuid.uuid4().hex), user_id=user.id, content=post_content)
            db.session.add(post)
            db.session.commit()
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