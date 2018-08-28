DIR=$(dirname $0)

docker build -t edge-envoy:step3 ${DIR}

if [ -n "" ]; then
    docker tag edge-envoy:step3 edge-envoy:step3
    docker push edge-envoy:step3
fi
