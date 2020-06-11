영화 추천 알고리즘

1. 사용자가 좋아요 한 장르 / 영화의 장르 중 가장 수치가 높은 장르의 영화 추천(좋아요, 싫어요, 나중에 표시한 영화 제외)

2. 날씨에 따른 추천(서울 날씨 기반 / 원한다면 현재 위치 기반으로도 가능하도록)

    장르 id를 context에 담아서 넘기고, axois 요청은 vue컴포넌트에서.

3. 사용자가 원하는 장르의 영화 추천 (좋아요, 싫어요 표시한 영화가 존재할 수 있음)





### 특정 장르 영화 가져오기

`https://api.themoviedb.org/3/discover/movie?api_key={API_KEY}&language=ko-KR&sort_by=popularity.desc&include_adult=false&include_video=false&page=1&with_genres=28`



* latitude : 37.4866767
* longitude : 126.94366350000001



`https://api.openweathermap.org/data/2.5/weather?lat=${latitude}&lon=${longitude}&appid=${API_KEY}`



서울 위도, 경도로 데이터 받아와서 영화 추천





사용자가 원하는 장르 영화 추천(평점 순으로)









음.... cardlist 로딩이 너무 오래걸리는데... restapi서버처럼 사용해볼까..