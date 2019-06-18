import requests
# import argparse
file_name = "users.config"
event = "PushEvent"
def user_events_url(user):
    return "https://api.github.com/users/"+user+"/events"

def get_data(users):
    data = [];
    for user in users:
        response = requests.get(user_events_url(user)).json()
        data.append(response)
    return data
def filter_by_event(events, event_type):
    return filter(lambda x: x["type"] == event_type, events)
def filter_by_author(commits, authors):
    tmp = []
    for author in authors:
        tmp.add(filter(lambda x: x["author"]["name"] == author), commits);
    return list(set(tmp))
# def filter_by_date(events, date):

def return_users_from_file(path):
    file = open(path,"r")
    users=[]
    line = file.readline()
    while(len(line)>0):
        line = line.splitlines()[0]
        line = line.strip()
        if(len(line)>0):
            users.append(line)
        line = file.readline()
    return users
# user = input()
def get_name_url(name):
    return "https://api.github.com/users/"+name
def get_name(name):
    return requests.get(get_name_url(name)).json()
def remove_empty(data):
    for item in data:
        return data.filter(lambda item: len(item.commits)>0)
users = return_users_from_file(file_name)
data = get_data(users)
for i in data:
    item = list(filter_by_event(item, event))
for response in data:
    for item in response:
        # print(item)
        author_name = get_name(item["actor"]["login"])
        item["payload"]["commits"] = filter_by_author(item["payload"]["commits"],[item["actor"]["login"], author_name])

for item in data:
    item = remove_empty(item)
print(data)

# data = get_data([user]);

# for event in filter_by_event(data[0], "PushEvent"):
#     commits = event["payload"]["commits"];
#     event["payload"]["commits"] = filter_by_author(commits, ["kishore-ganesh", "Kalpaj Aggrawala"])


# Add difference between previous run and this return
# Read from file  
#Name filter problems
#On Each run, store the results. On next run, just give the diff, i.e filter y dat
