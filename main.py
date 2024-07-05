import base64
import functions_framework
import flask
from generate import PROMPT, generate_from_image
from proof import proof_request, us_driver_request
import magic
mime = magic.Magic(mime=True)

@functions_framework.http
def process_id(request: flask.Request) -> flask.typing.ResponseReturnValue:
    if not (j := request.json) or not (img_b64 := j.get("img")):
        return {"err": "invalid request"}, 400

    img_bytes = base64.b64decode(img_b64)

    if (mime_type := mime.from_buffer(img_bytes)) not in ["image/jpeg", "image/png"]:
        return {"err": f"unsupported filetype {mime_type}"}, 400

    gemini_response = generate_from_image(PROMPT, image_bytes=img_bytes)
    proof_response = proof_request(image_bytes=img_bytes, mime_type=mime_type)
    driver_response = us_driver_request(image_bytes=img_bytes, mime_type=mime_type)  # Llamar a la nueva función

    print(proof_response)
    print(driver_response)

    return {"gemini_response": gemini_response, "proofing_response": proof_response, "driver_response": driver_response}, 200
