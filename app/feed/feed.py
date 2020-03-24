import datetime
import json
import uuid
from app.models import db, Users, Posts, Comments

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
    
    def get_feed(self):
        posts = db.session.query(Posts).all()
        feed = []
        for post in posts:
            feed.append({
                "post_id": post.id,
                "user_id": post.user_id,
                "post_content": post.content,
                "likes": post.likes,
                "posted_at": self.pretty_date(post.posted_at)
            })
        return feed
    
    def get_comment(self, post_id):
        comments = db.session.query(Comments).filter(post_id=post_id).all()
        feed = []
        for comment in comments:
            feed.append({
                "comment_id": comment.id,
                "post_id": comment.post_id,
                "user_id": comment.user_id,
                "comment_content": comment.content,
                "likes": post.likes,
                "posted_at": self.pretty_date(post.posted_at)
            })
        return feed