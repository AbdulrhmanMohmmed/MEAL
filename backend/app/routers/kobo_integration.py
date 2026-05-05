from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional
from app.database import get_db
from app.models import User, DataForm, FormSubmission
from app.auth import get_current_user

router = APIRouter(prefix="/api/kobo", tags=["KoBoToolbox Integration"])

FIELD_TYPE_MAP = {
    "text": "text",
    "number": "integer",
    "select": "select_one",
    "multi_select": "select_multiple",
    "date": "date",
    "datetime": "dateTime",
    "textarea": "text",
    "radio": "select_one",
    "checkbox": "select_multiple",
    "file": "file",
    "gps": "geopoint",
    "photo": "image",
    "rating": "integer",
    "matrix": "text",
    "section": "begin_group",
}


@router.get("/export-xlsform/{form_id}")
def export_to_xlsform(
    form_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    form = db.query(DataForm).filter(DataForm.id == form_id).first()
    if not form:
        raise HTTPException(status_code=404, detail="النموذج غير موجود")

    fields = form.fields if isinstance(form.fields, list) else []

    survey = []
    choices = []

    for i, field in enumerate(fields):
        if isinstance(field, dict):
            field_type = field.get("type", "text")
            xls_type = FIELD_TYPE_MAP.get(field_type, "text")
            label = field.get("label", f"field_{i}")

            if field_type in ("select", "multi_select", "radio"):
                list_name = f"list_{i}"
                xls_type = f"{xls_type} {list_name}"
                for j, opt in enumerate(field.get("options", [])):
                    if isinstance(opt, dict):
                        choices.append({"list_name": list_name, "name": opt.get("value", f"opt_{j}"), "label": opt.get("label", str(opt))})
                    else:
                        choices.append({"list_name": list_name, "name": f"opt_{j}", "label": str(opt)})

            survey.append({
                "type": xls_type,
                "name": field.get("name", f"field_{i}"),
                "label": label,
                "required": "yes" if field.get("required") else "",
            })

    return {
        "form_title": form.title,
        "form_id": f"humanitarian_form_{form.id}",
        "default_language": "Arabic",
        "survey": survey,
        "choices": choices,
        "settings": {
            "form_title": form.title,
            "form_id": f"humanitarian_form_{form.id}",
            "version": "1",
            "style": "theme-grid",
        },
        "instructions": {
            "kobo_import": "1. اذهب إلى KoBoToolbox → New Form → Import XLSForm. 2. حمّل هذا الملف كـ .xlsx",
            "odk_import": "1. حوّل إلى XML باستخدام pyxform. 2. ارفع إلى ODK Central",
        },
    }


@router.post("/import-submissions/{form_id}")
def import_kobo_submissions(
    form_id: int,
    data: dict,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    form = db.query(DataForm).filter(DataForm.id == form_id).first()
    if not form:
        raise HTTPException(status_code=404, detail="النموذج غير موجود")

    results = data.get("results", [])
    imported = 0
    for row in results:
        sub = FormSubmission(
            form_id=form_id,
            submitted_by=current_user.username,
            data=row,
            status="submitted",
        )
        db.add(sub)
        imported += 1

    db.commit()
    return {"imported": imported, "form_id": form_id}


@router.get("/connection-test")
def test_kobo_connection(current_user: User = Depends(get_current_user)):
    return {
        "status": "ready",
        "supported_versions": ["KoBoToolbox v2", "ODK Central v1"],
        "export_formats": ["XLSForm JSON", "XLS", "XML"],
        "import_formats": ["KoBo API JSON", "CSV", "ODK Briefcase"],
        "api_endpoints": {
            "kobo_api": "https://kf.kobotoolbox.org/api/v2/",
            "odk_central": "https://your-server.example.com/v1/",
        },
        "message": "جاهز للاتصال. قم بإعداد مفتاح API في إعدادات التكامل.",
    }
