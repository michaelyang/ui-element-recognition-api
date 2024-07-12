# UI Element Recognition API

## API Usage

### Authentication

All API requests require an API key to be provided in the `X-API-Key` header.

### Endpoints

1. POST /predict

   - Accepts a base64 encoded image in the request body
   - Optional query parameter: `confidence` (default: 0.5)

2. POST /predict_file

   - Accepts an image file in multipart/form-data
   - Optional query parameter: `confidence` (default: 0.5)

Example curl command:

```
curl -X POST -H "X-API-Key: your_api_key" -H "Content-Type: application/json"
-d '{"image": "base64_encoded_image_data"}'
"http://localhost:8080/predict?confidence=0.3"
```

---

## Setup

1. Clone the repo
2. Create a `.env` file in project root with:

   ```
   API_KEY=your_api_key
   ```

3. Choose one of the two options for the model and metadata

   - Download the files and place it in `model/` and `metadata/` respectively
   - Uncomment the download lines in Dockerfile

4. Build the Docker image:

   ```
   docker build --no-cache -t ui-element-recognition-api .
   ```

5. Run the container:

   ```
   docker run --env-file .env -p 8080:8080 ui-element-recognition-api
   ```
