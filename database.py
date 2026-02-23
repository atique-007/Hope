from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
import os

# MongoDB connection
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
DB_NAME = "college_chatbot"
COLLECTION_FAQS = "faqs"
COLLECTION_PROGRAMS = "programs"

try:
    client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
    # Verify connection
    client.admin.command('ping')
    db = client[DB_NAME]
    print("✓ Connected to MongoDB")
except ConnectionFailure:
    print("✗ Failed to connect to MongoDB. Make sure MongoDB is running.")
    client = None
    db = None


def get_faqs():
    """Fetch all FAQs from database"""
    if db is None:
        return []
    try:
        faqs_collection = db[COLLECTION_FAQS]
        faqs = list(faqs_collection.find({}, {"_id": 0}))
        return faqs
    except Exception as e:
        print(f"Error fetching FAQs: {e}")
        return []


def get_programs():
    """Fetch all programs from database"""
    if db is None:
        return []
    try:
        programs_collection = db[COLLECTION_PROGRAMS]
        programs = list(programs_collection.find({}, {"_id": 0}))
        return programs
    except Exception as e:
        print(f"Error fetching programs: {e}")
        return []


def add_faq(question):
    """Add a new FAQ to database"""
    if not db:
        return False
    try:
        faqs_collection = db[COLLECTION_FAQS]
        faqs_collection.insert_one({"q": question})
        return True
    except Exception as e:
        print(f"Error adding FAQ: {e}")
        return False


def add_program(name, category, duration, eligibility, fees, seats):
    """Add a new program to database"""
    if db is None:
        return False
    try:
        programs_collection = db[COLLECTION_PROGRAMS]
        programs_collection.insert_one({
            "name": name,
            "category": category,  # "Undergraduate" or "Postgraduate"
            "duration": duration,
            "eligibility": eligibility,
            "fees": fees,
            "seats": seats
        })
        return True
    except Exception as e:
        print(f"Error adding program: {e}")
        return False


def initialize_database():
    """Initialize database with sample data if empty"""
    if db is None:
        return False
    
    try:
        faqs_collection = db[COLLECTION_FAQS]
        programs_collection = db[COLLECTION_PROGRAMS]
        
        # Initialize FAQs if empty
        if faqs_collection.count_documents({}) == 0:
            sample_faqs = [
                {"q": "What programs are offered?"},
                {"q": "What are the admission requirements?"},
                {"q": "What is the application deadline?"},
                {"q": "What are the tuition fees?"},
                {"q": "How can I contact admissions?"},
                {"q": "Is financial aid available?"},
                {"q": "What are the hostel facilities?"},
                {"q": "What is the campus placement record?"},
                {"q": "Are there any scholarship programs?"},
                {"q": "What are the required entrance exams?"},
                {"q": "What is the course duration?"},
                {"q": "Can international students apply?"},
            ]
            faqs_collection.insert_many(sample_faqs)
            print(f"✓ Initialized {len(sample_faqs)} FAQs")
        
        # Initialize programs if empty
        if programs_collection.count_documents({}) == 0:
            sample_programs = [
                {
                    "name": "Bachelor's of Computer Applications",
                    "category": "Undergraduate",
                    "duration": "3 Years",
                    "eligibility": "10+2 with Mathematics",
                    "fees": "₹45,000 per year",
                    "seats": "60"
                },
                {
                    "name": "Bachelor's of Commerce",
                    "category": "Undergraduate",
                    "duration": "3 Years",
                    "eligibility": "10+2 in any stream",
                    "fees": "₹35,000 per year",
                    "seats": "80"
                },
                {
                    "name": "Bachelor's of Business Administration",
                    "category": "Undergraduate",
                    "duration": "3 Years",
                    "eligibility": "10+2 in any stream",
                    "fees": "₹50,000 per year",
                    "seats": "60"
                },
                {
                    "name": "Bachelor's of BA-Aviation Management",
                    "category": "Undergraduate",
                    "duration": "3 Years",
                    "eligibility": "10+2 in any stream",
                    "fees": "₹65,000 per year",
                    "seats": "40"
                },
                {
                    "name": "Master's in Computer Applications",
                    "category": "Postgraduate",
                    "duration": "2 Years",
                    "eligibility": "Bachelor's degree with Mathematics",
                    "fees": "₹55,000 per year",
                    "seats": "40"
                },
                {
                    "name": "Master's in Commerce",
                    "category": "Postgraduate",
                    "duration": "2 Years",
                    "eligibility": "Bachelor's in Commerce",
                    "fees": "₹40,000 per year",
                    "seats": "50"
                },
                {
                    "name": "Master's in Business Administrations",
                    "category": "Postgraduate",
                    "duration": "2 Years",
                    "eligibility": "Bachelor's degree in any discipline",
                    "fees": "₹75,000 per year",
                    "seats": "50"
                }
            ]
            programs_collection.insert_many(sample_programs)
            print(f"✓ Initialized {len(sample_programs)} programs")
        
        return True
    except Exception as e:
        print(f"Error initializing database: {e}")
        return False
