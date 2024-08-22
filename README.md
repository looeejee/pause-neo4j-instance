# Pause Neo4j Aura Instance

GitHub Action to pause a Neo4j Aura Instance that contains a specific keyword in the name.

This Action runs automatically following a cron schedule and uses Neo4j AURA DB REST API to pause a running instance.

For more information on Neo4j AURA Rest API visit https://neo4j.com/docs/aura/platform/api/overview/

# How to Use

For this workflow to run correctly it is necessary to define and add values for the following secrets used by the GitHub Action in repository settings:

```
CLIENT_ID
CLIENT_PWD
TENANT_ID
```

