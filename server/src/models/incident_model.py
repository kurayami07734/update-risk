from datetime import datetime


def build_incident_document(extracted_data: dict, reference_url: str):
    
    print(extracted_data)
    document = {
        "package_name": extracted_data.get("package_name"),
        "version_affected": extracted_data.get("version_affected"),
        "risk_description": extracted_data.get("risk_description"),
        "suggested_solution": extracted_data.get("suggested_solution"),
        "resolved_at": extracted_data.get("resolved_at"),
        "reference_url": reference_url,
        "created_at": datetime.utcnow(),
    }

    clean_document = {
        key: value
        for key, value in document.items()
        if value not in (None, "", [])
    }

    llm_fields = [
        "package_name",
        "version_affected",
        "risk_description",
        "suggested_solution",
        "resolved_at",
    ]

    if all(field not in clean_document for field in llm_fields):
        return None

    return clean_document
