#!/bin/bash

# Parse flags
while getopts "d:l:" opt; do
  case $opt in
    d) output_dir=$OPTARG      ;;
    l) language=$OPTARG   ;;
    *) echo 'error' >&2
       exit 1
  esac
done

# Validate inputs
if [ -z "${output_dir+x}" ]; then
    echo 'Option -d missing (should specify an output directory)' >&2
    exit 1
fi

if [ -z "${language+x}" ]; then
    echo 'Option -l missing (should specify language for the generated server)' >&2
    exit 1
fi

# Convert to absolute paths
output_dir=$(readlink -f $output_dir)
openapi_file=$(readlink -f ./openapi/openapi.yml)

# Generate the server code
docker run --rm \
    -v $openapi_file:/openapi.yml:ro \
    -v $output_dir:/out \
    -w / \
    swaggerapi/swagger-codegen-cli:2.4.10 generate \
        -i ./openapi.yml \
        -l $language \
        -o ./out

# Apply appropriate permissions to the generated code
sudo chown -R $(id -u):$(id -g) $output_dir
