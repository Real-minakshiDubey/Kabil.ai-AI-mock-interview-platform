# ml_workflow/utils.py

def normalize_text(text: str) -> str:
    """Simple cleaning for ML models."""
    return text.strip().lower()

def safe_run(fn, *args, **kwargs):
    """Runs any ML component safely and catches errors."""
    try:
        return fn(*args, **kwargs)
    except Exception as e:
        return {"error": str(e)}
