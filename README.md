# BERT SLS Worker

## Building the Docker Image

To build and push the Docker image, use the following commands:

```bash
docker build --tag user-name/image:latest . --platform=linux/amd64
docker push user-name/image:latest
```

## Sending a Request with CURL

Use the following CURL command to send a POST request:

```bash
curl -X POST "https://api.runpod.ai/v2/endpoint/runsync" \
     -H "accept: application/json" \
     -H "content-type: application/json" \
     -H "authorization: YOUR_API_KEY" \
     -d '{
        "input": {
            "sequence": "The weather is sunny today.",
            "labels": ["weather", "sports", "news"]
        }
     }'
```

## Example JSON Payload

Here is an example of the JSON payload used in the CURL request:

```json
{
    "input": {
        "sequence": "The weather is sunny today.",
        "labels": ["weather", "sports", "news"]
    }
}
```
