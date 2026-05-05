from sqlalchemy import (
    Column, Integer, String, Float, Boolean, DateTime, Date, Text,
    ForeignKey, JSON
)
from sqlalchemy.orm import relationship
from datetime import datetime, date
from app.database import Base
import enum


# ==================== ENUMS ====================

class UserRole(str, enum.Enum):
    ADMIN = "admin"
    MANAGER = "manager"
    MEAL_OFFICER = "meal_officer"
    FIELD_OFFICER = "field_officer"
    FINANCE = "finance"
    HR = "hr"
    VIEWER = "viewer"


class Gender(str, enum.Enum):
    MALE = "male"
    FEMALE = "female"


class BeneficiaryStatus(str, enum.Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    SUSPENDED = "suspended"
    GRADUATED = "graduated"


class ProjectStatus(str, enum.Enum):
    PLANNED = "planned"
    ACTIVE = "active"
    COMPLETED = "completed"
    SUSPENDED = "suspended"
    CANCELLED = "cancelled"


class TransactionType(str, enum.Enum):
    INCOME = "income"
    EXPENSE = "expense"
    TRANSFER = "transfer"


class GrantStatus(str, enum.Enum):
    PENDING = "pending"
    APPROVED = "approved"
    ACTIVE = "active"
    COMPLETED = "completed"
    REJECTED = "rejected"


class EmployeeStatus(str, enum.Enum):
    ACTIVE = "active"
    ON_LEAVE = "on_leave"
    TERMINATED = "terminated"
    RESIGNED = "resigned"


class LeaveType(str, enum.Enum):
    ANNUAL = "annual"
    SICK = "sick"
    MATERNITY = "maternity"
    EMERGENCY = "emergency"
    UNPAID = "unpaid"


class LeaveStatus(str, enum.Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"


class ItemCategory(str, enum.Enum):
    FOOD = "food"
    MEDICINE = "medicine"
    SHELTER = "shelter"
    WASH = "wash"
    NFI = "nfi"
    EDUCATION = "education"
    OTHER = "other"


class DistributionStatus(str, enum.Enum):
    PLANNED = "planned"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class CashTransferStatus(str, enum.Enum):
    PENDING = "pending"
    APPROVED = "approved"
    DISBURSED = "disbursed"
    RECEIVED = "received"
    FAILED = "failed"


class CashTransferMethod(str, enum.Enum):
    BANK = "bank"
    MOBILE_MONEY = "mobile_money"
    HAWALA = "hawala"
    CASH_IN_HAND = "cash_in_hand"
    VOUCHER = "voucher"


class IndicatorType(str, enum.Enum):
    OUTPUT = "output"
    OUTCOME = "outcome"
    IMPACT = "impact"


class FormStatus(str, enum.Enum):
    DRAFT = "draft"
    PUBLISHED = "published"
    CLOSED = "closed"
    ARCHIVED = "archived"


class FieldType(str, enum.Enum):
    TEXT = "text"
    NUMBER = "number"
    SELECT = "select"
    MULTI_SELECT = "multi_select"
    DATE = "date"
    DATETIME = "datetime"
    TEXTAREA = "textarea"
    RADIO = "radio"
    CHECKBOX = "checkbox"
    FILE = "file"
    GPS = "gps"
    PHOTO = "photo"
    RATING = "rating"
    MATRIX = "matrix"
    SECTION = "section"


class SubmissionStatus(str, enum.Enum):
    DRAFT = "draft"
    SUBMITTED = "submitted"
    VALIDATED = "validated"
    REJECTED = "rejected"


class DocumentCategory(str, enum.Enum):
    PROJECT_PROPOSAL = "project_proposal"
    REPORT = "report"
    ASSESSMENT = "assessment"
    AGREEMENT = "agreement"
    BUDGET = "budget"
    MEETING_MINUTES = "meeting_minutes"
    POLICY = "policy"
    PHOTO = "photo"
    MAP = "map"
    OTHER = "other"


class ComplaintChannel(str, enum.Enum):
    PHONE = "phone"
    BOX = "box"
    EMAIL = "email"
    IN_PERSON = "in_person"
    SMS = "sms"
    WHATSAPP = "whatsapp"
    WEBSITE = "website"
    OTHER = "other"


class ComplaintStatus(str, enum.Enum):
    RECEIVED = "received"
    UNDER_REVIEW = "under_review"
    IN_PROGRESS = "in_progress"
    REFERRED = "referred"
    RESOLVED = "resolved"
    CLOSED = "closed"
    ESCALATED = "escalated"


class ComplaintPriority(str, enum.Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class ComplaintCategory(str, enum.Enum):
    SERVICE_QUALITY = "service_quality"
    STAFF_BEHAVIOR = "staff_behavior"
    TARGETING = "targeting"
    DISTRIBUTION = "distribution"
    PROTECTION = "protection"
    SAFEGUARDING = "safeguarding"
    FRAUD = "fraud"
    SUGGESTION = "suggestion"
    APPRECIATION = "appreciation"
    OTHER = "other"


class RiskLevel(str, enum.Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class Currency(str, enum.Enum):
    YER = "YER"
    USD = "USD"
    SAR = "SAR"
    EUR = "EUR"


# ==================== MODELS ====================

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True)
    full_name = Column(String(100), nullable=False)
    hashed_password = Column(String(200), nullable=False)
    role = Column(String(20), default=UserRole.VIEWER)
    department = Column(String(50))
    is_active = Column(Boolean, default=True)
    last_login = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    preferred_language = Column(String(5), default="ar")


class Beneficiary(Base):
    __tablename__ = "beneficiaries"
    id = Column(Integer, primary_key=True, index=True)
    national_id = Column(String(20), unique=True, index=True)
    full_name = Column(String(100), nullable=False)
    gender = Column(String(10))
    date_of_birth = Column(Date)
    phone = Column(String(20))
    governorate = Column(String(50), nullable=False)
    district = Column(String(50))
    village = Column(String(100))
    household_size = Column(Integer, default=1)
    vulnerability_score = Column(Float, default=0.0)
    status = Column(String(20), default=BeneficiaryStatus.ACTIVE)
    registration_date = Column(Date, default=date.today)
    latitude = Column(Float)
    longitude = Column(Float)
    notes = Column(Text)
    is_idp = Column(Boolean, default=False)
    disability = Column(Boolean, default=False)
    female_headed = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Project(Base):
    __tablename__ = "projects"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    code = Column(String(20), unique=True, index=True)
    description = Column(Text)
    sector = Column(String(50))
    status = Column(String(20), default=ProjectStatus.ACTIVE)
    start_date = Column(Date)
    end_date = Column(Date)
    budget = Column(Float, default=0)
    spent = Column(Float, default=0)
    currency = Column(String(5), default=Currency.USD)
    governorate = Column(String(50))
    donor = Column(String(100))
    target_beneficiaries = Column(Integer, default=0)
    reached_beneficiaries = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    indicators = relationship("Indicator", back_populates="project")
    activities = relationship("Activity", back_populates="project")


class Activity(Base):
    __tablename__ = "activities"
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"))
    name = Column(String(200), nullable=False)
    description = Column(Text)
    planned_start = Column(Date)
    planned_end = Column(Date)
    actual_start = Column(Date)
    actual_end = Column(Date)
    status = Column(String(20), default="planned")
    progress_percent = Column(Float, default=0)
    budget = Column(Float, default=0)
    spent = Column(Float, default=0)
    responsible_person = Column(String(100))
    location = Column(String(100))
    created_at = Column(DateTime, default=datetime.utcnow)
    project = relationship("Project", back_populates="activities")


class Indicator(Base):
    __tablename__ = "indicators"
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"))
    name = Column(String(200), nullable=False)
    description = Column(Text)
    indicator_type = Column(String(20), default=IndicatorType.OUTPUT)
    unit = Column(String(50))
    baseline = Column(Float, default=0)
    target = Column(Float, default=0)
    current_value = Column(Float, default=0)
    data_source = Column(String(100))
    frequency = Column(String(20), default="monthly")
    responsible = Column(String(100))
    sector = Column(String(50))
    disaggregation = Column(String(100))
    created_at = Column(DateTime, default=datetime.utcnow)
    project = relationship("Project", back_populates="indicators")
    measurements = relationship("Measurement", back_populates="indicator")


class Measurement(Base):
    __tablename__ = "measurements"
    id = Column(Integer, primary_key=True, index=True)
    indicator_id = Column(Integer, ForeignKey("indicators.id"))
    value = Column(Float, nullable=False)
    date = Column(Date, nullable=False)
    notes = Column(Text)
    collected_by = Column(String(100))
    verified = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    indicator = relationship("Indicator", back_populates="measurements")


class Grant(Base):
    __tablename__ = "grants"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    donor = Column(String(100), nullable=False)
    amount = Column(Float, nullable=False)
    currency = Column(String(5), default=Currency.USD)
    start_date = Column(Date)
    end_date = Column(Date)
    status = Column(String(20), default=GrantStatus.ACTIVE)
    spent = Column(Float, default=0)
    description = Column(Text)
    reporting_frequency = Column(String(20), default="quarterly")
    created_at = Column(DateTime, default=datetime.utcnow)


class Transaction(Base):
    __tablename__ = "transactions"
    id = Column(Integer, primary_key=True, index=True)
    grant_id = Column(Integer, ForeignKey("grants.id"))
    transaction_type = Column(String(20), nullable=False)
    amount = Column(Float, nullable=False)
    currency = Column(String(5), default=Currency.USD)
    description = Column(String(200))
    category = Column(String(50))
    date = Column(Date, nullable=False)
    reference_number = Column(String(50))
    approved_by = Column(String(100))
    created_at = Column(DateTime, default=datetime.utcnow)


class Employee(Base):
    __tablename__ = "employees"
    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(String(20), unique=True, index=True)
    full_name = Column(String(100), nullable=False)
    email = Column(String(100))
    phone = Column(String(20))
    department = Column(String(50))
    position = Column(String(100))
    status = Column(String(20), default=EmployeeStatus.ACTIVE)
    join_date = Column(Date)
    salary = Column(Float)
    contract_type = Column(String(20))
    location = Column(String(50))
    supervisor = Column(String(100))
    created_at = Column(DateTime, default=datetime.utcnow)


class LeaveRequest(Base):
    __tablename__ = "leave_requests"
    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employees.id"))
    leave_type = Column(String(20), nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    reason = Column(Text)
    status = Column(String(20), default=LeaveStatus.PENDING)
    approved_by = Column(String(100))
    created_at = Column(DateTime, default=datetime.utcnow)


class Warehouse(Base):
    __tablename__ = "warehouses"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    location = Column(String(100))
    governorate = Column(String(50))
    capacity = Column(Float)
    manager = Column(String(100))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)


class InventoryItem(Base):
    __tablename__ = "inventory_items"
    id = Column(Integer, primary_key=True, index=True)
    warehouse_id = Column(Integer, ForeignKey("warehouses.id"))
    name = Column(String(200), nullable=False)
    category = Column(String(20), default=ItemCategory.OTHER)
    quantity = Column(Float, default=0)
    unit = Column(String(20))
    min_stock = Column(Float, default=0)
    expiry_date = Column(Date)
    batch_number = Column(String(50))
    created_at = Column(DateTime, default=datetime.utcnow)


class Distribution(Base):
    __tablename__ = "distributions"
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"))
    warehouse_id = Column(Integer, ForeignKey("warehouses.id"))
    item_name = Column(String(200))
    quantity = Column(Float)
    beneficiaries_count = Column(Integer, default=0)
    location = Column(String(100))
    date = Column(Date)
    status = Column(String(20), default=DistributionStatus.PLANNED)
    distributed_by = Column(String(100))
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)


class CashTransfer(Base):
    __tablename__ = "cash_transfers"
    id = Column(Integer, primary_key=True, index=True)
    beneficiary_id = Column(Integer, ForeignKey("beneficiaries.id"))
    project_id = Column(Integer, ForeignKey("projects.id"))
    amount = Column(Float, nullable=False)
    currency = Column(String(5), default=Currency.USD)
    method = Column(String(20), default=CashTransferMethod.HAWALA)
    status = Column(String(20), default=CashTransferStatus.PENDING)
    transfer_date = Column(Date)
    reference_number = Column(String(50))
    agent = Column(String(100))
    notes = Column(Text)
    verified = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)


class DataForm(Base):
    __tablename__ = "data_forms"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    description = Column(Text)
    status = Column(String(20), default=FormStatus.DRAFT)
    project_id = Column(Integer, ForeignKey("projects.id"))
    fields = Column(JSON)
    created_by = Column(String(100))
    created_at = Column(DateTime, default=datetime.utcnow)
    submissions = relationship("FormSubmission", back_populates="form")


class FormSubmission(Base):
    __tablename__ = "form_submissions"
    id = Column(Integer, primary_key=True, index=True)
    form_id = Column(Integer, ForeignKey("data_forms.id"))
    data = Column(JSON)
    status = Column(String(20), default=SubmissionStatus.SUBMITTED)
    submitted_by = Column(String(100))
    location_lat = Column(Float)
    location_lng = Column(Float)
    submitted_at = Column(DateTime, default=datetime.utcnow)
    synced = Column(Boolean, default=True)
    form = relationship("DataForm", back_populates="submissions")


class Complaint(Base):
    __tablename__ = "complaints"
    id = Column(Integer, primary_key=True, index=True)
    reference_number = Column(String(20), unique=True)
    channel = Column(String(20), default=ComplaintChannel.PHONE)
    category = Column(String(30), default=ComplaintCategory.OTHER)
    priority = Column(String(10), default=ComplaintPriority.MEDIUM)
    status = Column(String(20), default=ComplaintStatus.RECEIVED)
    description = Column(Text, nullable=False)
    complainant_name = Column(String(100))
    complainant_phone = Column(String(20))
    complainant_gender = Column(String(10))
    location = Column(String(100))
    project_id = Column(Integer, ForeignKey("projects.id"))
    assigned_to = Column(String(100))
    resolution = Column(Text)
    response_date = Column(DateTime)
    is_anonymous = Column(Boolean, default=False)
    is_sensitive = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    closed_at = Column(DateTime)


class LogFrame(Base):
    __tablename__ = "logframes"
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"))
    level = Column(String(20))
    code = Column(String(20))
    description = Column(Text, nullable=False)
    indicators = Column(Text)
    means_of_verification = Column(Text)
    assumptions = Column(Text)
    parent_id = Column(Integer, ForeignKey("logframes.id"))
    created_at = Column(DateTime, default=datetime.utcnow)


class FieldVisit(Base):
    __tablename__ = "field_visits"
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"))
    visit_date = Column(Date, nullable=False)
    location = Column(String(100))
    purpose = Column(String(200))
    findings = Column(Text)
    recommendations = Column(Text)
    follow_up_actions = Column(Text)
    visited_by = Column(String(100))
    status = Column(String(20), default="planned")
    photos_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)


