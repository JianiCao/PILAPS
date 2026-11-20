# PILAPS: A Bilingual Benchmark for Evaluating Pragmatic Inference across Phenomena and Settings

## Disclaimer
This repository contains experimental software and data, published for the sole purpose of providing additional background on the accompanying paper.

📄 [Paper](https://arxiv.org/abs/2611.25459)

><details>
><summary> <b>Abstract</b> </summary>
>Recent work reports strong pragmatic performance by large language models (LLMs) in English, yet whether this performance generalises across languages and evaluation settings remains unclear. This question is increasingly important as LLMs are deployed across languages, cultures, and conversational contexts. In this paper, we first introduce PILAPS, a bilingual English/Mandarin Chinese benchmark covering eight pragmatic phenomena across purpose-written and dialogue-derived items, with both culturally adapted and independently sourced data. We then evaluate eight LLMs from four families across a range of model sizes and prompting strategies. Our results reveal substantial variation across models and pragmatic phenomena: open-source models continue to struggle particularly with humour, while cross-linguistic performance varies with model origin. Our error analysis shows that, compared with human participants, models are more prone to literal interpretations in conversational contexts. Theory-of-Mind prompting lowers the literal share of errors, whereas Chain-of-Thought prompting slightly raises it. Together, these findings demonstrate that strong pragmatic performance in one evaluation setting does not necessarily generalise across languages or conversational contexts.
></details></p>

## Dataset
PILAPS is a bilingual benchmark in which the English portion incorporates
two existing academic datasets: [PragMega](https://github.com/jennhu/lm-pragmatics) and [Ludwig](https://github.com/LauraRuis/do-pigs-fly).
The Chinese version is culturally adapted from the English subset.
Additionally, we introduce new multi-turn evaluation items.

| Subset (`dataset_type`) | Description | File |
|---|---|---|
| `constructed` | Purpose-written items covering eight pragmatic phenomena; English items build on [PragMega](https://github.com/jennhu/lm-pragmatics), Chinese items are culturally adapted | `master_constructed.csv` |
| `dialogue` | Newly created multi-turn, dialogue-derived items in both languages | `master_dialogue.csv` |
| `ludwig` | Implicature items from [Ludwig](https://github.com/LauraRuis/do-pigs-fly), with Chinese adaptation | `ludwig.csv` |

## Request the data
The dataset is not included in this repository. To obtain it, please fill in the request form:

👉 **[PILAPS data request form](https://forms.gle/JFKN6AKiw9rfFqwJ6)**

You will receive a download link after submitting the form. Place the three CSV files in `src/data/` before running the evaluation.

## How to run
```
pip install -r requirements.txt

python src/main.py \
            model.short_name=MODEL_SHORT \
            dataset.dataset_type=DATA \
            dataset.language=LANG \
            prompt.prompt_type=PROMPT \
            prompt.prompt_ver=PROMPT_VERSION
```

```
MODEL_SHORT=[
    "gemini3.5flash",
    "deepseekv4flash",
    "qwen3-32b",
    "qwen3-8b",
    "qwen3-4b",
    "llama3.3-70b",
    "llama3.1-8b",
    "llama3.2-3b",
]
DATA=["constructed", "dialogue", "ludwig"]
LANG=["EN", "ZH"]
PROMPT=["baseline", "cot", "tom"]
PROMPT_VERSION=[0, 1, 2]
```

## Results and human data
`src/results/<model>/` contains the model outputs reported in the paper. In file names, `constructed` appears as `controlled`, `dialogue` as `naturalistic`, and `baseline` as `vanilla`. The four small models (`gemma4`, `mistral`, `smol`, `tinyaya`) were evaluated with the baseline prompt only.

`human_response/` contains the human participant data used in the paper.

---
## Citation
If you find this repository useful, please cite the following paper:

```
@misc{cao2026pilaps,
      title={PILAPS: A Bilingual Benchmark for Evaluating Pragmatic Inference across Phenomena and Settings}, 
      author={Jiani Cao and Anna Korhonen and Chen Cecilia Liu},
      year={2026},
      eprint={2611.25459},
      archivePrefix={arXiv},
      primaryClass={cs.CL},
      url={https://arxiv.org/abs/2611.25459}, 
}
```
