DIR=$(dirname $0)

docker build -t usersvc:step2 ${DIR}

if [ -n "" ]; then
    docker tag usersvc:step2 usersvc:step2
    docker push usersvc:step2
fi
