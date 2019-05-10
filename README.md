# README
## build
```
docker build -t flask_docker .
```

## start
```
docker-compose up
```

## How To Use
```
curl -X POST -H 'Accept:application/json' -H 'Content-Type:application/json' http://localhost:5000/mask -d '{"text":"フジテレビ系「バイキング」は２３日、ＮＧＴ４８の山口真帆（２３）のグループ卒業の話題を取り上げた。"}' 
```

## Release
```
heroku container:login
heroku create masking-api
heroku container:push --app masking-api web
heroku container:release --app masking-api web
heroku open --app masking-api
```
