import unittest
from models import Node, create_rule, evaluate_rule, combine_rules

class TestRuleEngine(unittest.TestCase):

    def test_create_rule_and_ast_structure(self):
        rule_string = "age > 30 AND salary > 50000"
        ast = create_rule(rule_string)
        
        # Test root node
        self.assertEqual(ast.type, 'operator')
        self.assertEqual(ast.value, 'AND')
        
        # Test left operand
        self.assertEqual(ast.left.type, 'operand')
        self.assertEqual(ast.left.value, 'age > 30')
        
        # Test right operand
        self.assertEqual(ast.right.type, 'operand')
        self.assertEqual(ast.right.value, 'salary > 50000')
    
    def test_evaluate_rule(self):
        rule_string = "age > 30 AND salary > 50000"
        ast = create_rule(rule_string)
        
        # Test evaluation with matching data
        data = {"age": 35, "salary": 60000}
        result = evaluate_rule(ast, data)
        self.assertTrue(result)
        
        # Test evaluation with non-matching data
        data = {"age": 25, "salary": 60000}
        result = evaluate_rule(ast, data)
        self.assertFalse(result)
    
    def test_combine_rules(self):
        rule1 = create_rule("age > 30 AND salary > 50000")
        rule2 = create_rule("experience > 5 OR department == 'Sales'")
        combined_ast = combine_rules([rule1, rule2])
        
        # Test combined AST structure
        self.assertEqual(combined_ast.type, 'operator')
        self.assertEqual(combined_ast.value, 'AND')
    
    def test_evaluate_combined_rule(self):
        rule1 = create_rule("age > 30 AND salary > 50000")
        rule2 = create_rule("experience > 5 OR department == 'Sales'")
        combined_ast = combine_rules([rule1, rule2])
        
        # Test evaluation with matching data
        data = {"age": 35, "salary": 60000, "experience": 6, "department": "Sales"}
        result = evaluate_rule(combined_ast, data)
        self.assertTrue(result)
        
        # Test evaluation with non-matching data
        data = {"age": 25, "salary": 40000, "experience": 3, "department": "HR"}
        result = evaluate_rule(combined_ast, data)
        self.assertFalse(result)

if __name__ == '__main__':
    unittest.main()
