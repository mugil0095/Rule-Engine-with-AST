from flask import Flask, request, jsonify
from api import create_rule, evaluate_rule, combine_rules
from pymongo import MongoClient

app = Flask(__name__)

# MongoDB connection
client = MongoClient("mongodb://localhost:27017/")
db = client["rule_engine_db"]
rules_collection = db["rules"]

# Endpoint to create a rule
@app.route('/create_rule/', methods=['POST'])
def create_rule_endpoint():
    data = request.get_json()
    rule_string = data.get('rule')
    try:
        ast_root = create_rule(rule_string)
        ast_json = ast_root.to_dict()
        return jsonify({'success': True, 'ast': ast_json}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Endpoint to evaluate a rule
@app.route('/evaluate_rule/', methods=['POST'])
def evaluate_rule_endpoint():
    data = request.get_json()
    rule_string = data.get('rule_string')
    user_data = data.get('user_data')
    try:
        ast_root = create_rule(rule_string)
        result = evaluate_rule(ast_root, user_data)
        return jsonify({'success': True, 'result': result}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Endpoint to combine rules
@app.route('/combine_rules/', methods=['POST'])
def combine_rules_endpoint():
    data = request.get_json()
    rule_strings = data.get('rule_strings')
    try:
        ast_roots = [create_rule(rule) for rule in rule_strings]
        combined_ast = combine_rules(ast_roots)
        combined_ast_json = combined_ast.to_dict()
        return jsonify({'success': True, 'combined_ast': combined_ast_json}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(port=8000, debug=True)
