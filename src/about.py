from dataclasses import dataclass
from enum import Enum

@dataclass
class Task:
    benchmark: str
    metric: str
    col_name: str


# Select your tasks here
# ---------------------------------------------------
class Tasks(Enum):
    # task_key in the json file, metric_key in the json file, name to display in the leaderboard 
    task0 = Task("FPB", "F1", "FPB-F1")
    task1 = Task("FPB", "Acc", "FPB-Acc")
    task2 = Task("FiQA-SA", "F1", "FiQA-SA-F1")
    task3 = Task("TSA", "RMSE", "TSA-RMSE")
    task4 = Task("Headlines", "AvgF1", "Headlines-AvgF1")
    task5 = Task("FOMC", "F1", "FOMC-F1")
    task6 = Task("FOMC", "Acc", "FOMC-Acc")
    task7 = Task("FinArg-ACC", "MicroF1", "FinArg-ACC-MicroF1")
    task8 = Task("FinArg-ARC", "MicroF1", "FinArg-ARC-MicroF1")
    task9 = Task("MultiFin", "MicroF1", "Multifin-MicroF1")
    task10 = Task("MA", "MicroF1", "MA-MicroF1")
    task11 = Task("MLESG", "MicroF1", "MLESG-MicroF1")
    task12 = Task("NER", "EntityF1", "NER-EntityF1")
    task13 = Task("FINER-ORD", "EntityF1", "FINER-ORD-EntityF1")
    task14 = Task("FinRED", "F1", "FinRED-F1")
    task15 = Task("SC", "F1", "SC-F1")
    task16 = Task("CD", "F1", "CD-F1")
    task17 = Task("FinQA", "EmAcc", "FinQA-EmAcc")
    task18 = Task("TATQA", "EmAcc", "TATQA-EmAcc")
    task19 = Task("ConvFinQA", "EmAcc", "ConvFinQA-EmAcc")
    task20 = Task("FNXL", "EntityF1", "FNXL-EntityF1")
    task21 = Task("FSRL", "EntityF1", "FSRL-EntityF1")
    task22 = Task("EDTSUM", "Rouge-1", "EDTSUM-Rouge-1")
    task23 = Task("EDTSUM", "BertScore", "EDTSUM-BertScore")
    task24 = Task("EDTSUM", "BartScore", "EDTSUM-BartScore")
    task25 = Task("ECTSUM", "Rouge-1", "ECTSUM-Rouge-1")
    task26 = Task("ECTSUM", "BertScore", "ECTSUM-BertScore")
    task27 = Task("ECTSUM", "BartScore", "ECTSUM-BartScore")
    task28 = Task("BigData22", "Acc", "BigData22-Acc")
    task29 = Task("BigData22", "MCC", "BigData22-MCC")
    task30 = Task("ACL18", "Acc", "ACL18-Acc")
    task31 = Task("ACL18", "MCC", "ACL18-MCC")
    task32 = Task("CIKM18", "Acc", "CIKM18-Acc")
    task33 = Task("CIKM18", "MCC", "CIKM18-MCC")
    task34 = Task("German", "F1", "German-F1")
    task35 = Task("German", "MCC", "German-MCC")
    task36 = Task("Australian", "F1", "Australian-F1")
    task37 = Task("Australian", "MCC", "Australian-MCC")
    task38 = Task("LendingClub", "F1", "LendingClub-F1")
    task39 = Task("LendingClub", "MCC", "LendingClub-MCC")
    task40 = Task("ccf", "F1", "ccf-F1")
    task41 = Task("ccf", "MCC", "ccf-MCC")
    task42 = Task("ccfraud", "F1", "ccfraud-F1")
    task43 = Task("ccfraud", "MCC", "ccfraud-MCC")
    task44 = Task("polish", "F1", "polish-F1")
    task45 = Task("polish", "MCC", "polish-MCC")
    task46 = Task("taiwan", "F1", "taiwan-F1")
    task47 = Task("taiwan", "MCC", "taiwan-MCC")
    task48 = Task("portoseguro", "F1", "portoseguro-F1")
    task49 = Task("portoseguro", "MCC", "portoseguro-MCC")
    task50 = Task("travelinsurance", "F1", "travelinsurance-F1")
    task51 = Task("travelinsurance", "MCC", "travelinsurance-MCC")

NUM_FEWSHOT = 0 # Change with your few shot
# ---------------------------------------------------



# Your leaderboard name
TITLE = """<h1 align="center" id="space-title">🐲 The FinBen FLARE Leaderboard</h1>"""

# What does your leaderboard evaluate?
INTRODUCTION_TEXT = """📊 The FinBen FLARE Leaderboard is designed to rigorously track, rank, and evaluate state-of-the-art models in financial Natural Language Understanding and Prediction. 

📈 Unique to FLARE, our leaderboard not only covers standard NLP tasks but also incorporates financial prediction tasks such as stock movement and credit scoring, offering a more comprehensive evaluation for real-world financial applications.

📚 Our evaluation metrics include, but are not limited to, Accuracy, F1 Score, ROUGE score, BERTScore, and Matthews correlation coefficient (MCC), providing a multidimensional assessment of model performance.

🔗 For more details, refer to our GitHub page [here](https://github.com/The-FinAI/PIXIU).
"""

# Which evaluations are you running? how can people reproduce what you have?
LLM_BENCHMARKS_TEXT = f"""
## How it works

## Reproducibility
To reproduce our results, here is the commands you can run:

"""

EVALUATION_QUEUE_TEXT = """
## Some good practices before submitting a model

### 1) Make sure you can load your model and tokenizer using AutoClasses:
```python
from transformers import AutoConfig, AutoModel, AutoTokenizer
config = AutoConfig.from_pretrained("your model name", revision=revision)
model = AutoModel.from_pretrained("your model name", revision=revision)
tokenizer = AutoTokenizer.from_pretrained("your model name", revision=revision)
```
If this step fails, follow the error messages to debug your model before submitting it. It's likely your model has been improperly uploaded.

Note: make sure your model is public!
Note: if your model needs `use_remote_code=True`, we do not support this option yet but we are working on adding it, stay posted!

### 2) Convert your model weights to [safetensors](https://huggingface.co/docs/safetensors/index)
It's a new format for storing weights which is safer and faster to load and use. It will also allow us to add the number of parameters of your model to the `Extended Viewer`!

### 3) Make sure your model has an open license!
This is a leaderboard for Open LLMs, and we'd love for as many people as possible to know they can use your model 🤗

### 4) Fill up your model card
When we add extra information about models to the leaderboard, it will be automatically taken from the model card

## In case of model failure
If your model is displayed in the `FAILED` category, its execution stopped.
Make sure you have followed the above steps first.
If everything is done, check you can launch the EleutherAIHarness on your model locally, using the above command without modifications (you can add `--limit` to limit the number of examples per task).
"""

CITATION_BUTTON_LABEL = "Copy the following snippet to cite these results"
CITATION_BUTTON_TEXT = r"""
"""
