MODELS = {
    "mistral:latest": {
        "prompt_pricing": 0.0015,
        "completion_pricing": 0.002,
        "context_window": 16385,
        "encoding": "cl100k_base"
    },
    "gpt-3.5-turbo": {
        "prompt_pricing": 0.0015,
        "completion_pricing": 0.002,
        "context_window": 16385,
        "encoding": "cl100k_base"
    },
    "gpt-3.5-turbo-16k": {
        "prompt_pricing": 0.003,
        "completion_pricing": 0.004,
        "context_window": 16385,
        "encoding": "cl100k_base"
    },
    "gpt-4": {
        "prompt_pricing": 0.03,
        "completion_pricing": 0.06,
        "context_window": 8192,
        "encoding": "cl100k_base"
    },
    "gpt-4-32k": {
        "prompt_pricing": 0.06,
        "completion_pricing": 0.12,
        "context_window": 32768,
        "encoding": "cl100k_base"
    },
    "gpt-4-turbo": {
        "prompt_pricing": 0.01,
        "completion_pricing": 0.03,
        "context_window": 128000,
        "encoding": "cl100k_base"
    },
}