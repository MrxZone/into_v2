source "$(dirname ${BASH_SOURCE[0]})/utils.sh"
docker-compose stop into worker worker_did worker_faucet
docker-compose up -d pg rabbitmq redis
waituntil 10 ">>> connect postgres" docker-compose exec pg pg_isready
docker-compose up -d into
docker-compose up -d worker worker_did worker_faucet
sleep 5
docker-compose up -d flower
