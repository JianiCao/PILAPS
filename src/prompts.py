from __future__ import annotations

from enum import Enum


class PromptType(Enum):
    BASELINE = "baseline"
    TOM = "tom"
    COT = "cot"


TASK_INSTRUCTIONS: dict[tuple[str, str], list[str]] = {
    ("Coherence", "EN"): [
        (
            "Task: You will read pair of sentences. "
            "Read each pair and decide whether they form a coherent story. "
            "The answer options are 1 or 2."
        ),
        (
            "Task: Here is a pair of sentences. "
            "Read them and decide whether they form a coherent story. "
            "The answer options are 1 or 2."
        ),
        (
            "Task: Here are some texts."
            "Please read them and decide whether they form a coherent story. "
            "The answer options are 1 or 2."
        ),
    ],
    ("Deceits", "EN"): [
        (
            "Task: You will read short stories that describe two characters "
            "interacting with each other. Each story will be followed by a "
            "multiple-choice question. Read each story and choose the best answer to "
            "each question. Your task is to decide why the character in the story "
            "responds in a certain way. The answer options are 1, 2, 3, or 4."
        ),
        (
            "Task: Here is a short story that describe two characters "
            "interacting with each other. The story will be followed by a "
            "multiple-choice question. Read the story and choose the best answer to "
            "each question. Your task is to decide why the character in the story "
            "responds in a certain way. The answer options are 1, 2, 3, or 4."
        ),
        (
            "Task: Here are some texts that describe two characters "
            "interacting with each other. Read the texts and choose the best answer to "
            "each question. Your task is to decide why the character in the texts "
            "responds in a certain way. The answer options are 1, 2, 3, or 4."
        ),
    ],
    ("Humour", "EN"): [
        (
            "Task: You will read jokes that are missing their punch lines. "
            "A punch line is a funny line that finishes the joke. Each joke will be "
            "followed by five possible endings. Please choose the ending that makes "
            "the joke funny. The answer options are 1, 2, 3, 4, or 5."
        ),
        (
            "Task: Here is a joke that are missing their punch lines. "
            "A punch line is a funny line that finishes the joke. A joke will be "
            "followed by five possible endings. Please choose the ending that makes "
            "the joke funny. The answer options are 1, 2, 3, 4, or 5."
        ),
        (
            "Task: Here are some texts that are missing their punch lines. "
            "A punch line is a funny line that finishes a joke. Please choose the ending that makes "
            "the text funny. The answer options are 1, 2, 3, 4, or 5."
        ),
    ],
    ("IndirectSpeech", "EN"): [
        (
            "Task: You will read short stories that describe everyday situations. "
            "Each story will be followed by a multiple-choice question. "
            "Read each story and choose the best answer. Your task is to decide what "
            "the character in the story is trying to convey. "
            "The answer options are 1, 2, 3, or 4."
        ),
        (
            "Task: Here is a short story that describe everyday situations. "
            "A story will be followed by a multiple-choice question. "
            "Read the story and choose the best answer. Your task is to decide what "
            "the character in the story is trying to convey. "
            "The answer options are 1, 2, 3, or 4."
        ),
        (
            "Task: Here are some texts that describe everyday situations. "
            "Read the texts and choose the best answer. Your task is to decide what "
            "the character in the texts is trying to convey. "
            "The answer options are 1, 2, 3, or 4."
        ),
    ],
    ("Irony", "EN"): [
        (
            "Task: You will read short stories that describe everyday situations. "
            "Each story will be followed by a multiple-choice question. Read each story "
            "and choose the best answer. Your task is to decide what the character in "
            "the story is trying to convey. The answer options are 1, 2, 3, or 4."
        ),
        (
            "Task: Here is a short story that describe everyday situations. "
            "A story will be followed by a multiple-choice question. Read the story "
            "and choose the best answer. Your task is to decide what the character in "
            "the story is trying to convey. The answer options are 1, 2, 3, or 4."
        ),
        (
            "Task: Here are some texts that describe everyday situations. "
            "Read the texts and choose the best answer. Your task is to decide what the character in "
            "the texts is trying to convey. The answer options are 1, 2, 3, or 4."
        ),
    ],
    ("Maxims", "EN"): [
        (
            "Task: You will read short stories that describe everyday situations. "
            "Each story will be followed by a multiple-choice question. Read each story "
            "and choose the best answer. Your task is to decide why the character in the "
            "story responds in a certain way. The answer options are 1, 2, 3, or 4."
        ),
        (
            "Task: Here is a short story that describe everyday situations. "
            "A story will be followed by a multiple-choice question. Read the story "
            "and choose the best answer. Your task is to decide why the character in the "
            "story responds in a certain way. The answer options are 1, 2, 3, or 4."
        ),
        (
            "Task: Here are some texts that describe everyday situations. "
            "Read the texts and choose the best answer. Your task is to decide what the character in "
            "story responds in a certain way. The answer options are 1, 2, 3, or 4."
        ),
    ],
    ("Metaphor", "EN"): [
        (
            "Task: You will read short stories that describe everyday situations. "
            "Each story will be followed by a multiple-choice question. Read each story "
            "and choose the best answer to each question. "
            "The answer options are 1, 2, 3, 4, or 5."
        ),
        (
            "Task: Here is a short story that describe everyday situations. "
            "A story will be followed by a multiple-choice question. Read the story "
            "and choose the best answer to each question. "
            "The answer options are 1, 2, 3, 4, or 5."
        ),
        (
            "Task: Here are some texts that describe everyday situations. "
            "Read the texts and choose the best answer to each question. "
            "The answer options are 1, 2, 3, 4, or 5."
        ),
    ],
    ("Implicature", "EN"): [
        (
            "Task: You will read a short dialogue. A dialogue contains a question "
            "and a response. Your task is to decide what the speaker is implying with their response. Choose the best answer. "
            "The answer options are 1 or 2."
        ),
        (
            "Task: Here is a short dialogue. A dialogue contains a question "
            "and a response. Your task is to decide what the speaker is implying with their response. Choose the best answer. "
            "The answer options are 1 or 2."
        ),
        (
            "Task: Here are some texts."
            "Your task is to decide what the speaker is implying with their response. Choose the best answer. "
            "The answer options are 1 or 2."
        ),
    ],

    ("Coherence", "ZH"): [
        (
            "任务：你将阅读两句话。请阅读每对句子，判断它们是否构成连贯的故事。"
            "答案选项为1或2。"
        ),
        (
            "任务：这里有一对句子。"
            "请阅读它们，判断它们是否构成连贯的故事。"
            "答案选项为1或2。"
        ),
        (
            "任务：这里有一些文本。"
            "请阅读并判断它们是否构成连贯的故事。"
            "答案选项为1或2。"
        ),
    ],
    ("Deceits", "ZH"): [
        (
            "任务：你将阅读描述两个人物互动的短故事。故事后面会有一道选择题。"
            "请阅读故事并选择最佳答案。你的任务是判断故事中的人物为什么如此回应。"
            "答案选项为1、2、3或4。"
        ),
        (
            "任务：这里有一个描述两个人物互动的短故事。故事后面会有一道选择题。"
            "请阅读故事并选择最佳答案。你的任务是判断故事中的人物为什么如此回应。"
            "答案选项为1、2、3或4。"
        ),
        (
            "任务：这里有一些描述两个人物互动的文本。"
            "请阅读文本并选择最佳答案。你的任务是判断故事中的人物为什么如此回应。"
            "答案选项为1、2、3或4。"
        ),
    ],
    ("Humour", "ZH"): [
        (
            "任务：你将阅读缺少妙语结尾的笑话。妙语是使笑话变得有趣的结尾句。"
            "笑话后面会有五个可能的结尾。请选择能使笑话变得有趣的结尾。"
            "答案选项为1、2、3、4或5。"
        ),
        (
            "任务：这里有一个缺少妙语结尾的笑话。妙语是使笑话变得有趣的结尾句。"
            "笑话后面会有五个可能的结尾。请选择能使笑话变得有趣的结尾。"
            "答案选项为1、2、3、4或5。"
        ),
        (
            "任务：这里有一些缺少妙语结尾的文本。妙语是使笑话变得有趣的结尾句。"
            "请选择能使文本变得有趣的结尾。"
            "答案选项为1、2、3、4或5。"
        ),
    ],
    ("IndirectSpeech", "ZH"): [
        (
            "任务：你将阅读描述日常情境的短故事。故事后面会有一道选择题。"
            "请阅读故事并选择最佳答案。你的任务是判断故事中的人物想要表达什么。"
            "答案选项为1、2、3或4。"
        ),
        (
            "任务：这里有一个描述日常情境的短故事。故事后面会有一道选择题。"
            "请阅读故事并选择最佳答案。你的任务是判断故事中的人物想要表达什么。"
            "答案选项为1、2、3或4。"
        ),
        (
            "任务：这里有一些描述日常情境的文本。"
            "请阅读文本并选择最佳答案。你的任务是判断故事中的人物想要表达什么。"
            "答案选项为1、2、3或4。"
        ),
    ],
    ("Irony", "ZH"): [
        (
            "任务：你将阅读描述日常情境的短故事。故事后面会有一道选择题。"
            "请阅读故事并选择最佳答案。你的任务是判断故事中的人物想要表达什么。"
            "答案选项为1、2、3或4。"
        ),
        (
            "任务：这里有一个描述日常情境的短故事。故事后面会有一道选择题。"
            "请阅读故事并选择最佳答案。你的任务是判断故事中的人物想要表达什么。"
            "答案选项为1、2、3或4。"
        ),
        (
            "任务：这里有一些描述日常情境的文本。"
            "请阅读文本并选择最佳答案。你的任务是判断文本中的人物想要表达什么。"
            "答案选项为1、2、3或4。"
        ),
    ],
    ("Maxims", "ZH"): [
        (
            "任务：你将阅读描述日常情境的短故事。故事后面会有一道选择题。"
            "请阅读故事并选择最佳答案。你的任务是判断故事中的人物为什么如此回应。"
            "答案选项为1、2、3或4。"
        ),
        (
            "任务：这里有一个描述日常情境的短故事。故事后面会有一道选择题。"
            "请阅读故事并选择最佳答案。你的任务是判断故事中的人物为什么如此回应。"
            "答案选项为1、2、3或4。"
        ),
        (
            "任务：这里有一些描述日常情境的文本。"
            "请阅读文本并选择最佳答案。你的任务是判断文本中的人物为什么如此回应。"
            "答案选项为1、2、3或4。"
        ),
    ],
    ("Metaphor", "ZH"): [
        (
            "任务：你将阅读描述日常情境的短故事。故事后面会有一道选择题。"
            "请阅读故事并选择最佳答案。答案选项为1、2、3、4或5。"
        ),
        (
            "任务：这里有一个描述日常情境的短故事。故事后面会有一道选择题。"
            "请阅读故事并选择最佳答案。答案选项为1、2、3、4或5。"
        ),
        (
            "任务：这里有一些描述日常情境的文本。"
            "请阅读文本并选择最佳答案。答案选项为1、2、3、4或5。"
        ),
    ],
    ("Implicature", "ZH"): [
        (
            "任务：你将阅读一段简短的对话。一段对话包含一个问题和一个回答。"
            "你的任务是判断说话者的回答暗示了什么。请选出最佳答案。"
            "答案选项为1或2。"
        ),
        (
            "任务：这里有一段简短的对话。对话包含一个问题和一个回答。"
            "你的任务是判断说话者的回答暗示了什么。请选出最佳答案。"
            "答案选项为1或2。"
        ),
        (
            "任务：这里有一些文本。"
            "你的任务是判断说话者的回答暗示了什么。请选出最佳答案。"
            "答案选项为1或2。"
        ),
    ],
}


