from base64 import b64encode
import json
from os import listdir
import vertexai
from vertexai.generative_models import GenerativeModel, Part
import vertexai.preview.generative_models as generative_models

LOCATION = "us-central1"
PROMPT = """Please translate the data in this image, to a JSON object with this fields:
    documentType
    documentNumber
    name
    lastName
    dateOfBirth
    address
    zipCode
    state
    gender
    country

    if no data is found for a field, mark it as null.
    please include only the JSON object in your response."""

vertexai.init(location=LOCATION)
model = GenerativeModel(
    "gemini-1.5-flash"
)


def generate_from_image(prompt: str, image_path: str | None = None, image_bytes: bytes | None = None):
    if image_path:
        with open(image_path, "rb") as image_file:
            data = image_file.read()
    elif image_bytes:
        data = image_bytes
    else:
        raise Exception("Missing image_path or image_bytes")

    image1 = Part.from_data(
        mime_type="image/jpeg",
        data=data)

    res = model.generate_content(
        [
            prompt,
            image1
        ],
        generation_config={
            "max_output_tokens": 8192,
            "temperature": 1,
            "top_p": 0.95,
        },
        safety_settings={
            generative_models.HarmCategory.HARM_CATEGORY_HATE_SPEECH: generative_models.HarmBlockThreshold.BLOCK_ONLY_HIGH,
            generative_models.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: generative_models.HarmBlockThreshold.BLOCK_ONLY_HIGH,
            generative_models.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: generative_models.HarmBlockThreshold.BLOCK_ONLY_HIGH,
            generative_models.HarmCategory.HARM_CATEGORY_HARASSMENT: generative_models.HarmBlockThreshold.BLOCK_ONLY_HIGH,
        },
        stream=False,
    )
    try:
        return json.loads(res.text)
    except Exception as e:
        print(e)
        return None


if __name__ == "__main__":
    for img in listdir("examples/"):
        with open("examples/"+img, "rb") as f:
            data = b64encode(f.read()).decode()
        with open(f"out/{img}.json", "w+") as f:
            json.dump({"img": data}, f)
