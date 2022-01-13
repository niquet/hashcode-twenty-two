# from dis import dis
import copy
import functools
import json

def purify_preferences(preferences: str, separator: str = ' ') -> list:
    """Removes the integer string from the specified preferences string and sorts it.

    Args:
        preferences (str): Preferences string of type L(ike) or D(islike).
        separator (str, optional): Seperator for splitting the preferences string. Defaults to ' '.

    Returns:
        list: A purified preference in form of a sorted list of strings.
    """
    preference_list = preferences.split(separator)
    num_preferences = int(preference_list[0])
    pure_preferences = ['none'] if (num_preferences == 0) else preference_list[1:]
    return pure_preferences

def create_client(likes: str, dislikes: str) -> list:
    """Creates a client of form [L, D, 1] when given the clients likes and dislikes strings.
       L specifies the purified likes list and D the purified dislikes list.

    Args:
        likes (str): String of likes as per problem statement. Including the integer string
        specifying the amount of likes.
        dislikes (str): String of dislikes as per problem statement. Including the integer string
        specifying the amount of dislikes.

    Returns:
        list: A client list in the form of [L, D, 1] where one represents the number of clients
        matching this description of L and D. Initialized with 1, the client that gets created.
    """
    pure_likes = purify_preferences(likes)
    pure_dislikes = purify_preferences(dislikes)
    sorted_likes = sorted(pure_likes)
    sorted_dislikes = sorted(pure_dislikes)
    return [sorted_likes, sorted_dislikes, 1]

def filter_by_dislikes(client_list: list, dislikes: list) -> list:
    """Receives a list of clients and returns a list of clients that have the specified dislikes D.

    Args:
        client_list (list): List of clients that has the form [[L,D,N]*].
        dislikes (list): A list of dislikes in the form of a sorted list of strings.

    Returns:
        list: Returns a list of clients C in [[L,D,N]*] all for which the condition D == dislikes holds.
    """
    clients_sharing_dislikes = list(filter(lambda client: client[1] == dislikes, client_list))
    return clients_sharing_dislikes

def thin_out_by_dislikes(client_list: list, dislikes: list) -> list:
    """Receives a list of clients and returns a list of clients that don't have the specified dislikes D.

    Args:
        client_list (list): List of clients that has the form [[L,D,N]*].
        dislikes (list): A list of dislikes in the form of a sorted list of strings.

    Returns:
        list: Returns a list of clients C in [[L,D,N]*] all for which the condition D != dislikes holds.
    """
    thinned_out_client_list = list(filter(lambda client: client[1] != dislikes, client_list))
    return thinned_out_client_list

def merge_clients(first_client: list, second_client: list) -> list:
    """Receives two clients of the form [L, D, N] and merges them together into one client.
    It is assumed that they share the same dislikes.

    Args:
        first_client (list): A client list in the form of [L, D, 1] where one represents the number of clients
        matching this description of L and D.
        second_client (list): See 'first_client (list)'.

    Returns:
        list: Returns a client [L, D, N], where the likes of both clients are included and N represents the
        number of clients matching this new description of L and D.
    """
    set_of_likes = set(first_client[0])
    set_of_likes.update(second_client[0])
    list_of_updated_likes = list(set_of_likes)
    sum_of_clients = first_client[2] + second_client[2]
    return [sorted(list_of_updated_likes), first_client[1], sum_of_clients]

def reduce_client_list(client_list: list) -> list:
    """Receives a list of clients and returns a single aggregated client. Assumes that all of the clients in
    have the list share the same dislikes.

    Args:
        client_list (list): List of clients that has the form [[L,D,N]*].

    Returns:
        list: A client [L, D, N] that is an aggregation over all the clients likes and the number of clients
        that represents each client description. (Likes are merged and the number of clients get summed up).
    """
    reduced_client_list = functools.reduce(lambda a, b: merge_clients(a, b), client_list)
    return reduced_client_list

def group_by_dislikes(client_list: list) -> list:
    """[summary]

    Args:
        client_list (list): [description]

    Returns:
        list: [description]
    """
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
    """[summary]

    Args:
        client_list (list): [description]

    Returns:
        list: [description]
    """
    max_num_clients = 0
    current_largest = None
    for client in client_list:
        if client[2] > max_num_clients:
            current_largest = client
    return current_largest

def format_solution(client: list) -> str:
    """[summary]

    Args:
        client (list): [description]

    Returns:
        str: [description]
    """
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
