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

### Local

1. Clone the repo
2. Create a `.env` file in project root with:

   ```
   API_KEY=your_api_key
   ```

3. Download the files and place it in `model/` and `metadata/` respectively

4. Create a virtual envionment

   ```
   pipenv shell
   ```

5. Install requirements

   ```
   pipenv install -r requirements.txt
   ```

6. Run the script

   ```
   python app.py
   ```

### Docker

1. Clone the repo
2. Create a `.env` file in project root

   ```
   API_KEY=your_api_key
   ```

3. Choose one of the two options for the model and metadata

   - Download the files and place it in `model/` and `metadata/` respectively
   - Uncomment the download lines in Dockerfile

4. Build the Docker image

   ```
   docker build --no-cache -t ui-element-recognition-api .
   ```

5. Run the container

   ```
   docker run --env-file .env -p 8080:8080 ui-element-recognition-api
   ```

## Deploy to Render

1. Login to Gitlab CLI

   ```
   docker login registry.gitlab.com
   ```

2. Build (Render only supports images built with the platform `linux/amd64`, which is significantly larger/slower)

   ```
   docker build --platform=linux/amd64 -t registry.gitlab.com/it-is-what-it-is/it-is-what-it-is .
   ```

3. Add image to resgistry

   ```
   docker push registry.gitlab.com/it-is-what-it-is/it-is-what-it-is
   ```

4. Create an Access Token with `read_registry` permission

5. Copy the URL for the registry and add the credentials on Render

6. Set Environment Variables

7. Deploy!

## Deploy to Fly.io

1. Install `flyctl`

   ```
   brew install flyctl
   ```

2. Login to Fly.io

   ```
   fly auth login
   ```

3. Set secrets

   ```
   fly secrets set FLASK_ENV=production
   fly secrets set API_KEY=...
   ```

4. Deploy from source directory

   ```
   fly launch # for first deploy
   fly deploy # for redeploys
   ```
