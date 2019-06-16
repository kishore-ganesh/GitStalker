import requests
# import argparse

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
    return filter(lambda x: x["author"]["name"] == author for author in authors, authors);

user = input()
data = get_data([user]);

for event in filter_by_event(data[0], "PushEvent"):
    commits = event["payload"]["commits"];
    event["payload"]["commits"] = filter_by_author(commits, ["kishore-ganesh", "Kalpaj Aggrawala"])


# Add difference between previous run and this return
# Read from file  
#Name filter problems