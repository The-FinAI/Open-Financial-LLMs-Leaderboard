---
title: Open FinLLM Leaderboard
emoji: 🥇
colorFrom: green
colorTo: indigo
sdk: gradio
sdk_version: 4.42.0
app_file: app.py
pinned: true
license: apache-2.0
---

![badge-labs](https://user-images.githubusercontent.com/327285/230928932-7c75f8ed-e57b-41db-9fb7-a292a13a1e58.svg)

# Open Financial LLM Leaderboard (OFLL)

The growing complexity of financial language models (LLMs) demands evaluations that go beyond general NLP benchmarks. Traditional leaderboards often focus on broader tasks like translation or summarization, but they fall short of addressing the specific needs of the finance industry. Financial tasks such as predicting stock movements, assessing credit risks, and extracting information from financial reports present unique challenges, requiring models with specialized capabilities. This is why we created the **Open Financial LLM Leaderboard (OFLL)**.

## Why OFLL?

OFLL provides a specialized evaluation framework tailored specifically to the financial sector. It fills a critical gap by offering a transparent, one-stop solution to assess model readiness for real-world financial applications. The leaderboard focuses on tasks that matter most to finance professionals—information extraction from financial documents, market sentiment analysis, and financial trend forecasting.

## Key Differentiators

- **Comprehensive Financial Task Coverage**: Unlike general LLM leaderboards that evaluate broad NLP capabilities, OFLL focuses exclusively on tasks directly relevant to finance. These include information extraction, sentiment analysis, credit risk scoring, and stock movement forecasting—tasks crucial for real-world financial decision-making.

- **Real-World Financial Relevance**: OFLL uses datasets that represent real-world challenges in the finance industry. This ensures models are not only tested on general NLP tasks but are also evaluated on their ability to handle complex financial data, making them suitable for industry applications.

- **Focused Zero-Shot Evaluation**: OFLL employs a zero-shot evaluation method, testing models on unseen financial tasks without prior fine-tuning. This highlights a model’s ability to generalize and perform well in financial contexts, such as predicting stock price movements or extracting entities from regulatory filings, without being explicitly trained on these tasks.

## Key Features of OFLL

- **Diverse Task Categories**: OFLL covers tasks across seven categories: Information Extraction (IE), Textual Analysis (TA), Question Answering (QA), Text Generation (TG), Risk Management (RM), Forecasting (FO), and Decision-Making (DM).

- **Robust Evaluation Metrics**: Models are assessed using various metrics, including Accuracy, F1 Score, ROUGE Score, and Matthews Correlation Coefficient (MCC). These metrics provide a multidimensional view of model performance, helping users identify the strengths and weaknesses of each model.

The Open Financial LLM Leaderboard aims to set a new standard in evaluating the capabilities of language models in the financial domain, offering a specialized, real-world-focused benchmarking solution.


# Start the configuration

Most of the variables to change for a default leaderboard are in `src/env.py` (replace the path for your leaderboard) and `src/about.py` (for tasks).

Results files should have the following format and be stored as json files:
```json
{
    "config": {
        "model_dtype": "torch.float16", # or torch.bfloat16 or 8bit or 4bit
        "model_name": "path of the model on the hub: org/model",
        "model_sha": "revision on the hub",
    },
    "results": {
        "task_name": {
            "metric_name": score,
        },
        "task_name2": {
            "metric_name": score,
        }
    }
}
```

Request files are created automatically by this tool.

If you encounter problem on the space, don't hesitate to restart it to remove the create eval-queue, eval-queue-bk, eval-results and eval-results-bk created folder.

# Code logic for more complex edits

You'll find 
- the main table' columns names and properties in `src/display/utils.py`
- the logic to read all results and request files, then convert them in dataframe lines, in `src/leaderboard/read_evals.py`, and `src/populate.py`
- teh logic to allow or filter submissions in `src/submission/submit.py` and `src/submission/check_validity.py`

## License

Copyright 2024 Fintech Open Source Foundation

Distributed under the [Apache License, Version 2.0](http://www.apache.org/licenses/LICENSE-2.0).

SPDX-License-Identifier: [Apache-2.0](https://spdx.org/licenses/Apache-2.0)


### Current submissions are manully evaluated. Will open a automatic evaluation pipeline in the future update
tags:
  - leaderboard
  - modality:text
  - submission:manual
  - test:public
  - judge:humans
  - eval:generation
  - language:English

