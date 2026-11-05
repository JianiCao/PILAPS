from __future__ import annotations

import re
import logging
import time
from pathlib import Path

import pandas as pd
import hydra
from omegaconf import DictConfig

from datasets import PragmaticsDataset, DataItem
from llm_inference import LLMInferenceEngine
from prompts import PromptType, build_baseline_prompt, build_probe_step1, build_probe_step2

log = logging.getLogger(__name__)

_PROMPT_TYPE_SHORT = {
    "baseline": "vanilla",
    "tom": "tom",
    "cot": "cot",
}

MODEL2FULL: dict[str, str] = {
    "gemini3.5flash": "gemini-3.5-flash",
    "deepseekv4flash": "deepseek-v4-flash",
    "qwen3-32b": "Qwen/Qwen3-32B",
    "qwen3-8b": "Qwen/Qwen3-8B",
    "qwen3-4b": "Qwen/Qwen3-4B-Instruct-2507",
    "llama3.3-70b": "meta-llama/Llama-3.3-70B-Instruct",
    "llama3.1-8b": "meta-llama/Meta-Llama-3-8B-Instruct",
    "llama3.2-3b": "meta-llama/Llama-3.2-3B-Instruct",
}

def parse_answer(text: str) -> int | None:
    m = re.search(r"\b([1-9])\b", str(text))
    return int(m.group(1)) if m else None



def build_results_filename(cfg: DictConfig) -> str:
    model_short = cfg.model.get("short_name", cfg.model.model_name)
    dataset_name = cfg.dataset.dataset_type
    lang = cfg.dataset.language or "all"
    prompt_short = _PROMPT_TYPE_SHORT.get(cfg.prompt.prompt_type, cfg.prompt.prompt_type)
    prompt_ver = cfg.prompt.prompt_ver
    seed = cfg.dataset.shuffle_seed
    return f"{model_short}_{dataset_name}_{lang}_{prompt_short}_v{prompt_ver}_s{seed}.csv"


def run_baseline(engine: LLMInferenceEngine, dataset: PragmaticsDataset,
                 cfg: DictConfig) -> list[dict]:
    prompt_ver = cfg.prompt.prompt_ver
    results = []

    for i, item in enumerate(dataset):
        question = dataset.format_question(item)
        prompt = build_baseline_prompt(item.task, item.language, question, prompt_ver)

        try:
            raw_response = engine.infer(prompt)
        except Exception as e:
            log.error("Inference error item %d: %s", item.item_id, e)
            raw_response = f"ERROR: {e}"

        if cfg.get("debug"):
            print(f"--- DEBUG BASELINE PROMPT ---\n{prompt}\n-----------------------------")
            print(f"--- DEBUG RAW RESPONSE ---\n{raw_response}\n--------------------------")

        parsed = parse_answer(raw_response)
        gold = dataset.get_answer_number(item)

        results.append(build_record(item, raw_response, parsed, gold, dataset))
        log.info("[%d/%d] item=%d parsed=%s gold=%s",
                 i + 1, len(dataset), item.item_id, parsed, gold)
        time.sleep(0.5)

        if cfg.get("debug"):
            break

    return results


