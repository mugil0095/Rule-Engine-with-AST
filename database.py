from pymongo import MongoClient

# MongoDB connection (replace with your actual connection string)
client = MongoClient("mongodb://localhost:27017/")
db = client["rule_engine_db"]
rules_collection = db["rules"]

def store_rule(rule_string, ast_json):
    rule_id = rules_collection.count_documents({}) + 1  # Auto-generate rule ID
    rules_collection.insert_one({
        "rule_id": rule_id,
        "rule_string": rule_string,
        "ast": ast_json
    })

def get_all_rules():
    return list(rules_collection.find({}, {"_id": 0}))  # Retrieve all rules without MongoDB "_id" field
