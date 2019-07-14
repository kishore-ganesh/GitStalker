# Data is array of responses
import requests
import iso8601
import configparser
config = configparser.ConfigParser()
config.read("api_config")

# import argparse
file_name = "users.config"
event = "PushEvent"
token = config["DEFAULT"]["github_token"]
def user_events_url(user):
    return "https://api.github.com/users/"+user+"/events"

def get_data(users):
    data = [];
    for user in users:
        user_data = []
        response = requests.get(
            user_events_url(user),
            headers = {'Authorization': token}
        )
        url = response.links["last"]["url"]
        last = int(url[url.find("?page=")+len("?page="):])
        response = response.json()
        month = iso8601.parse_date(response[0]["created_at"]).month
        user_data.extend(response)
        page = 2        
        while(iso8601.parse_date(response[len(response)-1]["created_at"]).month>month-1 and page <= last):
            response = requests.get(
                user_events_url(user),
                params = {'page': page},
                headers = {'Authorization': token}
                ).json()
            page = page + 1
            user_data.extend(response)
        data.append(user_data)
    return data
def filter_by_event(events, event_type):
    return list(filter(lambda x: x["type"] == event_type, events))
def filter_by_author(commits, authors):
    tmp = []
    for author in authors:
        tmp.extend(list((filter(lambda x: x["author"]["name"] == author, commits))));
    return tmp
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
    return requests.get(get_name_url(name), headers = {'Authorization': token}).json()["name"]
def remove_empty(data):
    return list(filter(lambda item: len(item["payload"]["commits"])>0, data))
def print_item(data):
    for item in data:
        print("{} has pushed {} commits to {}".format(item["actor"]["login"], len(item["payload"]["commits"]), item["repo"]["name"]))
if __name__ == "__main__":
    users = return_users_from_file(file_name)
    data = get_data(users)
    for index,item in enumerate(data):
        data[index] = list(filter_by_event(item, event));
    data = list(filter(lambda item: len(item)>0, data));
    for response in data:
        author_name = get_name(response[0]["actor"]["login"])
        for item in response:
            # print(item)
            item["payload"]["commits"] = filter_by_author(item["payload"]["commits"],[item["actor"]["login"], author_name])

    for index, item in enumerate(data):
        data[index] = remove_empty(item)
    for item in data:
        print_item(item)

    print(data)


# data = get_data([user]);

# for event in filter_by_event(data[0], "PushEvent"):
#     commits = event["payload"]["commits"];
#     event["payload"]["commits"] = filter_by_author(commits, ["kishore-ganesh", "Kalpaj Aggrawala"])


# Add difference between previous run and this return
# Read from file  
#Name filter problems
#On Each run, store the results. On next run, just give the diff, i.e filter y dat
#Let it go back one month