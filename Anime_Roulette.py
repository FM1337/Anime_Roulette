import requests
import json
import random
from urllib.parse import urlparse
import webbrowser


def roulette(u_id):
    a_list = list()
    streamlinks_list = list()
    anime_list = requests.get("https://kitsu.io/api/edge/users/{}/library-entries?page[limit]=1000&filter[status]=planned".format(u_id)).json()
    for anime in anime_list['data']:
        a_list.append(anime['relationships']['anime']['links']['related'])
    while(True):
        try:
            random_anime = requests.get(random.choice(a_list)).json()
            streaming_links = requests.get(random_anime['data']['relationships']['streamingLinks']['links']['related']).json()
            for links in streaming_links['data']:
                streamlinks_list.append(links['attributes']['url'])
            try:
                while(True):
                    random_url = random.choice(streamlinks_list)
                    stream_service = input('is {uri.scheme}://{uri.netloc} okay? (type exit to cancel this choice)'.format(uri=urlparse(random_url)))
                    if stream_service.lower() in ('yes', 'yeah', 'sure', 'okay', 'ok', 'ya', 'hell yeah', 'why not', 'y', 'yup'):
                        print("Okay :)")
                        webbrowser.open_new(random_url)
                        break
                    elif stream_service.lower() == 'exit':
                        print("okay!")
                        break
                    else:
                        print("Alright then...")
                streamlinks_list.clear()
                continue_watch = input("Would you like to continue?")
                if continue_watch.lower() in ('yes', 'yeah', 'sure', 'okay', 'ok', 'ya', 'hell yeah', 'why not', 'y', 'yup'):
                    print("Alright let's do this!")
                else:
                    print("Alright see ya!")
                    break
            except:
                print("Oh shit an error occured, looks like the random chosen anime doesn't have any streaming links!")
        except:
            print("Oh dear, looks like a problem occured, error details {}.")
            keep_going = input("Would you like to keep trying/keep going?")
            if keep_going.lower() in ('yes', 'yeah', 'sure', 'okay', 'ok', 'ya', 'hell yeah', 'why not', 'y', 'yup'):
                print("Alrighty!")
            else:
                print("Cya!")
                break


def get_user_id(username):
    user_information = requests.get("https://kitsu.io/api/edge/users?filter[name]={}".format(username)).json()
    return user_information['data'][0]['id']


choice = input("Would like to select your list from Kitsu.io or try the random picker from Crunchyroll? (cr for crunchyroll, ki for kitsu) ")
if choice.lower() == 'cr':
    while(True):
        webbrowser.open_new('http://www.crunchyroll.com/random/anime?random_ref=topbar')
        again = input("Would you like to watch another random anime?")
        if again.lower() in ('yes', 'yeah', 'sure', 'okay', 'ok', 'ya', 'hell yeah', 'why not', 'y', 'yup'):
            print("Okay here we go!")
        else:
            print("Okay cya!")
            break
elif choice.lower() == 'ki':
    kitsu_username = input("Please enter your kistu username ")  # Ask for Kitsu username
    user_id = get_user_id(kitsu_username)  # Pass it to the function that'll get the ID
    roulette(user_id)  # Pass the newly returned ID to the roulette function
else:
    print("This is not a correct choice!")
