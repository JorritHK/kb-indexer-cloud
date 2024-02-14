## Test using development setup

This folder contains some configuration and deployment files to quickly create the needed systems for testing:
- elasticsearch container
- kb-indexer container
and the connections between the two

### Installationi and deployment
For this you need docker and docker-compose

To run deployment env on you own machine:
- `docker-compose up`
- `docker exec -it dev_deployment_kb_indexer_1 /bin/bash`
- Run the command on the indexer

To inspect created indexes:
`curl -X GET 'Http://localhost:9200/_aliases?pretty=true'`

Should be expanded in the future when more sophisticated ways of interacting with the indexer are added
