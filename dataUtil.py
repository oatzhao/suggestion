import pandas as pd
import math
import sys


# unames = ['user_id', 'gender', 'age', 'occupation', 'zip']
# users = pd.read_table('ml-1m/users.dat', sep='::', header=None, names=unames)
#
# mnames = ['movie_id', 'title', 'genres']
# movies = pd.read_table('ml-1m/movies.dat', sep='::', header=None, names=mnames)
#
# rnames = ['user_id', 'movie_id', 'rating', 'timestamp']
# ratings = pd.read_table('ml-1m/ratings.dat', sep= "::", header=None, names= rnames )
#
# all_data = pd.merge(pd.merge(ratings, users), movies)
# data = pd.DataFrame(data=all_data, columns=['user_id', 'movie_id'])
# data.to_csv('data.csv')

def recommend(user,user_item,W,K):
    rank={}
    interacted_items=user_item[user]
    for v,wuv in sorted(W[user].items(),reverse=True)[0:K]:
        for i in user_item[v]:
            if i not in interacted_items:
                if i not in rank :
                    rank.setdefault(i,0)
                rank[i]+=wuv
    return rank

if __name__ == '__main__':
    data = pd.read_csv('data.csv')
    X = data['user_id']
    Y = data['movie_id']

    item_user = dict()
    testX = X.count()
    for i in range(X.count()):
        user = X.iloc[i]
        item = Y.iloc[i]
        if item not in item_user:
            item_user[item] = set()
        item_user[item].add(user)

    testY = Y.count()
    user_item = dict()
    for i in range(Y.count()):
        user = X.iloc[i]
        item = Y.iloc[i]
        if user not in user_item:
            user_item[user] = set()
        user_item[user].add(item)

    C = {}
    N = {}
    for i, users in item_user.items():
        for u in users:
            N.setdefault(u, 0)
            N[u] += 1
            C.setdefault(u, {})
            for v in users:
                if u == v:
                    continue
                C[u].setdefault(v, 0)
                C[u][v] += 1

    # 用相似度代替原来两个用户之间共同电影评价数
    W = C.copy()
    for u, related_users in C.items():
        for v, cuv in related_users.items():
            W[u][v] = cuv / math.sqrt(N[u] * N[v])

    rank = recommend(1, user_item, W, 5)
    print(rank)