class RiskRegister(Base):
    __tablename__ = "risk_register"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    description = Column(Text)
    category = Column(String(50))
    likelihood = Column(Integer, default=3)
    impact = Column(Integer, default=3)
    risk_level = Column(String(10))
    mitigation = Column(Text)
    owner = Column(String(100))
    status = Column(String(20), default="open")
    project_id = Column(Integer, ForeignKey("projects.id"))
    review_date = Column(Date)
    created_at = Column(DateTime, default=datetime.utcnow)


class LessonLearned(Base):
    __tablename__ = "lessons_learned"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=False)
    category = Column(String(50))
    project_id = Column(Integer, ForeignKey("projects.id"))
    source = Column(String(100))
    recommendations = Column(Text)
    shared_with = Column(String(200))
    date = Column(Date, default=date.today)
    created_at = Column(DateTime, default=datetime.utcnow)


class MEALPlan(Base):
    __tablename__ = "meal_plans"
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"))
    title = Column(String(200), nullable=False)
    description = Column(Text)
    objectives = Column(Text)
    monitoring_approach = Column(Text)
    evaluation_approach = Column(Text)
    accountability_approach = Column(Text)
    learning_approach = Column(Text)
    data_collection_methods = Column(Text)
    frequency = Column(String(50))
    responsible_staff = Column(String(200))
    budget = Column(Float, default=0)
    status = Column(String(20), default="draft")
    created_at = Column(DateTime, default=datetime.utcnow)


