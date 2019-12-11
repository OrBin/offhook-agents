# Offhook Agents

## Agents API
API for the agents is specified in `openapi/openapi.yml`, based on OpenAPI Specification V2.0.

## Generating a new server code
Assuming you want to generate a `python-flask` server code into `./generated-server` directory:

```bash
docker run --rm \
    -v ${PWD}/openapi/openapi.yml:/openapi.yml:ro \
    -v ${PWD}/generated-server:/out \
    -w / \
    swaggerapi/swagger-codegen-cli:2.4.10 generate \
        -i ./openapi.yml \
        -l python-flask \
        -o ./out

sudo chown -R $(id -u):$(id -g) generated-server/
```
