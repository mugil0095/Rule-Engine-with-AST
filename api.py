class Node:
    def __init__(self, type, left=None, right=None, value=None):
        self.type = type
        self.left = left
        self.right = right
        self.value = value

    def __repr__(self):
        if self.type == 'operator':
            return f"Operator({self.value}, {self.left}, {self.right})"
        return f"Operand({self.value})"
    
    def to_dict(self):
        if self.type == 'operator':
            return {
                'type': 'operator',
                'left': self.left.to_dict() if self.left else None,
                'right': self.right.to_dict() if self.right else None,
                'value': self.value
            }
        return {'type': 'operand', 'value': self.value}

def create_rule(rule_string):
    # Example rule creation for demonstration
    if 'AND' in rule_string:
        return Node('operator', 
                    Node('operand', value='age > 30'), 
                    Node('operand', value='salary > 50000'), 
                    value='AND')
    return Node('operator', 
                Node('operand', value='age < 40'), 
                Node('operand', value='salary > 30000'), 
                value='OR')

def evaluate_rule(ast_node, data):
    if ast_node.type == 'operand':
        left, operator, right = ast_node.value.split()
        left_value = data.get(left, 0)
        if operator == '==':
            return left_value == float(right)
        elif operator == '>':
            return float(left_value) > float(right)
        elif operator == '<':
            return float(left_value) < float(right)
    elif ast_node.type == 'operator':
        left_result = evaluate_rule(ast_node.left, data)
        right_result = evaluate_rule(ast_node.right, data)
        if ast_node.value == 'AND':
            return left_result and right_result
        elif ast_node.value == 'OR':
            return left_result or right_result
    return False

def combine_rules(rules):
    def merge_ast(ast1, ast2):
        if ast1 == ast2:
            return ast1
        if ast1 is None:
            return ast2
        if ast2 is None:
            return ast1
        if ast1.type == 'operand' and ast2.type == 'operand':
            if ast1.value == ast2.value:
                return ast1
        if ast1.type == 'operator' and ast2.type == 'operator':
            if ast1.value == 'AND' and ast2.value == 'AND':
                left = merge_ast(ast1.left, ast2.left)
                right = merge_ast(ast1.right, ast2.right)
                return Node('operator', left=left, right=right, value='AND')
            elif ast1.value == 'OR' and ast2.value == 'OR':
                left = merge_ast(ast1.left, ast2.left)
                right = merge_ast(ast1.right, ast2.right)
                return Node('operator', left=left, right=right, value='OR')
        return Node('operator', left=ast1, right=ast2, value='AND')

    if not rules:
        return None
    
    combined_ast = rules[0]
    for rule in rules[1:]:
        combined_ast = merge_ast(combined_ast, rule)
    
    return combined_ast
