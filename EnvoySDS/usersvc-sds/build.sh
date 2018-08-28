DIR=$(dirname $0)

docker build -t usersvc-sds:step2 ${DIR}

if [ -n "" ]; then
    docker tag usersvc-sds:step2 usersvc-sds:step2
    docker push usersvc-sds:step2
fi
