
docker network create pytest-docker-compose-network &> /dev/null
if [ "$?" -ne "0" ]; then
  echo "Network pytest-docker-compose-network already exists"
else
  echo "Created docker network pytest-docker-compose-network"
fi
