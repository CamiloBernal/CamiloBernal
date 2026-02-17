import json
import os
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

CACHE_FILE = "src/assets/json/cache.json"

def load_cache():
    """Loads the cache from the JSON file."""
    if os.path.exists(CACHE_FILE):
        try:
            with open(CACHE_FILE, 'r', encoding='utf-8') as f:
                content = f.read()
                if not content:
                    return {}
                return json.loads(content)
        except json.JSONDecodeError:
            logger.error("Cache file is corrupt. Returning empty dict.")
            return {}
        except Exception as e:
            logger.error(f"Error reading cache: {e}")
            return {}
    return {}

def save_cache(data):
    """Saves the given data to the cache JSON file."""
    try:
        os.makedirs(os.path.dirname(CACHE_FILE), exist_ok=True)
        with open(CACHE_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        logger.info("Cache saved successfully.")
    except Exception as e:
        logger.error(f"Failed to save cache: {e}")

def safe_execute(func, fallback_key, cache, *args, **kwargs):
    """
    Executes a function. If it fails, tries to load from cache using fallback_key.
    If successful, updates cache[fallback_key].
    Returns the result.
    """
    try:
        result = func(*args, **kwargs)
        if result is not None:
             cache[fallback_key] = result
        return result
    except Exception as e:
        logger.error(f"Error executing {func.__name__}: {e}")
        if fallback_key in cache:
            logger.info(f"Using cached data for {fallback_key}")
            return cache[fallback_key]
        else:
            logger.warning(f"No cache found for {fallback_key}. Returning default empty value.")
            # Return appropriate empty type based on expectation?
            # For now return [] as most things are lists, or let the caller handle None.
            # But the template expects lists usually.
            return []
