"""Public list prices for the LLM API cost calculator, USD per 1M tokens, standard (non-batch) tier.

Every number below was read on 2026-11-01 from the provider's official pricing page listed in SOURCES.
Do not add a model unless you read its price on the official page the same day. Update AS_OF when you re-check.
Fields: in = input, out = output, cached = cached-input / cache-hit price (None if the provider publishes none),
long = higher rates applied when input tokens per request exceed `over` (None if the page lists no such tier).
"""
AS_OF = "2026-11-01"

SOURCES = {
    "OpenAI": "https://developers.openai.com/api/docs/pricing",
    "Anthropic": "https://platform.claude.com/docs/en/about-claude/pricing",
    "Google Gemini": "https://ai.google.dev/gemini-api/docs/pricing",
    "DeepSeek": "https://api-docs.deepseek.com/quick_start/pricing",
    "Mistral": "https://mistral.ai/pricing/api",
}

NOTES = {
    "OpenAI": "Standard tier. Short context is up to 272K input tokens; above that the page lists long-context rates, applied here automatically. Cache-write prices are not modeled.",
    "Anthropic": "Cached price is the cache hit and refresh rate. Cache writes cost more than base input (1.25x for 5 minute writes) and are not modeled. Haiku 5.5 prompts over 100,000 tokens use its higher rates.",
    "Google Gemini": "Paid tier, standard. Context caching storage per hour is not modeled. Some rates are introductory and the page lists the date they change.",
    "DeepSeek": "Peak-hour rates. The page says off-peak rates are half of these. Cached price is the cache-hit input rate.",
    "Mistral": "Standard tier, USD, global inference.",
}

L = lambda over, i, o, c: {"over": over, "in": i, "out": o, "cached": c}

MODELS = [
    # OpenAI, standard pricing table
    ("gpt-6-astra", "OpenAI", "GPT-6 Astra", 10.00, 50.00, 1.00, L(272000, 20.00, 75.00, 2.00), ""),
    ("gpt-6.1-sol", "OpenAI", "GPT-6.1 Sol", 2.00, 10.00, 0.10, L(272000, 4.00, 15.00, 0.20), ""),
    ("gpt-6.1-terra", "OpenAI", "GPT-6.1 Terra", 1.00, 5.00, 0.05, L(272000, 2.00, 7.50, 0.10), ""),
    ("gpt-6-luna", "OpenAI", "GPT-6 Luna", 0.10, 0.50, 0.01, L(272000, 0.20, 0.75, 0.02), ""),
    ("gpt-5.5", "OpenAI", "GPT-5.5", 5.00, 30.00, 0.50, L(272000, 10.00, 45.00, 1.00), ""),
    ("gpt-5.4", "OpenAI", "GPT-5.4", 2.50, 15.00, 0.25, L(272000, 5.00, 22.50, 0.50), ""),
    ("gpt-5.4-mini", "OpenAI", "GPT-5.4 mini", 0.75, 4.50, 0.075, None, ""),
    ("gpt-5-mini", "OpenAI", "GPT-5 mini", 0.25, 2.00, 0.025, None, ""),
    ("gpt-4.1-mini", "OpenAI", "GPT-4.1 mini", 0.40, 1.60, 0.10, None, ""),
    ("gpt-4o-mini", "OpenAI", "GPT-4o mini", 0.15, 0.60, 0.075, None, ""),
    # Anthropic, model pricing table (base input, cache hits and refreshes, output)
    ("claude-fable-5.1", "Anthropic", "Claude Fable 5.1", 10.00, 50.00, 0.25, None, ""),
    ("claude-opus-5.5", "Anthropic", "Claude Opus 5.5", 4.00, 20.00, 0.20, None, ""),
    ("claude-opus-5", "Anthropic", "Claude Opus 5", 5.00, 25.00, 0.50, None, ""),
    ("claude-sonnet-5.5", "Anthropic", "Claude Sonnet 5.5", 2.00, 10.00, 0.10, None, ""),
    ("claude-sonnet-5", "Anthropic", "Claude Sonnet 5", 2.00, 10.00, 0.20, None, ""),
    ("claude-sonnet-4.6", "Anthropic", "Claude Sonnet 4.6", 3.00, 15.00, 0.30, None, ""),
    ("claude-haiku-5.5", "Anthropic", "Claude Haiku 5.5", 0.10, 0.50, 0.01, L(100000, 0.50, 2.50, 0.05), ""),
    ("claude-haiku-4.5", "Anthropic", "Claude Haiku 4.5", 1.00, 5.00, 0.10, None, ""),
    # Google Gemini API, paid tier, standard
    ("gemini-4-argon", "Google Gemini", "Gemini 4 Argon", 2.00, 10.00, 0.10, None, "Introductory rate through Nov 30, 2026; the page lists $4.00 input, $20.00 output from Dec 1, 2026."),
    ("gemini-3.8-flash", "Google Gemini", "Gemini 3.8 Flash", 0.75, 3.75, 0.075, None, "Rate through Dec 31, 2026; the page lists $1.50 input, $7.50 output from Jan 1, 2027."),
    ("gemini-3.5-flash-lite", "Google Gemini", "Gemini 3.5 Flash-Lite", 0.30, 2.50, 0.03, None, ""),
    ("gemini-3.1-pro-preview", "Google Gemini", "Gemini 3.1 Pro Preview", 2.00, 12.00, 0.20, L(200000, 4.00, 18.00, 0.40), ""),
    ("gemini-2.5-pro", "Google Gemini", "Gemini 2.5 Pro", 1.25, 10.00, 0.125, L(200000, 2.50, 15.00, 0.25), ""),
    ("gemini-2.5-flash", "Google Gemini", "Gemini 2.5 Flash", 0.30, 2.50, 0.03, None, "Text, image and video input rate."),
    ("gemini-2.5-flash-lite", "Google Gemini", "Gemini 2.5 Flash-Lite", 0.10, 0.40, 0.01, None, "Text, image and video input rate."),
    # DeepSeek, peak rates
    ("deepseek-flash", "DeepSeek", "DeepSeek V4.1 Flash (deepseek-flash)", 0.30, 1.20, 0.006, None, "Peak rate; off-peak is $0.15 input, $0.60 output."),
    ("deepseek-v4-pro", "DeepSeek", "DeepSeek V4 Pro", 1.32, 3.96, 0.044, None, "Peak rate; off-peak is $0.66 input, $1.98 output."),
    # Mistral, API pricing page, standard
    ("mistral-large-4", "Mistral", "Mistral Large 4", 0.70, 2.10, 0.07, None, ""),
    ("mistral-small-4", "Mistral", "Mistral Small 4", 0.15, 0.60, 0.015, None, ""),
    ("ministral-3-8b", "Mistral", "Ministral 3 8B", 0.15, 0.15, 0.015, None, ""),
]


def as_json():
    return [{"id": i, "p": p, "name": n, "in": a, "out": b, "cached": c, "long": lg, "note": note} for i, p, n, a, b, c, lg, note in MODELS]
