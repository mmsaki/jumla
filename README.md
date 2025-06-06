# Jumla

[![PyPI - Version](https://img.shields.io/pypi/v/jumla)](https://pypi.org/project/jumla/)
![GitHub Issues or Pull Requests](https://img.shields.io/github/issues/mmsaki/jumla)
![GitHub last commit](https://img.shields.io/github/last-commit/mmsaki/jumla)
![PyPI - Downloads](https://img.shields.io/pypi/dm/jumla)
![PyPI - License](https://img.shields.io/pypi/l/jumla)
![GitHub repo size](https://img.shields.io/github/repo-size/mmsaki/jumla)
[![X (formerly Twitter) Follow](https://img.shields.io/twitter/follow/msakiart)](https://x.com/intent/user?screen_name=msakiart)

**Jumla** is a Python package for programmatically generating structured datasets of Lean 4 verification tasks from Python functions, complete with specifications, test cases, and formal proof scaffolds.

> _"Don't ship vibes — ship proofs."_

---

## 📦 Installation

If installing from pypi:

```bash
pip install jumla
```

This installs the CLI command:

```bash
jumla
```


## Usage

Generate a Lean dataset from a single Python task file:

```bash
jumla examples/min_of_three.py
```

Or process all Python files in a folder:

```bash
jumla examples/
```

Output will be written to the `dataset/` folder (e.g. `dataset/task_id_0/`).

Use `--log` for detailed debug output:

```bash
jumla examples/ --log
```


## Development Setup

> [!NOTE]
> Install `uv` (if not already)
>
> ```bash
> curl -LsSf https://astral.sh/uv/install.sh | sh
> ```

Clone the repo

```bash
git clone https://github.com/mmsaki/jumla
cd jumla
```

Create a virtual environment

```bash
uv venv
source .venv/bin/activate
```

Install the project in editable mode

```bash
uv sync
uv pip install -e .
```

Run the CLI

```bash
jumla examples/
```


## Example Structure

```python
# examples/min_of_three.py
import inspect, textwrap

def minOfThree(a: int, b: int, c: int) -> int:
    return min(a, b, c)

function = textwrap.dedent(inspect.getsource(minOfThree))

description_doc = "This task requires writing a Lean 4 method..."
input_doc = "The input consists of three integers..."
output_doc = "The output is an integer..."
test_cases = [
    {"input": {"a": 3, "b": 2, "c": 1}, "expected": 1, "unexpected": [2, 3, -1]},
    ...
]
```


## 📁 Output Directory Example

```
dataset/
├── task_id_0/
│   ├── description.txt
│   ├── signature.json
│   ├── task.lean
│   ├── test.json
│   └── tests.lean
```


Let me know if you want to add Lean syntax checks, markdown summaries, or GitHub CI automation!