def run_probe(engine: LLMInferenceEngine, dataset: PragmaticsDataset,
              cfg: DictConfig) -> list[dict]:
    prompt_type = PromptType(cfg.prompt.prompt_type)
    prompt_ver = cfg.prompt.prompt_ver
    results = []

    for i, item in enumerate(dataset):
        question = dataset.format_question(item)

        step1_prompt = build_probe_step1(question, prompt_type, item.language, prompt_ver)
        try:
            probe_response = engine.infer(step1_prompt)
        except Exception as e:
            log.error("Step1 error item %d: %s", item.item_id, e)
            probe_response = f"ERROR: {e}"

        if cfg.get("debug"):
            print(f"--- DEBUG STEP 1 PROMPT ---\n{step1_prompt}\n---------------------------")
            print(f"--- DEBUG PROBE RESPONSE ---\n{probe_response}\n----------------------------")

        step2_prompt = build_probe_step2(
            item.task, item.language, question, probe_response, prompt_type, prompt_ver,
        )
        try:
            raw_response = engine.infer(step2_prompt)
        except Exception as e:
            log.error("Step2 error item %d: %s", item.item_id, e)
            raw_response = f"ERROR: {e}"

        if cfg.get("debug"):
            print(f"--- DEBUG STEP 2 PROMPT ---\n{step2_prompt}\n---------------------------")
            print(f"--- DEBUG FINAL RESPONSE ---\n{raw_response}\n----------------------------")

        parsed = parse_answer(raw_response)
        gold = dataset.get_answer_number(item)

        record = build_record(item, raw_response, parsed, gold, dataset)
        record["probe_response"] = raw_response.replace("\n", " ")
        results.append(record)

        log.info("[%d/%d] item=%d parsed=%s gold=%s",
                 i + 1, len(dataset), item.item_id, parsed, gold)

        if cfg.get("debug"):
            break

    return results


def build_record(item: DataItem, raw_response: str, parsed: int | None,
                 gold: int, dataset: PragmaticsDataset) -> dict:
    label_cols = [f"Option_{i}_label" for i in range(1, 6)]
    has_labels = any(
        item.original_row.get(c) is not None
        and not pd.isna(item.original_row.get(c))
        and str(item.original_row.get(c)).strip()
        for c in label_cols
    )

    pred_type = None
    gold_type = None
    if has_labels:
        all_labels = []
        for i in range(1, 6):
            v = item.original_row.get(f"Option_{i}_label")
            if v is not None and not pd.isna(v) and str(v).strip():
                all_labels.append(str(v).strip())

        original_answer_idx = int(item.original_row.get("Answer", 0)) - 1
        if 0 <= original_answer_idx < len(all_labels):
            gold_type = all_labels[original_answer_idx]

        if parsed and 1 <= parsed <= len(item.options):
            pred_option_text = item.options[parsed - 1]
            original_options = []
            for c in ["Option_1", "Option_2", "Option_3", "Option_4", "Option_5"]:
                v = item.original_row.get(c)
                if v is not None and not pd.isna(v) and str(v).strip():
                    original_options.append(str(v).strip())

            for j, orig_opt in enumerate(original_options):
                if orig_opt == pred_option_text and j < len(all_labels):
                    pred_type = all_labels[j]
                    break

    return {
        "item_id": item.item_id,
        "task": item.task,
        "language": item.language,
        "raw_output": raw_response.replace("\n", " "),
        "parsed_prediction": parsed,
        "parsed_prediction_type": pred_type,
        "gold_label": gold,
        "gold_label_type": gold_type,
    }


def save_results(results: list[dict], cfg: DictConfig) -> Path:
    results_dir = Path(cfg.output.results_dir) / cfg.model.short_name
    results_dir.mkdir(parents=True, exist_ok=True)

    filename = build_results_filename(cfg)
    out_path = results_dir / filename

    df = pd.DataFrame(results)
    df.to_csv(out_path, index=False)
    log.info("Results saved to %s (%d rows)", out_path, len(df))
    return out_path


@hydra.main(version_base=None, config_path="config", config_name="config")
def main(cfg: DictConfig) -> None:
    cfg.model.model_name = MODEL2FULL.get(cfg.model.short_name, "llama3.1-8b")

    log.info("Loading model: %s (%s)", cfg.model.model_name, cfg.model.backend)
    engine = LLMInferenceEngine(cfg.model)

    log.info("Loading dataset: %s lang=%s", cfg.dataset.dataset_type,
             cfg.dataset.get("language", "all"))
    dataset = PragmaticsDataset(cfg.dataset)
    log.info("Dataset loaded: %d items", len(dataset))

    prompt_type = PromptType(cfg.prompt.prompt_type)

    if prompt_type == PromptType.BASELINE:
        results = run_baseline(engine, dataset, cfg)
    else:
        results = run_probe(engine, dataset, cfg)

    out_path = save_results(results, cfg)
    log.info("Done. Output: %s", out_path)


if __name__ == "__main__":
    main()
