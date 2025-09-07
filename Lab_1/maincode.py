"""
A simple calculator program demonstrating functions, loops, and error handling.
"""

def add(a, b):
    """Return the sum of two numbers."""
    return a + b

def subtract(a, b):
    """Return the difference between two numbers."""
    return a - b

def multiply(a, b):
    """Return the product of two numbers."""
    return a * b

def divide(a, b):
    """Return the division of two numbers."""
    if b == 0:
        return "Error: Division by zero"
    return a / b

def main():
    """Main function to run the calculator."""
    print("Available operations: add, subtract, multiply, divide")
    while True:
        operation = input("\nEnter operation (or 'quit' to exit): ").lower()
        if operation == "quit":
            print("Goodbye")
            break

        try:
            num1 = float(input("Enter first number: "))
            num2 = float(input("Enter second number: "))
        except ValueError:
            print("Invalid input. Please enter numbers.")
            continue

        if operation == "add":
            print("Result:", add(num1, num2))
        elif operation == "subtract":
            print("Result:", subtract(num1, num2))
        elif operation == "multiply":
            print("Result:", multiply(num1, num2))
        elif operation == "divide":
            print("Result:", divide(num1, num2))
        else:
            print("Invalid operation. Try again.")

if __name__ == "__main__":
    main()
