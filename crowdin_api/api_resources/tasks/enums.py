from enum import Enum


class TaskOperationPatchPath(Enum):
    STATUS = "/status"
    TITLE = "/title"
    DESCRIPTION = "/description"
    DEADLINE = "/deadline"
    SPLIT_FILES = "/splitFiles"
    FILE_IDS = "/fileIds"
    ASSIGNEES = "/assignees"
    DATE_FROM = "/dateFrom"
    DATE_TO = "/dateTo"
    LABEL_IDS = "/labelIds"


class VendorTaskOperationPatchPath(Enum):
    title = "/title"
    description = "/description"
    status = "/status"


class CrowdinTaskType(Enum):
    TRANSLATE = 0
    PROOFREAD = 1
    TRANSLATE_BY_VENDOR = 2
    PROOFREAD_BY_VENDOR = 3


class CrowdinGeneralTaskType(Enum):
    TRANSLATE = 0
    PROOFREAD = 1


class CrowdinTaskStatus(Enum):
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    DONE = "done"
    CLOSED = "closed"


# Oht
class OhtCrowdinTaskType(Enum):
    TRANSLATE_BY_VENDOR = 2
    PROOFREAD_BY_VENDOR = 3


class OhtCrowdinTaskExpertise(Enum):
    STANDARD = "standard"
    MOBILE_APPLICATIONS = "mobile-applications"
    SOFTWARE_IT = "software-it"
    GAMING_VIDEO_GAMES = "gaming-video-games"
    TECHNICAL_ENGINEERING = "technical-engineering"
    MARKETING_CONSUMER_MEDIA = "marketing-consumer-media"
    BUSINESS_FINANCE = "business-finance"
    LEGAL_CERTIFICATE = "legal-certificate"
    CV = "cv"
    MEDICAL = "medical"
    PATENTS = "patents"
    AD_WORDS_BANNERS = "ad-words-banners"
    AUTOMOTIVE_AEROSPACE = "automotive-aerospace"
    SCIENTIFIC = "scientific"
    SCIENTIFIC_ACADEMIC = "scientific-academic"
    TOURISM = "tourism"
    CERTIFICATES_TRANSLATION = "certificates-translation"
    TRAINING_EMPLOYEE_HANDBOOKS = "training-employee-handbooks"
    FOREX_CRYPTO = "forex-crypto"


# Gengo
class GengoCrowdinTaskType(Enum):
    TRANSLATE_BY_VENDOR = 2


class GengoCrowdinTaskExpertise(Enum):
    STANDARD = "standard"
    PRO = "pro"


class GengoCrowdinTaskTone(Enum):
    EMPTY = ""
    INFORMAL = "Informal"
    FRIENDLY = "Friendly"
    BUSINESS = "Business"
    FORMAL = "Formal"
    OTHER = "other"


class GengoCrowdinTaskPurpose(Enum):
    STANDARD = "standard"
    PERSONAL_USE = "Personal use"
    BUSINESS = "Business"
    ONLINE_CONTENT = "Online content"
    APP_OR_WEB_LOCALIZATION = "App/Web localization"
    MEDIA_CONTENT = "Media content"
    SEMI_TECHNICAL = "Semi-technical"
    OTHER = "other"


# Translated
class TranslatedCrowdinTaskType(Enum):
    TRANSLATE_BY_VENDOR = 2


class TranslatedCrowdinTaskExpertise(Enum):
    ECONOMY = "P"
    PROFESSIONAL = "T"
    PREMIUM = "R"


class TranslatedCrowdinTaskSubjects(Enum):
    GENERAL = "general"
    ACCOUNTING_FINANCE = "accounting_finance"
    AEROSPACE_DEFENCE = "aerospace_defence"
    ARCHITECTURE = "architecture"
    ART = "art"
    AUTOMOTIVE = "automotive"
    CERTIFICATES_DIPLOMAS_LICENCES_CV_ETC = "certificates_diplomas_licences_cv_etc"
    CHEMICAL = "chemical"
    CIVIL_ENGINEERING_CONSTRUCTION = "civil_engineering_construction"
    CORPORATE_SOCIAL_RESPONSIBILITY = "corporate_social_responsibility"
    COSMETICS = "cosmetics"
    CULINARY = "culinary"
    ELECTRONICS_ELECTRICAL_ENGINEERING = "electronics_electrical_engineering"
    ENERGY_POWER_GENERATION_OIL_GAS = "energy_power_generation_oil_gas"
    ENVIRONMENT = "environment"
    FASHION = "fashion"
    GAMES_VISEOGAMES_CASINO = "games_viseogames_casino"
    GENERAL_BUSINESS_COMMERCE = "general_business_commerce"
    HISTORY_ARCHAEOLOGY = "history_archaeology"
    INFORMATION_TECHNOLOGY = "information_technology"
    INSURANCE = "insurance"
    INTERNET_ECOMMERCE = "internet_e-commerce"
    LEGAL_DOCUMENTS_CONTRACTS = "legal_documents_contracts"
    LITERARY_TRANSLATIONS = "literary_translations"
    MARKETING_ADVERTISING_MATERIAL_PUBLIC_RELATIONS = (
        "marketing_advertising_material_public_relations"
    )
    MATEMATICS_AND_PHYSICS = "matematics_and_physics"
    MECHANICAL_MANUFACTURING = "mechanical_manufacturing"
    MEDIA_JOURNALISM_PUBLISHING = "media_journalism_publishing"
    MEDICAL_PHARMACEUTICAL = "medical_pharmaceutical"
    MUSIC = "music"
    PRIVATE_CORRESPONDENCE_LETTERS = "private_correspondence_letters"
    RELIGION = "religion"
    SCIENCE = "science"
    SHIPPING_SAILING_MARITIME = "shipping_sailing_maritime"
    SOCIAL_SCIENCE = "social_science"
    TELECOMMUNICATIONS = "telecommunications"
    TRAVEL_TOURISM = "travel_tourism"
