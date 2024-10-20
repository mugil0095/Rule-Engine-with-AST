import streamlit as st
from api import create_rule, evaluate_rule, combine_rules

# Streamlit app layout
st.title('Rule Engine Dashboard')

rule_string = st.text_area('Enter Rule String:', placeholder="Enter your rule here...")

if st.button('Create Rule'):
    try:
        ast_root = create_rule(rule_string)
        example_data = {"age": 35, "department": "Sales", "salary": 60000, "experience": 3}
        result = evaluate_rule(ast_root, example_data)

        # Combine rules (Example: combining the same rule twice for demonstration)
        combined_ast = combine_rules([ast_root, ast_root])

        def ast_to_dict(node):
            if node.type == 'operator':
                return {
                    'type': 'operator',
                    'left': ast_to_dict(node.left),
                    'right': ast_to_dict(node.right),
                    'value': node.value
                }
            return {'type': 'operand', 'value': node.value}

        combined_ast_dict = ast_to_dict(combined_ast)

        st.write('### Rule Abstract Syntax Tree (AST):')
        st.json(ast_to_dict(ast_root))

        st.write('### Evaluation Result:')
        st.write(result)

        st.write('### Combined Rule AST:')
        st.json(combined_ast_dict)

    except Exception as e:
        st.error(f"Error: {str(e)}")