CLOSING: dict[str, str] = {
    "EN": "Reply with only the number of your answer.",
    "ZH": "请只回复答案对应的数字。",
}


TOM_PROBES: dict[str, list[str]] = {
    "EN": [
        "What's the true intend of the speaker or character? Output reasons only without the answer.",
        "Read the following text carefully and analyze the mental states, such as thoughts, feelings, and perspectives, of the people involved. Output reasons only without the answer.",
        (
            "What does the speaker or character actually think, feel, believe, "
            "want, or intend beyond the literal meaning of what is said? Output reasons only without the answer."
        ),
    ],
    "ZH": [
        "说话者或角色的真实意图是什么？ 仅输出原因，不做回答。",
        "请仔细阅读以下文本，并分析相关人物的心理状态，例如想法、感受和观点。仅输出原因，不做回答",
        "说话者或人物真正的想法、感受、信念、意愿或意图是什么，而非其字面含义？ 仅输出原因，不做回答。",
    ],
}

COT_PROBES: dict[str, list[str]] = {
    "EN": [
        "Think step by step and explain your reasoning. Output reasons only without the answer.",
        "Let's think step by step to understand the text. Output reasons only without the answer.",
        (
            "Think step by step. First, read the full scenario carefully, "
            "paying attention to all the details. Second, consider each "
            "answer option in turn, asking how it relates to the scenario "
            "as a whole. Output reasons only without the answer."
        ),
    ],
    "ZH": [
        "请一步一步思考，说明你的推理过程。仅输出原因，不做回答。",
        "让我们一步一步地思考，来理解这段文字。仅输出原因，不做回答。",
        (
            "请一步一步思考。首先，仔细阅读完整的情境，注意所有细节。"
            "其次，逐一考虑每个答案选项，思考它与整体情境的关系。"
            "仅输出原因，不做回答。"
        ),
    ],
}