class Document(Base):
    __tablename__ = "documents"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    category = Column(String(30), default=DocumentCategory.OTHER)
    file_path = Column(String(500))
    file_size = Column(Integer)
    project_id = Column(Integer, ForeignKey("projects.id"))
    uploaded_by = Column(String(100))
    tags = Column(String(500))
    description = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)


class AuditLog(Base):
    __tablename__ = "audit_logs"
    id = Column(Integer, primary_key=True, index=True)
    user = Column(String(100))
    action = Column(String(50), nullable=False)
    resource = Column(String(50))
    resource_id = Column(Integer)
    details = Column(Text)
    ip_address = Column(String(45))
    timestamp = Column(DateTime, default=datetime.utcnow)


class Notification(Base):
    __tablename__ = "notifications"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    title = Column(String(200), nullable=False)
    message = Column(Text)
    notification_type = Column(String(30))
    is_read = Column(Boolean, default=False)
    link = Column(String(200))
    created_at = Column(DateTime, default=datetime.utcnow)


class OfflineQueue(Base):
    __tablename__ = "offline_queue"
    id = Column(Integer, primary_key=True, index=True)
    device_id = Column(String(100))
    action = Column(String(50))
    resource_type = Column(String(50))
    data = Column(JSON)
    synced = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    synced_at = Column(DateTime)
