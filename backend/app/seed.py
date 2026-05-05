from sqlalchemy.orm import Session
from datetime import date, datetime, timedelta
from app.models import (
    User, Beneficiary, Project, Activity, Indicator, Measurement,
    Grant, Transaction, Employee, Warehouse, InventoryItem, Distribution,
    CashTransfer, DataForm, Complaint, LogFrame, FieldVisit,
    RiskRegister, LessonLearned, MEALPlan, Document, Notification
)
from app.auth import get_password_hash
import random

GOVERNORATES = ["صنعاء", "عدن", "تعز", "الحديدة", "إب", "مأرب", "حضرموت", "ذمار", "عمران", "صعدة", "لحج", "أبين"]
SECTORS = ["الصحة", "التعليم", "الأمن الغذائي", "المياه والصرف الصحي", "الحماية", "المأوى", "التغذية"]
DONORS = ["USAID", "ECHO", "DFID", "OCHA/CERF", "WFP", "UNICEF", "WHO", "KSRelief"]


def seed_database(db: Session):
    if db.query(User).first():
        return

    # Users
    users = [
        User(username="admin", full_name="مدير النظام", email="admin@meal.org", hashed_password=get_password_hash("admin123"), role="admin", department="الإدارة"),
        User(username="meal_officer", full_name="أحمد محمد - مسؤول MEAL", email="meal@meal.org", hashed_password=get_password_hash("pass123"), role="meal_officer", department="المتابعة والتقييم"),
        User(username="manager1", full_name="سارة أحمد - مدير برامج", email="manager@meal.org", hashed_password=get_password_hash("pass123"), role="manager", department="البرامج"),
        User(username="field1", full_name="محمد علي - موظف ميداني", email="field@meal.org", hashed_password=get_password_hash("pass123"), role="field_officer", department="الميداني"),
        User(username="finance1", full_name="فاطمة حسن - مالية", email="finance@meal.org", hashed_password=get_password_hash("pass123"), role="finance", department="المالية"),
        User(username="hr1", full_name="خالد عبدالله - موارد بشرية", email="hr@meal.org", hashed_password=get_password_hash("pass123"), role="hr", department="الموارد البشرية"),
    ]
    db.add_all(users)
    db.flush()

    # Projects
    projects = [
        Project(name="مشروع الاستجابة الصحية الطارئة", code="HLT-2024-001", description="توفير خدمات صحية أولية في المناطق المتأثرة بالنزاع", sector="الصحة", status="active", start_date=date(2024, 1, 1), end_date=date(2025, 12, 31), budget=850000, spent=425000, governorate="تعز", donor="WHO", target_beneficiaries=50000, reached_beneficiaries=32000),
        Project(name="برنامج الأمن الغذائي", code="FSL-2024-002", description="توزيع سلال غذائية وتحويلات نقدية للأسر الأكثر ضعفاً", sector="الأمن الغذائي", status="active", start_date=date(2024, 3, 1), end_date=date(2025, 6, 30), budget=1200000, spent=680000, governorate="الحديدة", donor="WFP", target_beneficiaries=80000, reached_beneficiaries=55000),
        Project(name="مشروع المياه والصرف الصحي", code="WSH-2024-003", description="إعادة تأهيل شبكات المياه وبناء مرافق صرف صحي", sector="المياه والصرف الصحي", status="active", start_date=date(2024, 2, 1), end_date=date(2025, 8, 31), budget=650000, spent=290000, governorate="مأرب", donor="UNICEF", target_beneficiaries=35000, reached_beneficiaries=18000),
        Project(name="برنامج التعليم في حالات الطوارئ", code="EDU-2024-004", description="دعم التعليم في المناطق المتأثرة وتوفير مستلزمات تعليمية", sector="التعليم", status="active", start_date=date(2024, 4, 1), end_date=date(2025, 3, 31), budget=450000, spent=180000, governorate="صنعاء", donor="ECHO", target_beneficiaries=25000, reached_beneficiaries=12000),
        Project(name="مشروع الحماية والدعم النفسي", code="PRT-2024-005", description="خدمات حماية ودعم نفسي اجتماعي للنساء والأطفال", sector="الحماية", status="active", start_date=date(2024, 5, 1), end_date=date(2025, 4, 30), budget=380000, spent=152000, governorate="عدن", donor="USAID", target_beneficiaries=15000, reached_beneficiaries=8500),
        Project(name="برنامج المأوى الطارئ", code="SHL-2024-006", description="توفير مأوى للنازحين في المخيمات", sector="المأوى", status="completed", start_date=date(2023, 6, 1), end_date=date(2024, 5, 31), budget=520000, spent=498000, governorate="مأرب", donor="KSRelief", target_beneficiaries=20000, reached_beneficiaries=19500),
        Project(name="مشروع التغذية العلاجية", code="NUT-2024-007", description="علاج سوء التغذية الحاد لدى الأطفال دون الخامسة", sector="التغذية", status="active", start_date=date(2024, 1, 15), end_date=date(2025, 7, 15), budget=720000, spent=380000, governorate="الحديدة", donor="UNICEF", target_beneficiaries=30000, reached_beneficiaries=20000),
        Project(name="مشروع سبل العيش", code="LVH-2024-008", description="دعم سبل العيش والتمكين الاقتصادي للأسر المتأثرة", sector="الأمن الغذائي", status="planned", start_date=date(2025, 1, 1), end_date=date(2026, 6, 30), budget=900000, spent=0, governorate="إب", donor="DFID", target_beneficiaries=40000, reached_beneficiaries=0),
    ]
    db.add_all(projects)
    db.flush()

    # Beneficiaries
    names_m = ["محمد أحمد", "علي حسن", "عبدالله صالح", "خالد محمد", "أحمد عبدالرحمن", "يوسف إبراهيم", "عمر فاروق", "حسين علي", "ناصر أحمد", "سالم محمد"]
    names_f = ["فاطمة محمد", "عائشة أحمد", "مريم علي", "نورة حسن", "سارة عبدالله", "هدى صالح", "أمل خالد", "رقية محمد", "زينب إبراهيم", "سمية أحمد"]
    beneficiaries = []
    for i in range(150):
        is_female = i % 3 == 0
        name = random.choice(names_f if is_female else names_m) + f" ({i+1})"
        gov = random.choice(GOVERNORATES)
        beneficiaries.append(Beneficiary(
            national_id=f"YEM{i+1:08d}",
            full_name=name,
            gender="female" if is_female else "male",
            date_of_birth=date(1970 + random.randint(0, 40), random.randint(1, 12), random.randint(1, 28)),
            phone=f"77{random.randint(1000000, 9999999)}",
            governorate=gov,
            district=f"مديرية {random.randint(1, 5)}",
            household_size=random.randint(3, 12),
            vulnerability_score=round(random.uniform(1, 10), 1),
            status="active",
            is_idp=random.random() > 0.6,
            disability=random.random() > 0.85,
            female_headed=is_female and random.random() > 0.5,
            latitude=13.5 + random.uniform(0, 3),
            longitude=44.0 + random.uniform(0, 4)
        ))
    db.add_all(beneficiaries)
    db.flush()

    # Indicators
    indicators_data = [
        ("عدد المستفيدين من الخدمات الصحية", "output", "شخص", 0, 50000, 32000, 1, "الصحة"),
        ("نسبة التغطية بالتحصين", "outcome", "%", 45, 85, 72, 1, "الصحة"),
        ("عدد الأسر المستفيدة من السلال الغذائية", "output", "أسرة", 0, 80000, 55000, 2, "الأمن الغذائي"),
        ("نسبة الأسر ذات الاستهلاك الغذائي المقبول", "outcome", "%", 35, 70, 58, 2, "الأمن الغذائي"),
        ("عدد مرافق المياه المعاد تأهيلها", "output", "مرفق", 0, 45, 28, 3, "المياه والصرف الصحي"),
        ("نسبة السكان مع وصول آمن للمياه", "outcome", "%", 30, 75, 52, 3, "المياه والصرف الصحي"),
        ("عدد الأطفال الملتحقين بالمدارس", "output", "طفل", 0, 25000, 12000, 4, "التعليم"),
        ("معدل الحضور المدرسي", "outcome", "%", 55, 85, 73, 4, "التعليم"),
        ("عدد النساء المستفيدات من خدمات الحماية", "output", "امرأة", 0, 8000, 5200, 5, "الحماية"),
        ("نسبة الحالات المحالة والمتابعة", "outcome", "%", 40, 90, 78, 5, "الحماية"),
        ("عدد الأطفال المعالجين من سوء التغذية", "output", "طفل", 0, 30000, 20000, 7, "التغذية"),
        ("معدل الشفاء من سوء التغذية الحاد", "outcome", "%", 65, 90, 82, 7, "التغذية"),
    ]
    indicators = []
    for name, itype, unit, baseline, target, current, proj_id, sector in indicators_data:
        ind = Indicator(
            project_id=proj_id, name=name, indicator_type=itype,
            unit=unit, baseline=baseline, target=target, current_value=current,
            data_source="تقارير ميدانية", frequency="monthly",
            responsible="مسؤول MEAL", sector=sector
        )
        indicators.append(ind)
    db.add_all(indicators)
    db.flush()

    # Measurements
    for ind in indicators:
        base_val = ind.baseline
        increment = (ind.current_value - ind.baseline) / 12
        for month in range(12):
            val = base_val + increment * (month + 1) + random.uniform(-increment * 0.2, increment * 0.2)
            db.add(Measurement(
                indicator_id=ind.id,
                value=round(val, 1),
                date=date(2024, month + 1, 15),
                collected_by="مسؤول MEAL",
                verified=month < 10
            ))

    # Grants
    grants = [
        Grant(name="منحة الاستجابة الصحية", donor="WHO", amount=850000, currency="USD", start_date=date(2024, 1, 1), end_date=date(2025, 12, 31), status="active", spent=425000, reporting_frequency="quarterly"),
        Grant(name="برنامج الأمن الغذائي الطارئ", donor="WFP", amount=1200000, currency="USD", start_date=date(2024, 3, 1), end_date=date(2025, 6, 30), status="active", spent=680000, reporting_frequency="monthly"),
        Grant(name="مشروع المياه - UNICEF", donor="UNICEF", amount=650000, currency="USD", start_date=date(2024, 2, 1), end_date=date(2025, 8, 31), status="active", spent=290000, reporting_frequency="quarterly"),
        Grant(name="التعليم في الطوارئ", donor="ECHO", amount=450000, currency="EUR", start_date=date(2024, 4, 1), end_date=date(2025, 3, 31), status="active", spent=180000, reporting_frequency="quarterly"),
        Grant(name="برنامج الحماية", donor="USAID", amount=380000, currency="USD", start_date=date(2024, 5, 1), end_date=date(2025, 4, 30), status="active", spent=152000, reporting_frequency="quarterly"),
        Grant(name="المأوى الطارئ", donor="KSRelief", amount=520000, currency="USD", start_date=date(2023, 6, 1), end_date=date(2024, 5, 31), status="completed", spent=498000, reporting_frequency="monthly"),
    ]
    db.add_all(grants)
    db.flush()

    # Transactions
    categories = ["رواتب", "مشتريات", "نقل", "إيجار", "تدريب", "معدات", "مواد"]
    for g in grants:
        for i in range(8):
            db.add(Transaction(
                grant_id=g.id, transaction_type="expense",
                amount=round(g.spent / 8, 2), currency=g.currency,
                description=f"مصروفات {random.choice(categories)}",
                category=random.choice(categories),
                date=date(2024, random.randint(1, 12), random.randint(1, 28)),
                reference_number=f"TXN-{g.id}-{i+1:03d}"
            ))

    # Employees
    departments = ["البرامج", "المتابعة والتقييم", "المالية", "الموارد البشرية", "اللوجستيات", "الإدارة"]
    positions = ["مدير برامج", "مسؤول MEAL", "محاسب", "مسؤول موارد بشرية", "مسؤول لوجستي", "موظف ميداني", "منسق مشروع"]
    for i in range(30):
        db.add(Employee(
            employee_id=f"EMP-{i+1:03d}",
            full_name=f"موظف {i+1}",
            email=f"emp{i+1}@meal.org",
            phone=f"73{random.randint(1000000, 9999999)}",
            department=random.choice(departments),
            position=random.choice(positions),
            status="active",
            join_date=date(2020 + random.randint(0, 4), random.randint(1, 12), 1),
            salary=random.randint(800, 3000),
            contract_type=random.choice(["full_time", "part_time", "consultant"]),
            location=random.choice(GOVERNORATES[:6])
        ))

    # Warehouses & Inventory
    warehouses = [
        Warehouse(name="المستودع الرئيسي - صنعاء", location="صنعاء", governorate="صنعاء", capacity=5000, manager="أحمد محمد"),
        Warehouse(name="مستودع عدن", location="عدن", governorate="عدن", capacity=3000, manager="علي حسن"),
        Warehouse(name="مستودع تعز", location="تعز", governorate="تعز", capacity=2500, manager="محمد صالح"),
        Warehouse(name="مستودع الحديدة", location="الحديدة", governorate="الحديدة", capacity=4000, manager="خالد أحمد"),
        Warehouse(name="مستودع مأرب", location="مأرب", governorate="مأرب", capacity=2000, manager="ناصر علي"),
    ]
    db.add_all(warehouses)
    db.flush()

    items = ["أرز", "زيت طبخ", "سكر", "دقيق", "حليب أطفال", "أدوية أساسية", "مواد تعقيم", "خيام", "بطانيات", "حصائر", "أدوات مدرسية", "مواد بناء"]
    for w in warehouses:
        for item_name in random.sample(items, 8):
            db.add(InventoryItem(
                warehouse_id=w.id, name=item_name,
                category=random.choice(["food", "medicine", "shelter", "wash", "nfi", "education"]),
                quantity=random.randint(50, 5000),
                unit=random.choice(["كرتون", "كيس", "عبوة", "قطعة"]),
                min_stock=random.randint(20, 200)
            ))

    # Distributions
    for i in range(20):
        db.add(Distribution(
            project_id=random.randint(1, 3),
            warehouse_id=random.randint(1, 5),
            item_name=random.choice(items),
            quantity=random.randint(100, 2000),
            beneficiaries_count=random.randint(50, 500),
            location=random.choice(GOVERNORATES),
            date=date(2024, random.randint(1, 12), random.randint(1, 28)),
            status=random.choice(["completed", "completed", "planned", "in_progress"]),
            distributed_by="فريق التوزيع"
        ))

    # Cash Transfers
    methods = ["hawala", "mobile_money", "cash_in_hand", "bank"]
    for i in range(30):
        db.add(CashTransfer(
            beneficiary_id=random.randint(1, 100),
            project_id=random.randint(1, 3),
            amount=random.choice([50, 75, 100, 150, 200]),
            currency="USD",
            method=random.choice(methods),
            status=random.choice(["received", "disbursed", "pending", "received", "received"]),
            transfer_date=date(2024, random.randint(1, 12), random.randint(1, 28)),
            reference_number=f"CT-{i+1:04d}",
            agent=f"وكيل {random.randint(1, 10)}",
            verified=random.random() > 0.3
        ))

    # Complaints (CFM)
    channels = ["phone", "box", "whatsapp", "in_person", "sms"]
    categories = ["service_quality", "targeting", "distribution", "staff_behavior", "suggestion"]
    for i in range(25):
        status = random.choice(["received", "under_review", "in_progress", "resolved", "closed", "resolved"])
        db.add(Complaint(
            reference_number=f"CFM-2024-{i+1:04d}",
            channel=random.choice(channels),
            category=random.choice(categories),
            priority=random.choice(["low", "medium", "high", "medium"]),
            status=status,
            description=f"شكوى رقم {i+1} - وصف المشكلة المبلغ عنها",
            complainant_name=f"مقدم الشكوى {i+1}" if random.random() > 0.3 else None,
            complainant_phone=f"77{random.randint(1000000, 9999999)}" if random.random() > 0.4 else None,
            location=random.choice(GOVERNORATES),
            project_id=random.randint(1, 5),
            is_anonymous=random.random() > 0.7,
            is_sensitive=random.random() > 0.85,
            resolution="تم حل المشكلة" if status in ["resolved", "closed"] else None
        ))

    # Field Visits
    for i in range(15):
        db.add(FieldVisit(
            project_id=random.randint(1, 7),
            visit_date=date(2024, random.randint(1, 12), random.randint(1, 28)),
            location=random.choice(GOVERNORATES),
            purpose=random.choice(["متابعة التوزيع", "تقييم الاحتياجات", "مراقبة الجودة", "التحقق من المستفيدين", "تقييم المخاطر"]),
            findings="نتائج الزيارة الميدانية - تم رصد عدة ملاحظات",
            recommendations="توصيات لتحسين الأداء",
            visited_by=f"فريق الزيارة {i+1}",
            status=random.choice(["completed", "planned", "completed"])
        ))

    # Risk Register
    risk_categories = ["أمني", "تشغيلي", "مالي", "سمعة", "بيئي", "صحي"]
    for i in range(12):
        likelihood = random.randint(1, 5)
        impact = random.randint(1, 5)
        score = likelihood * impact
        level = "critical" if score >= 20 else ("high" if score >= 12 else ("medium" if score >= 6 else "low"))
        db.add(RiskRegister(
            title=f"خطر {i+1} - {random.choice(risk_categories)}",
            description=f"وصف الخطر رقم {i+1}",
            category=random.choice(risk_categories),
            likelihood=likelihood, impact=impact, risk_level=level,
            mitigation="إجراءات التخفيف المقترحة",
            owner=f"مسؤول {random.randint(1, 5)}",
            status=random.choice(["open", "open", "mitigated", "closed"]),
            project_id=random.randint(1, 7)
        ))

    # Lessons Learned
    lesson_cats = ["program", "operations", "coordination", "monitoring", "finance"]
    for i in range(10):
        db.add(LessonLearned(
            title=f"درس مستفاد {i+1}",
            description=f"وصف تفصيلي للدرس المستفاد رقم {i+1} من تنفيذ الأنشطة الميدانية",
            category=random.choice(lesson_cats),
            project_id=random.randint(1, 7),
            source=random.choice(["تقييم", "زيارة ميدانية", "تقرير شهري", "اجتماع فريق"]),
            recommendations="التوصيات المرتبطة بهذا الدرس"
        ))

    # MEAL Plans
    for i, proj in enumerate(projects[:5]):
        db.add(MEALPlan(
            project_id=proj.id,
            title=f"خطة MEAL - {proj.name}",
            description=f"خطة المتابعة والتقييم والمساءلة والتعلم لمشروع {proj.name}",
            objectives="قياس التقدم نحو الأهداف، ضمان المساءلة، توثيق التعلم",
            monitoring_approach="جمع بيانات شهري عبر KoBoToolbox، تتبع المؤشرات عبر IPTT، زيارات ميدانية دورية",
            evaluation_approach="تقييم نصف سنوي بمنهجية مختلطة (كمي ونوعي)، تقييم نهائي مستقل",
            accountability_approach="آلية الشكاوى والملاحظات (هاتف، صندوق، واتساب)، اجتماعات مجتمعية ربع سنوية",
            learning_approach="توثيق الدروس المستفادة شهرياً، ورش تبادل خبرات ربع سنوية",
            data_collection_methods="استبيانات، مقابلات، مجموعات بؤرية، مراقبة مباشرة",
            frequency="شهري",
            responsible_staff="مسؤول MEAL + منسق المشروع",
            budget=proj.budget * 0.05,
            status="active"
        ))

    # Activities
    activity_names = ["توزيع مواد إغاثية", "تدريب موظفين", "تقييم احتياجات", "جمع بيانات ميدانية", "عقد ورش عمل", "إعادة تأهيل مرفق", "حملة توعية"]
    for proj in projects[:7]:
        for j in range(4):
            db.add(Activity(
                project_id=proj.id,
                name=f"{random.choice(activity_names)} - {proj.name[:20]}",
                status=random.choice(["completed", "in_progress", "planned", "completed"]),
                progress_percent=random.randint(30, 100),
                planned_start=proj.start_date,
                planned_end=proj.end_date,
                budget=proj.budget * 0.1,
                spent=proj.spent * 0.1,
                responsible_person=f"منسق {j+1}",
                location=proj.governorate
            ))

    # LogFrames
    levels = [("goal", "G1"), ("purpose", "P1"), ("output", "O1"), ("output", "O2"), ("activity", "A1"), ("activity", "A2")]
    for proj in projects[:3]:
        for level, code in levels:
            db.add(LogFrame(
                project_id=proj.id, level=level, code=code,
                description=f"{level} - هدف المشروع على مستوى {level}",
                indicators="مؤشر 1، مؤشر 2",
                means_of_verification="تقارير، استبيانات، زيارات ميدانية",
                assumptions="استمرار الوصول، توفر التمويل"
            ))

    # Data Collection Forms
    forms = [
        DataForm(title="استبيان رضا المستفيدين", description="قياس مستوى رضا المستفيدين عن الخدمات", status="published", project_id=1, created_by="مسؤول MEAL", fields=[
            {"name": "satisfaction", "type": "rating", "label": "مستوى الرضا العام", "required": True},
            {"name": "service_quality", "type": "select", "label": "جودة الخدمة", "options": ["ممتاز", "جيد", "متوسط", "ضعيف"]},
            {"name": "suggestions", "type": "textarea", "label": "اقتراحات للتحسين"},
            {"name": "location", "type": "gps", "label": "الموقع"}
        ]),
        DataForm(title="نموذج تقييم الاحتياجات", description="تقييم احتياجات الأسر المتأثرة", status="published", project_id=2, created_by="مسؤول MEAL", fields=[
            {"name": "household_size", "type": "number", "label": "حجم الأسرة", "required": True},
            {"name": "food_source", "type": "select", "label": "مصدر الغذاء الرئيسي", "options": ["سوق", "مساعدات", "زراعة", "أخرى"]},
            {"name": "water_access", "type": "radio", "label": "الوصول للمياه النظيفة", "options": ["نعم", "لا", "أحياناً"]},
            {"name": "health_needs", "type": "multi_select", "label": "الاحتياجات الصحية", "options": ["أدوية", "تغذية", "رعاية أمومة", "إعاقة"]},
        ]),
        DataForm(title="نموذج متابعة التوزيع", description="توثيق عمليات التوزيع الميداني", status="published", project_id=2, created_by="منسق المشروع", fields=[
            {"name": "distribution_date", "type": "date", "label": "تاريخ التوزيع", "required": True},
            {"name": "items_distributed", "type": "text", "label": "المواد الموزعة"},
            {"name": "beneficiaries_count", "type": "number", "label": "عدد المستفيدين"},
            {"name": "photo", "type": "photo", "label": "صورة التوزيع"},
        ]),
    ]
    db.add_all(forms)
    db.flush()

    # Documents
    doc_categories = ["report", "assessment", "project_proposal", "agreement", "policy"]
    for i in range(15):
        db.add(Document(
            title=f"وثيقة {i+1} - {random.choice(['تقرير شهري', 'تقييم احتياجات', 'مقترح مشروع', 'اتفاقية شراكة', 'سياسة حماية'])}",
            category=random.choice(doc_categories),
            project_id=random.randint(1, 7),
            uploaded_by="مدير النظام",
            tags=",".join(random.sample(["MEAL", "تقرير", "2024", "مانح", "ميداني"], 2)),
            description="وصف الوثيقة"
        ))

    # Notifications
    for user in users[:3]:
        for i in range(5):
            db.add(Notification(
                user_id=user.id,
                title=random.choice(["تنبيه مخزون منخفض", "تقرير جديد", "شكوى جديدة", "زيارة ميدانية قادمة", "موعد تقرير مانح"]),
                message="تفاصيل الإشعار",
                notification_type=random.choice(["alert", "info", "warning"]),
                is_read=random.random() > 0.5
            ))

    db.commit()
