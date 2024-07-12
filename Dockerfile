FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt


# Copy the entire directory content
COPY . .

# Download the model and metadata files
# RUN mkdir -p /app/model /app/metadata
# RUN pip install gdown
# RUN gdown https://drive.google.com/uc?id=14BjYnwyWhHK8APpWLHj9J7SgoHBLjrMb -O /app/model/screenrecognition-web350k-vins.torchscript
# RUN gdown https://drive.google.com/uc?id=YOUR_CLASS_MAP_FILE_ID -O /app/metadata/class_map_vins_manual.json

EXPOSE 8080

CMD ["python", "app.py"]