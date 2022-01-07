import json

if __name__ == '__main__':

    C = int(input()) # number of potential clients
    clients = {}
    ingredients = set()

    for client in range(2 * C):
        L = input().strip() # integer 1 <= L <= 5, followed by L ingredients a client likes
        D = input().strip() # integer 0 <= D <= 5, followed by D ingredients a client dislikes
        print(L)
        print(D)
        #clients[client] = [L[1:], D[1:]]
        #preferences = L[1:] + D[1:]
        #ingredients.update(preferences)
    
    parsed = json.loads(clients)
    print(json.dumps(parsed, indent=4, sort_keys=False))

    parsed = json.loads(ingredients)
    print(json.dumps(parsed, indent=4, sort_keys=False))
