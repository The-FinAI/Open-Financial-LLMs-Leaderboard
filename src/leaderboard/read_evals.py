import json
import os
import math
import glob
from dataclasses import dataclass
from typing import Dict, List, Tuple

import dateutil
import numpy as np

from src.display.utils import AutoEvalColumn, ModelType, Tasks
from src.display.formatting import make_clickable_model
from src.submission.check_validity import is_model_on_hub


@dataclass
class EvalResult:
    eval_name: str
    full_model: str
    org: str
    model: str
    revision: str
    results: dict
    precision: str = ""
    model_type: ModelType = ModelType.Unknown
    weight_type: str = "Original"
    license: str = "?"
    likes: int = 0
    num_params: int = 0
    date: str = ""
    still_on_hub: bool = False

    @classmethod
    def init_from_json_file(self, json_filepath):
        with open(json_filepath) as fp:
            data = json.load(fp)

        # We manage the legacy config format
        config = data.get("config", data.get("config_general", None))

        # Precision
        precision = config.get("model_dtype")
        if precision == "None":
            precision = "GPTQ"

        # Get model and org
        org_and_model = config.get("model_name", config.get("model_args", None))
        org_and_model = org_and_model.split("/", 1)

        if len(org_and_model) == 1:
            org = None
            model = org_and_model[0]
            result_key = f"{model}_{precision}"
        else:
            org = org_and_model[0]
            model = org_and_model[1]
            result_key = f"{org}_{model}_{precision}"

        still_on_hub = is_model_on_hub("/".join(org_and_model), config.get("model_sha", "main"), trust_remote_code=True)[0]

        # Extract results available in this file (some results are split in several files)
        results = {}
        for task in Tasks:
            task = task.value
            # We skip old mmlu entries
            wrong_mmlu_version = False
            if task.benchmark == "hendrycksTest":
                for mmlu_k in ["harness|hendrycksTest-abstract_algebra|5", "hendrycksTest-abstract_algebra"]:
                    if mmlu_k in data["versions"] and data["versions"][mmlu_k] == 0:
                        wrong_mmlu_version = True

            if wrong_mmlu_version:
                continue

            # Some truthfulQA values are NaNs
            if task.benchmark == "truthfulqa:mc" and task.benchmark in data["results"]:
                if math.isnan(float(data["results"][task.benchmark][task.metric])):
                    results[task.benchmark] = 0.0
                    continue

            # We average all scores of a given metric (mostly for mmlu)
            accs = np.array([v.get(task.metric, None) for k, v in data["results"].items() if task.benchmark in k])
            if accs.size == 0 or any([acc is None for acc in accs]):
                continue

            mean_acc = np.mean(accs) * 100.0
            results[task.benchmark] = mean_acc

        return self(
            eval_name=result_key,
            full_model="/".join(org_and_model),
            org=org,
            model=model,
            results=results,
            precision=precision,  # todo model_type=, weight_type=
            revision=config.get("model_sha", ""),
            date=config.get("submission_date", ""),
            still_on_hub=still_on_hub,
        )

    def update_with_request_file(self):
        request_file = get_request_file_for_model(self.full_model, self.precision)

        try:
            with open(request_file, "r") as f:
                request = json.load(f)
            self.model_type = ModelType.from_str(request.get("model_type", ""))
            self.license = request.get("license", "?")
            self.likes = request.get("likes", 0)
            self.num_params = request.get("params", 0)
        except Exception:
            print(f"Could not find request file for {self.org}/{self.model}")

    def to_dict(self):
        average = sum([v for v in self.results.values() if v is not None]) / len(Tasks)
        data_dict = {
            "eval_name": self.eval_name,  # not a column, just a save name,
            AutoEvalColumn.precision.name: self.precision,
            AutoEvalColumn.model_type.name: self.model_type.value.name,
            AutoEvalColumn.model_type_symbol.name: self.model_type.value.symbol,
            AutoEvalColumn.weight_type.name: self.weight_type,
            AutoEvalColumn.model.name: make_clickable_model(self.full_model),
            AutoEvalColumn.dummy.name: self.full_model,
            AutoEvalColumn.revision.name: self.revision,
            AutoEvalColumn.average.name: average,
            AutoEvalColumn.license.name: self.license,
            AutoEvalColumn.likes.name: self.likes,
            AutoEvalColumn.params.name: self.num_params,
            AutoEvalColumn.still_on_hub.name: self.still_on_hub,
        }

        for task in Tasks:
            data_dict[task.value.col_name] = self.results[task.value.benchmark]

        return data_dict


def get_request_file_for_model(model_name, precision):
    request_files = os.path.join(
        "eval-queue",
        f"{model_name}_eval_request_*.json",
    )
    request_files = glob.glob(request_files)

    # Select correct request file (precision)
    request_file = ""
    request_files = sorted(request_files, reverse=True)
    for tmp_request_file in request_files:
        with open(tmp_request_file, "r") as f:
            req_content = json.load(f)
            if (
                req_content["status"] in ["FINISHED", "PENDING_NEW_EVAL"]
                and req_content["precision"] == precision.split(".")[-1]
            ):
                request_file = tmp_request_file
    return request_file


def get_eval_results(results_path: str) -> List[EvalResult]:
    json_filepaths = []

    for root, _, files in os.walk(results_path):
        # We should only have json files in model results
        if len(files) == 0 or any([not f.endswith(".json") for f in files]):
            continue

        # Sort the files by date
        try:
            files.sort(key=lambda x: x.removesuffix(".json").removeprefix("results_")[:-7])
        except dateutil.parser._parser.ParserError:
            files = [files[-1]]

        # up_to_date = files[-1]
        for file in files:
            json_filepaths.append(os.path.join(root, file))

    eval_results = {}
    for json_filepath in json_filepaths:
        # Creation of result
        eval_result = EvalResult.init_from_json_file(json_filepath)
        eval_result.update_with_request_file()

        # Store results of same eval together
        eval_name = eval_result.eval_name
        if eval_name in eval_results.keys():
            eval_results[eval_name].results.update({k: v for k, v in eval_result.results.items() if v is not None})
        else:
            eval_results[eval_name] = eval_result

    results = []
    for v in eval_results.values():
        try:
            results.append(v.to_dict())
        except KeyError: # not all eval values present 
            continue

    return results