PROBE_MAP: dict[PromptType, dict[str, list[str]]] = {
    PromptType.TOM: TOM_PROBES,
    PromptType.COT: COT_PROBES,
}

PROBE_LABELS: dict[PromptType, dict[str, str]] = {
    PromptType.TOM: {
        "EN": "Note on the speaker's intention",
        "ZH": "关于说话者的意图",
    },
    PromptType.COT: {
        "EN": "Reasoning",
        "ZH": "推理过程",
    },
}


_TASK_ALIASES: dict[str, str] = {
    "coherence": "Coherence",
    "deceits": "Deceits",
    "humour": "Humour",
    "humor": "Humour",
    "indirectspeech": "IndirectSpeech",
    "irony": "Irony",
    "maxims": "Maxims",
    "maxim": "Maxims",
    "metaphor": "Metaphor",
    "implicature": "Implicature",
    "ludwig": "Implicature",
}


def _normalize_task(task: str) -> str:
    return _TASK_ALIASES.get(task.lower().strip(), task)


def _pick(versions: list[str], ver: int) -> str:
    if ver < 0 or ver >= len(versions):
        raise ValueError(
            f"prompt_ver={ver} out of range, available: 0..{len(versions) - 1}"
        )
    return versions[ver]


def get_task_instruction(task: str, lang: str, prompt_ver: int = 0) -> str:
    key = (_normalize_task(task), lang.upper())
    versions = TASK_INSTRUCTIONS.get(key)
    if versions is None:
        return (
            "Task: Read the following and choose the best answer."
            if lang.upper() == "EN"
            else "任务：请阅读以下内容并选出最佳答案。"
        )
    return _pick(versions, prompt_ver)


