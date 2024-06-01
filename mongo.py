from pymongo import MongoClient

# region Mongo init
client = MongoClient('localhost', 27017)
# client.admin.authenticate('username', 'password')
db = client.Jobs_crawler
collection = db.search_results
# endregion


def get_positions(filter_criteria):
    try:
        out = list(collection.find(filter_criteria))
    except:
        print("Mongo is down")
        exit(100500)
    return out


# positions_to_be_added_to_mongo = [
#     {
#         'company': "Рога и Копыта",
#         'location': 'Sofia, Bg',
#         'link': 'https://somewhere.com',
#         'date_found': '1/05/2024',
#         # 'last_found': '2/05/2024',
#         'hash': "@$EFcc#gv3GvF#WFVC",
#     },
#     {
#         'company': "Рога",
#         'location': 'Berlin, De',
#         'link': 'https://somewhere_else.com',
#         'date_found': '1/05/2024',
#         # 'last_found': '3/05/2024',
#         'hash': "@$EFcc##$Fcwsgv3GvF#WFVC",
#     }
#     ]

def add_new_position(positions: list):
    # new = positions_to_be_added_to_mongo
    for _ in positions:
        result = collection.insert_one(_)
        # print('Inserted document ID:', result.inserted_id)


def hash_is_present(hash_):
    return len(get_positions({'hash': hash_})) > 0


def delete_positions(filter_criteria: dict):
    # result = collection.delete_one({'name': 'John'})
    result = collection.delete_many(filter_criteria)
    print('Number of documents deleted:', result.deleted_count)


def update_positions(filter_criteria: dict, to_change: dict):
    # filter_criteria = {'city': 'New York'}
    # update_operation = {'$set': {'age': 35, 'city': 'Бобруйск'}}
    update_operation = {'$set': to_change}
    result = collection.update_many(filter_criteria, update_operation)
    print('Number of documents modified:', result.modified_count)


def clean_all_data():
    print(f"Removing all positions from {db}.{collection}...")
    delete_positions({})
    # add_new_position(positions_to_be_added_to_mongo)
