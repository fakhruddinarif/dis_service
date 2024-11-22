from faker import Faker

from app.core.database import database
from seeder.user_seeder import user_table

photo_table = database.get_collection("photos")

faker = Faker()
num_post_photo = 4
num_sell_photo = 6
limit_user = 5

url_post_photo = [
    "https://is3.cloudhost.id/dis/photos/post/33f8cf31-68a0-4920-9934-2c3cdc804e86_dummy_1.jpg",
    "https://is3.cloudhost.id/dis/photos/post/3985a4c7-f610-4c56-be8a-dee5fb33ebe5_dummy_2.jpg",
]

url_sell_photo = [
    "https://is3.cloudhost.id/dis/photos/sell/c1329a19-718d-4d86-85b0-cab5b13778f4_content.jpg",
    "https://is3.cloudhost.id/dis/photos/sell/9b590d19-ca3e-43ac-ab5f-49bd40fb516c_dummy_1.jpg",
    "https://is3.cloudhost.id/dis/photos/sell/9273756d-a2fc-4128-a926-fc0047572491_dummy_2.jpg"
]

def seed_post_photos():
    for i in range(limit_user):
        users = user_table.find().limit(limit_user)
        for user in users:
            for j in range(num_post_photo):
                post_photo = {
                    "url": url_post_photo[j % 2],
                    "name": faker.sentence(),
                    "description": faker.text(max_nb_chars=50),
                    "type": "post",
                    "likes": [],
                    "comments": [],
                    "user_id": user["_id"],
                    "created_at": faker.date_time_this_year(),
                    "updated_at": faker.date_time_this_year(),
                    "deleted_at": None
                }
                photo_table.insert_one(post_photo)

def seed_sell_photos():
    for i in range(limit_user):
        users = user_table.find().limit(limit_user)
        for user in users:
            for j in range(len(url_sell_photo)):
                sell_photo = {
                    "url": url_sell_photo[j],
                    "name": faker.sentence(),
                    "base_price": 1000,
                    "sell_price": 1100,
                    "type": "sell",
                    "status": "available",
                    "description": faker.text(max_nb_chars=50),
                    "user_id": user["_id"],
                    "buyer_id": None,
                    "created_at": faker.date_time_this_year(),
                    "updated_at": faker.date_time_this_year(),
                    "deleted_at": None
                }
                photo_table.insert_one(sell_photo)