def get_closing(lang: str) -> str:
    return CLOSING[lang.upper()]


def get_probe(prompt_type: PromptType, lang: str, prompt_ver: int = 0) -> str | None:
    probes = PROBE_MAP.get(prompt_type)
    if probes is None:
        return None
    return _pick(probes[lang.upper()], prompt_ver)


def get_probe_label(prompt_type: PromptType, lang: str) -> str:
    labels = PROBE_LABELS.get(prompt_type)
    if labels is None:
        return "Reasoning" if lang.upper() == "EN" else "推理过程"
    return labels[lang.upper()]


def build_baseline_prompt(
    task: str, lang: str, context: str, prompt_ver: int = 0,
) -> str:
    instruction = get_task_instruction(task, lang, prompt_ver)
    closing = get_closing(lang)
    return f"{instruction}\n\n{context}\n\n{closing}"


def build_probe_step1(
    context: str, prompt_type: PromptType, lang: str, prompt_ver: int = 0,
) -> str:
    probe = get_probe(prompt_type, lang, prompt_ver)
    return f"{context}\n\n{probe}"


def build_probe_step2(
    task: str,
    lang: str,
    context: str,
    probe_response: str,
    prompt_type: PromptType,
    prompt_ver: int = 0,
) -> str:
    instruction = get_task_instruction(task, lang, prompt_ver)
    label = get_probe_label(prompt_type, lang)
    closing = get_closing(lang)
    sep = "：" if lang.upper() == "ZH" else ": "
    return f"{instruction}\n\n{context}\n\n{label}{sep}{probe_response}\n\n{closing}"
