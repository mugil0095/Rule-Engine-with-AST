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
        """ Converts the AST Node into a dictionary for JSON serialization """
        if self.type == 'operator':
            return {
                'type': 'operator',
                'left': self.left.to_dict() if self.left else None,
                'right': self.right.to_dict() if self.right else None,
                'value': self.value
            }
        return {'type': 'operand', 'value': self.value}

def create_rule(rule_string):
    """ Creates a rule and returns the root node of the AST """
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
    """ Evaluates a rule (AST) based on the input data """
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
    """ Combines a list of AST nodes into a single AND node """
    if not rules:
        return None  # No rules to combine

    # Start with the first rule
    combined = rules[0]
    for rule in rules[1:]:
        combined = Node(
            type='operator',
            value='AND',
            left=combined,
            right=rule
        )
    return combined