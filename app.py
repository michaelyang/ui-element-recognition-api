import torch
from flask import Flask, request, jsonify
from PIL import Image
from torchvision import transforms
from functools import wraps
import json
import io
import base64
import os
from config import ProductionConfig, DevelopmentConfig
from waitress import serve


def create_app():
    print("⏳ Application starting...")
    app = Flask(__name__)
    app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024  # 16 MB limit
    app.config["UPLOAD_FOLDER"] = "temp_uploads"

    env = os.environ.get("FLASK_ENV")
    if env == "production":
        print("🏠 In production mode")
        app.config.from_object(ProductionConfig())
    elif env == "development":
        print("🛠️ In development mode")
        app.config.from_object(DevelopmentConfig())
    else:
        print(f"❓ Warning: Invalid FLASK_ENV '{env}'. Defaulting to production.")
        app.config.from_object(ProductionConfig())

    print(f"🧪 Flask app created in {env} mode")
    return app


def require_api_key(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        provided_key = request.headers.get("X-API-Key")
        if not provided_key:
            return jsonify({"error": "Missing API key"}), 401
        elif not provided_key == app.config["API_KEY"]:
            return jsonify({"error": "Invalid API key"}), 401
        else:
            return f(*args, **kwargs)

    return decorated


# Load model and other necessary files
model_path = "model/screenrecognition-web350k-vins.torchscript"
m = torch.jit.load(model_path)

img_transforms = transforms.ToTensor()

class_map_path = "metadata/class_map_vins_manual.json"
with open(class_map_path, "r") as f:
    class_map = json.load(f)

idx2Label = class_map["idx2Label"]


def process_image(image: Image, conf_thresh=0.5):
    # Convert image to RGB if it's not already
    if image.mode != "RGB":
        image = image.convert("RGB")

    # Preprocess image
    img_input = img_transforms(image)

    # Make prediction
    with torch.no_grad():
        pred = m([img_input])[1]

    # Process results
    results = []
    max_boxes = 10

    for i in range(min(len(pred[0]["boxes"]), max_boxes)):
        conf_score = pred[0]["scores"][i].item()
        if conf_score > conf_thresh:
            x1, y1, x2, y2 = pred[0]["boxes"][i].tolist()
            label = idx2Label[str(int(pred[0]["labels"][i]))]
            results.append({"bbox": [x1, y1, x2, y2], "label": label, "confidence": conf_score})

    return results


app = create_app()


@app.route("/predict", methods=["POST"])
@require_api_key
def predict():
    if "image" not in request.json:
        return jsonify({"error": "No image provided"}), 400

    conf_thresh = float(request.args.get("confidence", 0.5))

    # Decode base64 image
    image_data = base64.b64decode(request.json["image"])
    image = Image.open(io.BytesIO(image_data))

    results = process_image(image, conf_thresh)
    return jsonify(results)


@app.route("/predict_file", methods=["POST"])
@require_api_key
def predict_file():
    if "image" not in request.files:
        return jsonify({"error": "No image file provided"}), 400

    conf_thresh = float(request.args.get("confidence", 0.5))

    file = request.files["image"]
    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    if file:
        image = Image.open(file.stream)
        results = process_image(image, conf_thresh)
        return jsonify(results)


if __name__ == "__main__":
    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)
    print("Registered routes:")
    for rule in app.url_map.iter_rules():
        print(f"{rule.endpoint}: {rule.methods} {rule.rule}")
    port = os.environ.get("PORT", 8080)
    serve(app, host="0.0.0.0", port=port)
