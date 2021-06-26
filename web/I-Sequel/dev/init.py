with open('movies.csv', 'r') as fp:
    movies = fp.readlines()
    count = 0
    for i in movies[1:25]:
        if ("'" in i):
            continue
        data = i.split(',')
        print("INSERT INTO movies VALUES (" + str(count) + ", '" + data[0] + "', '" + data[-2][:-1] + "');")
        count += 1