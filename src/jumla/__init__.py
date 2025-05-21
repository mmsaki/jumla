import argparse
from pathlib import Path
from jumla.cli import write_to_dataset
from jumla.log import logger


def main():
    parser = argparse.ArgumentParser(
        description="Jumla: Generate Lean tasks from Python specs."
    )
    parser.add_argument("path", help="Path to example .py file OR folder of examples")
    parser.add_argument("--log", action="store_true", help="Print debug logs")
    args = parser.parse_args()

    path = Path(args.path)

    if not path.exists():
        print(f"[✗] Not found: {path}")
        return

    if path.is_dir():
        py_files = list(path.glob("*.py"))
        if not py_files:
            logger.warn(f"[!] No .py files found in {path}")
            return
        logger.info(f"Processing {len(py_files)} files in {path}")
        for i, py_file in enumerate(py_files):
            logger.bullet(f"file: {py_file.name}")
            task_id = f"task_id_{i}"
            write_to_dataset(py_file, task_id=task_id, log=args.log)
    elif path.suffix == ".py":
        write_to_dataset(path, "task_id_0", log=args.log)
    else:
        logger.error(f"[✗] Invalid file type: {path.name} (expected .py or directory)")
    logger.finish()


if __name__ == "__main__":
    main()
