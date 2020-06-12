
result = '['

for i in range(1, 30):
    url = f'https://api.themoviedb.org/3/discover/movie?api_key={API_KEY}&language=ko-KR&region=KR&sort_by=vote_average.desc&include_video=false&page={i}&vote_count.gte=500'

    movies = requests.get(url).json()["results"]

    for movie in movies:
        result += '{"model": "movies.movie","pk": ' + str(movie["id"]) + ',"fields": {'
        result += '"title": "' + movie["title"] + '", '
        result += '"original_title": "' + movie["original_title"] + '", '
        result += '"release_date": "' + movie["release_date"] + '", '
        result += '"popularity": "' + str(movie["popularity"]) + '", '
        result += '"vote_count": "' + str(movie["vote_count"]) + '", '
        result += '"vote_average": "' + str(movie["vote_average"]) + '", '
        result += '"adult": "' + str(movie["adult"]) + '", '
        overview = movie["overview"].replace('"', "'")
        result += '"overview": "' + overview + '", '
        result += '"original_language": "' + movie["original_language"] + '", '
        result += '"poster_path": "' + movie["poster_path"] + '", '
        result += '"backdrop_path": "' + str(movie["backdrop_path"]) + '", '
        result += '"genres": ' + str(movie["genre_ids"]) + '}}, '
        
print(result)

f = open("E:/testoutput2.txt", 'w', -1, "utf-8")
f.write(result)
f.close()
