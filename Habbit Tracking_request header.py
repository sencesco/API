import requests
from datetime import datetime

USER = "Pixela usr"
TOKEN = "Pixela Token"
GRAPH_ID = "Pixela graph ID name"

pixela_endpoint = "https://pixe.la/v1/users"
pixela_params = {
    "token" : TOKEN,
    "username": USER,
    "agreeTermsOfService": "yes",
    "notMinor": "yes"
}

# Use for create a user, if recall again and raise user is already exit is meaning is this user alrady cretatd
# respone = requests.post(url=pixela_endpoint, json=pixela_params)
# print(respone.text)

pixela_graph_endpoint = f"{pixela_endpoint}/{USER}/graphs"
graph_config ={
    "id": "demograph1",
    "name": "learning",
    "unit": "minute",
    "type": "int",
    "color": "sora",
}

headers = {
    "X-USER-TOKEN": TOKEN
}

# Use for 1 times crete a graph, if recall agian will get graph is already

# respone = requests.post(url=pixela_graph_endpoint, json=graph_config, headers=headers)
# print(respone.text)
# So whn call and see a tracking is : https://pixe.la/v1/users/Pixela usr/graphs/demograph1.html

today = datetime.now()
date_of_today = today.strftime("%Y%m%d")

""" # Create a post
pixela_creation_end_point = f"{pixela_endpoint}/{USER}/graphs/{GRAPH_ID}"
pixla_graph_data = {
    "date": date_of_today,
    "quantity": "130"
}
response_post =requests.post(url=pixela_creation_end_point, json=pixla_graph_data,headers=headers)
print(response_post.text) """

# Update a post
pixela_update_end_point = f"{pixela_endpoint}/{USER}/graphs/{GRAPH_ID}/{date_of_today}"
pixla_graph_data = {
    "date": date_of_today,
    "quantity": "130"
}
response_update_post =requests.put(url=pixela_update_end_point, json=pixla_graph_data,headers=headers)
print(response_update_post.text)

""" # delete a post
pixela_delete_end_point = f"{pixela_endpoint}/{USER}/graphs/{GRAPH_ID}/{date_of_today}"
pixla_graph_data = {
    "date": date_of_today,
}
response_delete_post =requests.delete(url=pixela_update_end_point, json=pixla_graph_data,headers=headers)
print(response_delete_post.text) """
