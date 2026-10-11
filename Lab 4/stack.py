# Infix to Postfix - Stack (linked-list based, same style as linked_list.py)

# Put your own experiments inside the `if __name__ == "__main__":` block at the
# bottom. Code at the top level of this file runs when your work is marked.


class Node:
    def __init__(self, data):
        self.data = data
        self.next = None


class Stack:
    def __init__(self):
        self.top = None

    def is_empty(self):
        return self.top is None

    def push(self, data):
        new_node = Node(data)
        new_node.next = self.top
        self.top = new_node

    def pop(self):
        if self.top is None:
            return None
        removed_node = self.top
        self.top = self.top.next
        return removed_node.data

    def peek(self):
        if self.top is None:
            return None
        return self.top.data

    def items(self):
        """Return the stack contents from bottom to top (for display)."""
        data, current_node = [], self.top
        while current_node:
            data.append(current_node.data)
            current_node = current_node.next
        return data[::-1]


PRECEDENCE = {"+": 1, "-": 1, "*": 2, "/": 2, "%": 2, "^": 3}
RIGHT_ASSOCIATIVE = {"^"}


def tokenize(expression):
    """Split an infix string into operands, operators and parentheses.
    Raises ValueError when it meets a character it does not understand."""
    tokens, i = [], 0
    while i < len(expression):
        ch = expression[i]
        if ch.isspace():
            i += 1
        elif ch.isalnum() or ch == ".":          # operand: letters / digits / decimals
            start = i
            while i < len(expression) and (expression[i].isalnum() or expression[i] == "."):
                i += 1
            tokens.append(expression[start:i])
        elif ch in PRECEDENCE or ch in "()":
            tokens.append(ch)
            i += 1
        else:
            raise ValueError(f"Unexpected character {ch!r}.")
    return tokens


def infix_to_postfix(expression):
    """Convert an infix expression to postfix.
    Returns (postfix_string, steps). Raises ValueError for invalid input.
    Each step is a dict: token, output, stack."""
    tokens = tokenize(expression)
    if not tokens:
        raise ValueError("Enter an expression first.")

    stack, output, steps = Stack(), [], []
    expect_operand = True                         # catches things like "A + * B"

    for token in tokens:
        if token[0].isalnum() or token[0] == ".":            # operand
            if not expect_operand:
                raise ValueError("Two operands in a row, an operator is missing.")
            output.append(token)
            expect_operand = False
        elif token == "(":
            if not expect_operand:
                raise ValueError("An operator is missing before '('.")
            stack.push(token)
        elif token == ")":
            if expect_operand:
                raise ValueError("An operand is missing before ')'.")
            while not stack.is_empty() and stack.peek() != "(":
                output.append(stack.pop())
            if stack.is_empty():
                raise ValueError("Parentheses do not match: extra ')'.")
            stack.pop()                                       # discard the '('
        else:                                                 # operator
            if expect_operand:
                raise ValueError(f"An operand is missing before '{token}'.")
            while (not stack.is_empty() and stack.peek() != "("
                   and (PRECEDENCE[stack.peek()] > PRECEDENCE[token]
                        or (PRECEDENCE[stack.peek()] == PRECEDENCE[token]
                            and token not in RIGHT_ASSOCIATIVE))):
                output.append(stack.pop())
            stack.push(token)
            expect_operand = True
        steps.append({"token": token, "output": " ".join(output), "stack": " ".join(stack.items())})

    if expect_operand:
        raise ValueError("The expression ends with an operator.")

    while not stack.is_empty():
        top = stack.pop()
        if top == "(":
            raise ValueError("Parentheses do not match: missing ')'.")
        output.append(top)
        steps.append({"token": "pop", "output": " ".join(output), "stack": " ".join(stack.items())})

    return " ".join(output), steps


if __name__ == "__main__":
    for sample in ["A + B * C", "(A + B) * C", "A + B * (C - D) / E", "A ^ B ^ C"]:
        print(sample, "->", infix_to_postfix(sample)[0])
