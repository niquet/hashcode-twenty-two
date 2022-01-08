import json

if __name__ == '__main__':

    C = int(input()) # number of potential clients
    clients = {}
    ingredients = set()

    for client in range(C):
        L = input().strip() # integer 1 <= L <= 5, followed by L ingredients a client likes
        D = input().strip() # integer 0 <= D <= 5, followed by D ingredients a client dislikes
        print(L)
        print(D)
        clients[client] = [L[2:], D[2:]]
        preferences = L[2:].split() + D[2:].split()
        ingredients.update(preferences)

    print(json.dumps(clients, indent=4, sort_keys=False))

    print(json.dumps(list(ingredients), indent=4, sort_keys=False))
