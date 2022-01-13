# from dis import dis
import copy
import functools
import json

def purify_preferences(preferences: list, separator: str = ' ') -> list:
    preference_list = preferences.split(separator)
    num_preferences = int(preference_list[0])
    pure_preferences = ['none'] if (num_preferences == 0) else preference_list[1:]
    return pure_preferences

def create_client(likes: str, dislikes: str) -> list:
    pure_likes = purify_preferences(likes)
    pure_dislikes = purify_preferences(dislikes)
    sorted_likes = sorted(pure_likes)
    sorted_dislikes = sorted(pure_dislikes)
    return [sorted_likes, sorted_dislikes, 1]

def filter_by_dislikes(client_list: list, dislikes: list) -> list:
    clients_sharing_dislikes = list(filter(lambda client: client[1] == dislikes, client_list))
    return clients_sharing_dislikes

def thin_out_by_dislikes(client_list: list, dislikes: list) -> list:
    thinned_out_client_list = list(filter(lambda client: client[1] != dislikes, client_list))
    return thinned_out_client_list

def merge_clients(first_client: list, second_client: list) -> list:
    set_of_likes = set(first_client[0])
    set_of_likes.update(second_client[0])
    list_of_updated_likes = list(set_of_likes)
    sum_of_clients = first_client[2] + second_client[2]
    return [sorted(list_of_updated_likes), first_client[1], sum_of_clients]

def reduce_client_list(client_list: list) -> list:
    reduced_client_list = functools.reduce(lambda a, b: merge_clients(a, b), client_list)
    return reduced_client_list

def group_by_dislikes(client_list: list) -> list:
    ungrouped_client_list = copy.deepcopy(client_list)
    grouped_client_list = []

    while(len(ungrouped_client_list) != 0):
        dislikes = client[1]
        clients_sharing_dislikes = filter_by_dislikes(ungrouped_client_list, dislikes)
        reduced_clients = reduce_client_list(clients_sharing_dislikes)
        ungrouped_client_list = thin_out_by_dislikes(ungrouped_client_list, dislikes)
        grouped_client_list.append(reduced_clients)

    return grouped_client_list

def largest_sublist_by_clients(client_list: list) -> list:
    max_num_clients = 0
    current_largest = None
    for client in client_list:
        if client[2] > max_num_clients:
            current_largest = client
    return current_largest

def format_solution(client: list) -> str:
    solution = str(len(client[0]))

    for ingredient in client[0]:
        solution += " " + ingredient

    return solution

if __name__ == '__main__':

    C = int(input()) # number of potential clients
    client_list = []

    for _ in range(C):
        likes = input().strip() # integer 1 <= L <= 5, followed by L ingredients a client likes
        dislikes = input().strip() # integer 0 <= D <= 5, followed by D ingredients a client dislikes
        client = create_client(likes, dislikes)
        client_list.append(client)
        clients_by_dislikes = group_by_dislikes(client_list)

    # print(json.dumps(client_list, indent=4, sort_keys=False))
    grouped_client_list = group_by_dislikes(client_list)
    # print(json.dumps(grouped_client_list, indent=4, sort_keys=False))
    largest_grouped_list = largest_sublist_by_clients(grouped_client_list)
    formatted_solution = format_solution(largest_grouped_list)
    print(formatted_solution)
