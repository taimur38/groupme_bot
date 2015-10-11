docker build -t groupme_bot .
docker kill juanita
docker rm juanita
docker run -d -p 7070:5000 --name juanita groupme_bot
