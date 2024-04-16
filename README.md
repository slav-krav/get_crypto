# get_crypto
Minimalistic API that provides info about cryptocurrency prices across different platforms.

Supported platforms:
`bybit`, `binance`

## How to run?
Locally could be launched via `docker-compose up` command from apps directory.  
Then open `http://0.0.0.0:8080/` with your browser and click "Try it out" button on any endpoint of your interest.

## DB Setup
Application supports PostgreSQL database. To configure connection set up following environment variables:
`DB_HOST` - host or socket (in case of Cloud Run socket connections use `/cloudsql/project:reguon:postgres_name` format)
`DB_PORT` - default: `5432`
`DB_USER` - default: `postgres`
`DB_PASSWORD` - user's password
`DB_NAME` - default: `postgres`
