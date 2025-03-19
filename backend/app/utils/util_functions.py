import tiktoken
from typing import Union
from app.utils.constants import MODELS
from typing import Dict, List, Union, Optional

def calculate_unit_price(prompt_tokens, completion_tokens, used_model):
    return (
        (MODELS[used_model]["prompt_pricing"] * prompt_tokens)
        + (MODELS[used_model]["completion_pricing"] * completion_tokens)
    ) / 1000

def count_tokens(text: str, model_name: str) -> int:
    """
    Count the number of tokens in a text string for a specific model.
    
    Args:
        text: The text to count tokens for
        model_name: The name of the model to use
    
    Returns:
        The number of tokens in the text
    """
    if model_name not in MODELS:
        raise ValueError(f"Unknown model: {model_name}")
    
    # Get the encoding for the model
    encoding_name = MODELS[model_name]["encoding"]
    try:
        encoding = tiktoken.get_encoding(encoding_name)
    except KeyError:
        # Fallback to cl100k_base for newer models
        encoding = tiktoken.get_encoding("cl100k_base")
    
    # Count tokens
    token_count = len(encoding.encode(text))
    return token_count

def calculate_price(
    prompt_tokens: int, 
    completion_tokens: int, 
    model_name: str
) -> float:
    """
    Calculate the price for a given number of tokens.
    
    Args:
        prompt_tokens: Number of tokens in the prompt
        completion_tokens: Number of tokens in the completion
        model_name: The name of the model to use
    
    Returns:
        The price in USD
    """
    if model_name not in MODELS:
        raise ValueError(f"Unknown model: {model_name}")
    
    return (
        (MODELS[model_name]["prompt_pricing"] * prompt_tokens)
        + (MODELS[model_name]["completion_pricing"] * completion_tokens)
    ) / 1000

def calculate_price_from_text(
    prompt_text: str, 
    completion_text: str, 
    model_name: str
) -> Dict[str, Union[int, float]]:
    """
    Calculate the price for a given prompt and completion.
    
    Args:
        prompt_text: The prompt text
        completion_text: The completion text
        model_name: The name of the model to use
    
    Returns:
        Dictionary with token counts and price
    """
    prompt_tokens = count_tokens(prompt_text, model_name)
    completion_tokens = count_tokens(completion_text, model_name)
    
    price = calculate_price(prompt_tokens, completion_tokens, model_name)
    
    return {
        "prompt_tokens": prompt_tokens,
        "completion_tokens": completion_tokens,
        "total_tokens": prompt_tokens + completion_tokens,
        "price_usd": price
    }

def calculate_price_for_tracing(
    model_name: str,
    input_text: str,
    output_text: str
) -> Optional[Dict[str, Union[int, float]]]:
    """
    Calculate the price directly from input and output text.
    
    Args:
        model_name: The name of the model to use
        input_text: The input text
        output_text: The output text
    
    Returns:
        Dictionary with token counts and price, or None if input is invalid
    """
    # Ensure input and output are strings
    if not isinstance(input_text, str):
        input_text = str(input_text)
    if not isinstance(output_text, str):
        output_text = str(output_text)
    
    # Calculate price
    return calculate_price_from_text(input_text, output_text, model_name)
