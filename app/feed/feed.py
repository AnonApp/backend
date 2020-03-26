import datetime
import json
import uuid
from app.models import db, Users, Posts, Comments, Likes

class Feed():

    def __init__(self, token):
        self.token = token

    def pretty_date(self, time=False):
        now = datetime.datetime.utcnow()
        if type(time) is int:
            diff = now - datetime.datetime.fromtimestamp(time)
        elif isinstance(time,datetime.datetime):
            diff = now - time
        elif not time:
            diff = now - now
        second_diff = diff.seconds
        day_diff = diff.days
        if day_diff < 0:
            return ''
        if day_diff == 0:
            if second_diff < 10:
                return "just now"
            if second_diff < 60:
                return str(int(second_diff)) + " seconds ago"
            if second_diff < 120:
                return "a minute ago"
            if second_diff < 3600:
                return str(int(second_diff / 60)) + " minutes ago"
            if second_diff < 7200:
                return "an hour ago"
            if second_diff < 86400:
                return str(int(second_diff / 3600)) + " hours ago"
        if day_diff == 1:
            return "Yesterday"
        if day_diff < 7:
            return str(int(day_diff)) + " days ago"
        if day_diff < 31:
            return str(int(day_diff / 7)) + " weeks ago"
        if day_diff < 365:
            return str(int(day_diff / 30)) + " months ago"
        return str(int(day_diff / 365)) + " years ago"
    
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
    
    def submit_comment(self, post_id, comment_content):
        try:
            user = db.session.query(Users).filter_by(token=self.token).first()
            post = db.session.query(Posts).filter_by(id=post_id).first()
            comment = Comments(id=str(uuid.uuid4().hex), post_id=post.id, user_id=user.id, content=comment_content)
            db.session.add(comment)
            db.session.commit()
            return False, "comment has been submitted" 
        except Exception as err:
            print("Error when submitting new comment: ", str(err))
            return False, str(err)
    
    def submit_like(self, post_id=None, comment_id=None):
        try:
            user = db.session.query(Users).filter_by(token=self.token).first()
            like = Likes(id=str(uuid.uuid4().hex), post_id=post_id, comment_id=comment_id, user_id=user.id)
            db.session.add(like)
            db.session.commit()
            return False, "the content is successfully liked."
        except Exception as err:
            print("Error when liking: ", str(err))
            return False, str(err)
    
    def submit_unlike(self, post_id=None, comment_id=None):
        try:
            user = db.session.query(Users).filter_by(token=self.token).first()
            like = Likes(id=str(uuid.uuid4().hex), post_id=post_id, comment_id=None, user_id=user.id)
            db.session.query(Likes).filter_by(post_id=like.post_id, comment_id=like.comment_id, user_id=user.id).delete()
            db.session.commit()
            return False, "the content is successfully unliked."
        except Exception as err:
            print("Error when unliking: ", str(err))
            return False, str(err)

    def get_posts(self):
        feed_query = """
        SELECT 
            users.id as user_id,
            posts.id as post_id,
            posts.content,
            exists(select 1 from likes where likes.post_id = posts.id and likes.user_id = users.id limit 1) as liked,
            (select count(distinct likes.user_id) from likes where likes.post_id = posts.id) as likes,
            (select count(distinct comments.id) from comments where comments.post_id = posts.id) as comments,
            posts.posted_at
        FROM
            users,
            posts
        WHERE
            users.token = '{}';
        """.format(self.token)
        posts = db.engine.execute(feed_query)
        posts_json = []
        for post in posts:
            posts_json.append({
                "user_id": post[0],
                "post_id": post[1],
                "post_content": post[2],
                "liked": post[3],
                "likes": post[4],
                "comments": post[5],
                "posted_at": self.pretty_date(post[6])
            })
        return posts_json
    
    def get_comments(self, post_id):
        comments_query = """
        SELECT 
            comments.user_id,
            posts.id as post_id, 
            comments.id as comment_id, 
            comments.content,
            exists(select 1 from likes where likes.comment_id = comments.id and likes.user_id = users.id limit 1) as liked,
            (select count(likes.comment_id) from likes where likes.comment_id = comments.id) as likes,
            comments.posted_at
        FROM 
            users,
            comments
        JOIN 
            posts on posts.id=comments.post_id
        WHERE
            users.token = '{}' and
            comments.post_id = '{}';
        """.format(self.token, post_id)
        comments = db.engine.execute(comments_query)
        comments_json = []
        for comment in comments:
            comments_json.append({
                "user_id": comment[0],
                "post_id": comment[1],
                "comment_id": comment[2],
                "comment_content": comment[3],
                "liked": comment[4],
                "likes": comment[5],
                "posted_at": self.pretty_date(comment[6])
            })
        return comments_json