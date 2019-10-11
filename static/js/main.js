
function connect() {
  var mainrow = document.getElementById("mainrow");
  var status = document.getElementById("status");
  var movies = []
  afkp_socket = new WebSocket("ws://127.0.0.1:8080/ws");
  //var rating_imdb = 0;
  console.log("***CREATED WEBSOCKET");

  afkp_socket.onopen = function(evt) {
    console.log("***ONOPEN");
    status.innerHTML = 'загружаем результаты... <img src="static/loading.gif" width="150" height="50">';
  };
  console.log("***CREATED ONOPEN");

  afkp_socket.onmessage = function (event) {
    if (event.data == 'completed'){
      console.log('completed');
      mainrow.innerHTML = '';
      setTimeout(function(){sortMovies(movies);}, 1000);
      status.innerHTML = '<div>отсортировано по рейтингу IMDB</div>';
    } else {
      var movie = JSON.parse(event.data);
      movies.push(movie);
      insertMovie(movie);
    }
  }
}

function sortMovies(movies) {
  movies.sort(compare);
  status.innerHTML = ''

  for (var i = 0; i < movies.length; i++) {
    insertMovie(movies[i]);
  }
}

function timer(ms) {
 return new Promise(res => setTimeout(res, ms));
}

function insertMovie(movie) {
  where = 'afterbegin'
  if (movie.rating_imdb !== undefined){
    imdb_link = ' <a href="https://www.imdb.com/title/' + movie.id_imdb + '/" class="btn btn-sm btn-outline-secondary">IMDB ' + movie.rating_imdb + '</a> '
  } else {
    imdb_link = ''
  }
  if (movie.rating_kp !== null){
    kp_link = ' <a href="https://www.kinopoisk.ru/film/' + movie.id_kinopoisk + '/" class="btn btn-sm btn-outline-secondary">КП ' + movie.rating_kp + '</a> '
  } else {
    kp_link = ''
  }
  var html = '<div class="col-md-4"><div class="card mb-4 box-shadow"><img class="card-img-top" src="https://st.kp.yandex.net/images/film_iphone/iphone360_' + movie.id_kinopoisk + '.jpg" alt="' + movie.title + ', ' + movie.year + '" title="' + movie.title + ', ' + movie.year + '">                      <div class="card-body">                        <p class="card-text"><h4>' + movie.title + '</h4><h6>' + movie.title_eng + '</h6><p></p><p>' + movie.year + '<p><p>'+ movie.runtime + '</p><p>' + movie.descr + '</p><div class="d-flex justify-content-between align-items-center"><div class="btn-group"><a href="https://www.afisha.ru/movie/' + movie.id_afisha + '" class="btn btn-sm btn-outline-secondary">Афиша</a>' + kp_link + imdb_link + '</div></div></div></div></div>'
  $(html).appendTo('#mainrow').show('slow');
}


function compare(a, b) {
  if (a.rating_imdb < b.rating_imdb ){
    return 1;
  }
  if (a.rating_imdb > b.rating_imdb ){
    return -1;
  }
  return 0;
}
