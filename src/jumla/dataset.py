import json
import os
from typing import Dict
from dataclasses import dataclass
from .files import Files
from .parser import PythonParser


@dataclass
class Dataset(Files, PythonParser):
    DESCRIPTION_TITLE = "-----Description-----"
    INPUT_TITLE = "-----Input-----"
    OUTPUT_TITLE = "-----Output-----"
    DESCRIPTION_FILENAME = "description.txt"
    TASK_FILENAME = "task.lean"
    SIGNATURE_FILENAME = "signature.json"
    CODE_START = "  -- << CODE START >>"
    CODE_BODY = "  {{code}}"
    CODE_END = "  -- << CODE END >>"
    SPEC_START = "  -- << SPEC START >>"
    SPEC_BODY = "  {{spec}}"
    SPEC_END = "  -- << SPEC END >>"
    PROOF_START = "  -- << PROOF START >>"
    PROOF_BODY = "  {{proof}}"
    PROOF_END = "  -- << PROOF END >>"

    def __init__(
        self,
        function: str,
        description: str,
        inputs: str,
        outputs: str,
        dir="task_id_0",
    ):
        self.function = function
        self.description = description
        self.inputs = inputs
        self.outputs = outputs
        function_name, params, return_type = self.extract_function_signature()
        self.function_name = function_name
        self.params = params
        self.return_type = return_type
        self.lean_arguments = self.build_lean_args()
        self.signature = self.build_signature()
        self.lean_task = self.build_lean_task()
        os.makedirs("dataset")
        if not os.path.exists(f"dataset/{dir}"):
            os.makedirs(f"dataset/{dir}")
        self.dir = f"dataset/{dir}/"

    def build_description(self, log=False):
        description = (
            f"{self.DESCRIPTION_TITLE}\n{self.description}\n\n"
            f"{self.INPUT_TITLE}\n{self.inputs}\n\n"
            f"{self.OUTPUT_TITLE}\n{self.outputs}"
        )

        if log:
            print(description)

        return description

    def write_description(self, log=False):
        data = self.build_description(log)
        path = self.dir + self.DESCRIPTION_FILENAME
        self.write_to_file(path, data, log=log)

    def write_signature(self, log=False):
        signature = self.build_signature()
        signature_str = json.dumps(signature, indent=2)
        path = self.dir + self.SIGNATURE_FILENAME
        self.write_to_file(path, signature_str, log=log)

    def write_lean_task(self, log=False):
        lean_sig = self.build_lean_task()
        path = self.dir + self.TASK_FILENAME
        self.write_to_file(path, lean_sig, log=log)

    def write_all(self, log=False):
        self.write_description(log=log)
        self.write_signature(log=log)
        self.write_lean_task(log=log)

    def build_signature(self, log=False) -> Dict[str, str]:
        signature = {
            "name": self.function_name,
            "parameters": self.params,
            "return_type": self.return_type,
        }
        if log:
            print(json.dumps(signature, indent=2))
        return signature

    def build_lean_task(self, log=False) -> str:
        imports = "import Mathlib\nimport Aesop\n"
        function = self.build_lean_function()
        spec = self.build_lean_spec()
        theorem = self.build_lean_theorem()
        lean_task = f"{imports}\n{function}\n\n{spec}\n\n{theorem}"

        if log:
            print(lean_task)

        return lean_task

    def build_lean_function(self) -> str:
        body = f"{self.CODE_START}\n{self.CODE_BODY}\n{self.CODE_END}"
        return f"def {self.function_name} {self.lean_arguments} : {self.return_type} :=\n{body}"

    def build_lean_spec(self, log=False) -> str:
        function_definition = (
            f"def {self.function_name}_spec "
            f"{self.lean_arguments} "
            f"(_ : {self.return_type}) : Prop :="
        )
        spec = (
            f"{function_definition}\n"
            f"{self.SPEC_START}\n{self.SPEC_BODY}\n{self.SPEC_END}"
        )
        if log:
            print(spec)
        return spec

    def build_lean_theorem(self, log=False):
        theorem_definition = (
            f"theorem {self.function_name}_spec_satisfied {self.lean_arguments} :"
        )
        args = " ".join(param["param_name"] for param in self.params)
        spec_prop = (
            f"  {self.function_name}_spec {args} ({self.function_name} {args}) := by"
        )
        proof_unfold = f"  unfold {self.function_name} {self.function_name}_spec"
        theorem = (
            f"{theorem_definition}\n"
            f"{spec_prop}\n"
            f"{self.PROOF_START}\n"
            f"{proof_unfold}\n"
            f"{self.PROOF_BODY}"
            f"\n{self.PROOF_END}"
        )

        if log:
            print(theorem)

        return theorem

    def build_lean_args(self):
        params = [
            f"({param['param_name']} : {param['param_type']})" for param in self.params
        ]
        parameters = " ".join(params)
        return parameters
