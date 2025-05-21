import importlib.util
from pathlib import Path
from jumla.dataset import Dataset
from jumla.log import logger


def create_dataset(path: Path, dir_name: str) -> Dataset:
    """Load a Dataset object or construct one from raw fields in a Python file."""
    spec = importlib.util.spec_from_file_location("example", path)

    if spec is None:
        raise ImportError(f"Could not create import spec for {path}")

    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None, f"No loader for module {path}"
    spec.loader.exec_module(module)

    if hasattr(module, "dataset"):
        return module.dataset

    required = ["function", "description_doc", "input_doc", "output_doc", "test_cases"]
    if not all(hasattr(module, key) for key in required):
        raise AttributeError(
            f"{path} must define either `dataset` or all of: {', '.join(required)}"
        )

    return Dataset(
        function=module.function,
        description_doc=module.description_doc,
        input_doc=module.input_doc,
        output_doc=module.output_doc,
        test_cases=module.test_cases,
        dir=dir_name,
    )


def write_to_dataset(path: Path, task_id: str, log=False):
    try:
        dataset = create_dataset(path, dir_name=task_id)
        dataset.write_all(log=log)
        logger.bullet(f"Generated: {dataset.dir}")
    except Exception as e:
        logger.error(f"Failed on {path.name}: {e}")
