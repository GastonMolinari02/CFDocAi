from google.cloud import documentai

proofing_processor_name = "projects/{PROJECT_NUMBER}/locations/{LOCATION}/processors/{PROCESSOR_ID}"
us_driver_processor_name = "projects/{PROJECT_NUMBER}/locations/{LOCATION}/processors/{PROCESSOR_ID}"

def proof_request(image_bytes: bytes = b"", mime_type: str = ""):
    client = documentai.DocumentProcessorServiceClient()

    raw_document = documentai.RawDocument(
        content=image_bytes,
        mime_type=mime_type,
    )

    request = documentai.ProcessRequest(name=proofing_processor_name, raw_document=raw_document)

    result = client.process_document(request=request)

    flags = [{"type": f.type_, "status": f.mention_text} for f in result.document.entities]
    
    flags_dict = {f["type"]: f["status"] for f in flags}

    return flags_dict

def us_driver_request(image_bytes: bytes = b"", mime_type: str = ""):
    client = documentai.DocumentProcessorServiceClient()

    raw_document = documentai.RawDocument(
        content=image_bytes,
        mime_type=mime_type,
    )

    request = documentai.ProcessRequest(name=us_driver_processor_name, raw_document=raw_document)

    result = client.process_document(request=request)

    driver_info = {entity.type_: entity.mention_text for entity in result.document.entities}

    return driver_info
