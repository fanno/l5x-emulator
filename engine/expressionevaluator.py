import operator
import re
from typing import Any, Dict, Callable

class ExpressionEvaluator:

    OPERATORS = {
        '+': operator.add,
        '-': operator.sub,
        '*': operator.mul,
        '/': operator.truediv,
        'MOD': lambda a, b: a % b,
        'AND': operator.and_,
        'OR': operator.or_,
        'XOR': operator.xor,
        '<': operator.lt,
        '>': operator.gt,
        '<=': operator.le,
        '>=': operator.ge,
        '=': operator.eq,
        '<>': operator.ne,
        '**': operator.pow,
    }
    '''
    1 ( )
    2 ABS, ACS, ASN, ATN, COS, DEG, BCD_TO, IsINF, IsNAN, LN, LOG, RAD, SIN, SQR, TAN, TO_BCD, TRUNC
    3 **
    4 - (negate), NOT, !
    5 *, /, MOD
    6 - (subtract), +
    7 AND
    8 XOR
    9 OR
    10 <, <=, >, >=, =, <>
    11 &&
    12 ^^
    13 ||
    '''


    def __init__(self, tags: Dict[str, Any]):
        """Initialize with tag dictionary containing PLC variable values"""
        self.tags = tags
    
    def tokenize(self, expression: str) -> list:
        """Split expression into tokens (tags, operators, numbers)"""
        # Regex to match tags, numbers, operators, parentheses
        token_pattern = r'([a-zA-Z_][a-zA-Z0-9_.]*|\d+\.?\d*|[^a-zA-Z0-9_.\s])'
        tokens = re.findall(token_pattern, expression.replace(' ', ''))
        return [t for t in tokens if t.strip()]
    
    def resolve_tag(self, tag_name: str) -> Any:
        """Resolve a tag name to its value"""
        # Handle nested tags like "myTag.SubTag"
        keys = tag_name.split('.')
        value = self.tags
        
        for key in keys:
            if isinstance(value, dict):
                value = value.get(key)
            else:
                raise KeyError(f"Cannot traverse {key} in {tag_name}")
        
        if value is None:
            raise KeyError(f"Tag '{tag_name}' not found")
        return value
    
    def is_numeric_literal(self, token: str) -> bool:
        """Check if token is a number literal"""
        try:
            float(token)
            return True
        except ValueError:
            return False
    
    def parse_value(self, token: str) -> Any:
        """Parse a single token (either tag or literal)"""
        if self.is_numeric_literal(token):
            # Return int if whole number, else float
            return int(token) if '.' not in token else float(token)
        elif token.startswith('(') and token.endswith(')'):
            # Recursive evaluation of parenthesized expression
            return self.evaluate(token[1:-1].strip())
        else:
            return self.resolve_tag(token)
    
    def evaluate_simple(self, expression: str) -> Any:
        """Evaluate binary expression: operand_a operator operand_b"""
        # Find operator position (handle multi-char operators like <=, >=, <>, MOD)
        op_pos = -1
        op_str = None
        
        # Check multi-character operators first
        for op in ['<=', '>=', '<>', '**', 'MOD', 'AND', 'OR', 'XOR']:
            if f' {op} ' in expression or expression.startswith(op) or expression.endswith(op):
                parts = expression.split(f' {op} ')
                if len(parts) == 2:
                    op_pos = expression.find(f' {op} ')
                    op_str = op
                    break
        
        # Single character operators
        if op_str is None:
            for op in ['+', '-', '*', '/', '<', '>', '=', '^']:
                if op in expression:
                    parts = expression.split(op)
                    if len(parts) == 2:
                        op_pos = expression.find(op)
                        op_str = op
                        break
        
        if op_str is None or op_pos == -1:
            # No operator found, treat as single value assignment or comparison
            if '=' in expression and '<>' not in expression:
                # Assignment case: xxx = yyy
                parts = expression.split('=')
                if len(parts) == 2:
                    target_tag = parts[0].strip()
                    value_expr = parts[1].strip()
                    evaluated_value = self.evaluate_simple(value_expr)
                    # Store back to tags
                    keys = target_tag.split('.')
                    target_dict = self.tags
                    for key in keys[:-1]:
                        target_dict = target_dict[key]
                    target_dict[keys[-1]] = evaluated_value
                    return evaluated_value
            else:
                return self.parse_value(expression.strip())
        
        left_part = expression[:op_pos].strip()
        right_part = expression[op_pos + len(op_str):].strip()
        
        left_val = self.evaluate_simple(left_part)
        right_val = self.evaluate_simple(right_part)
        
        return self.OPERATORS[op_str](left_val, right_val)
    
    def evaluate(self, expression: str) -> Any:
        """Main entry point - handles complex expressions with parentheses"""
        # Handle parentheses recursively
        while '(' in expression:
            start = expression.rfind('(')
            end = expression.find(')', start)
            
            if end == -1:
                raise ValueError("Unmatched parentheses")
            
            inner_expr = expression[start + 1:end]
            inner_result = self.evaluate(inner_expr)
            
            # Replace the parenthesized section with the result
            expression = expression[:start] + str(inner_result) + expression[end + 1:]
        
        return self.evaluate_simple(expression)