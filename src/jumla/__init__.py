from jumla.dataset import Dataset


def main():
    print("Hello from jumla!")
    fun = """def minOfThree(a: int, b: int, c: int) -> int:
    return min(a, b, c)"""
    description = """This task requires writing a Lean 4 method that finds the minimum among three given integers. The method should return the smallest value, ensuring that the result is less than or equal to each of the input numbers and that it is one of the provided integers."""

    inputs = """The input consists of three integers:
a: The first integer.
b: The second integer.
c: The third integer."""

    outputs = """The output is an integer:
Returns the minimum of the three input numbers, assuring that the returned value is less than or equal to a, b, and c, and that it matches one of these values."""
    dataset = Dataset(fun, description, inputs, outputs)

    desc_file = dataset.build_description(log=True)
    signature_file = dataset.build_signature(log=True)
    task_file = dataset.build_lean_task(log=True)
    dataset.write_all()


if __name__ == "__main__":
    main()
