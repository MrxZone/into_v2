source "$(dirname ${BASH_SOURCE[0]})/utils.sh"
docker-compose stop into worker worker_did worker_faucet
waituntil 10 ">>> connect postgres" docker-compose exec pg pg_isready
docker-compose up -d into worker worker_did worker_faucet
