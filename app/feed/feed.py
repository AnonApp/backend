import psycopg2
import json

class Feed():

    def __init__(self):
        self.db_conn = psycopg2.connect(user = "postgres", host = "localhost", port = "5432", database = "anonimus")
        self.db_cursor = self.db_conn.cursor()
    
    def get_feed(self):
        return  
        {
            "feed": 
            [{
                "post_id": "2398fhin2pvi2ovn!2o3",
                "content": "Aku gak suka diginiin",
                "likes": "20",
                "timestamp": "12:00:00",
                "location": "Pademangan"
            },
            {
                "post_id": "onvkwoeuvbwpievubwep",
                "content": "Jangan pernah jahatin cewe lu",
                "likes": "200",
                "timestamp": "12:00:00",
                "location": "Kuningan"
            },
            {
                "post_id": "280fub2ouf23uf23!2o3",
                "content": "Apakah dia orangnya?",
                "likes": "4",
                "timestamp": "12:00:00",
                "location": "Rawamangun"
            }]
        }