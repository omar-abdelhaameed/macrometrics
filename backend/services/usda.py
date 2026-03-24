"""
USDA FoodData Central API service layer.
Uses the FDC REST API to search and retrieve food nutrition data.
Docs: https://fdc.nal.usda.gov/api-guide
"""
import os
import logging
import httpx
from typing import Optional

logger = logging.getLogger("macrometrics.usda")

USDA_API_KEY = os.getenv("NUTRITION_API_KEY", "DEMO_KEY")
USDA_BASE_URL = "https://api.nal.usda.gov/fdc/v1"


def _parse_search_nutrients(food: dict) -> dict:
    """Safely extract nutrient values from a search-result food item."""
    nutrients = {}
    for n in food.get("foodNutrients", []):
        name = n.get("nutrientName", "")
        value = n.get("value")
        if name and value is not None:
            nutrients[name] = value
    return nutrients


async def search_foods(query: str, page_size: int = 15) -> list[dict]:
    """Search USDA FoodData Central for foods matching query."""
    logger.info(f"USDA search: query='{query}', page_size={page_size}, key={'SET' if USDA_API_KEY != 'DEMO_KEY' else 'DEMO'}")

    try:
        async with httpx.AsyncClient(timeout=20.0) as client:
            resp = await client.get(
                f"{USDA_BASE_URL}/foods/search",
                params={
                    "api_key": USDA_API_KEY,
                    "query": query,
                    "pageSize": page_size,
                    "dataType": "Foundation,SR Legacy",
                },
                headers={
                    "Content-Type": "application/json",
                    "Accept": "application/json",
                },
            )

        if resp.status_code == 403:
            logger.error(f"USDA API key rejected (403). Key prefix: {USDA_API_KEY[:6]}...")
            raise ValueError("USDA API key is invalid or expired. Check NUTRITION_API_KEY in .env")

        if resp.status_code == 429:
            logger.warning("USDA API rate limit reached (429)")
            raise ValueError("USDA API rate limit reached. Please wait a moment and try again.")

        if resp.status_code >= 400:
            logger.error(f"USDA API error: HTTP {resp.status_code} — {resp.text[:200]}")
            raise ValueError(f"USDA API returned HTTP {resp.status_code}")

        data = resp.json()

    except httpx.TimeoutException:
        logger.error("USDA API request timed out after 20s")
        raise ValueError("Nutrition database request timed out. Please try again.")
    except httpx.ConnectError:
        logger.error("Cannot connect to USDA API (network error)")
        raise ValueError("Cannot reach the nutrition database. Check your internet connection.")
    except ValueError:
        raise  # Re-raise our own ValueErrors
    except Exception as e:
        logger.exception(f"Unexpected error calling USDA API: {e}")
        raise ValueError(f"Unexpected error contacting nutrition database: {str(e)}")

    results = []
    for food in data.get("foods", []):
        try:
            nutrients = _parse_search_nutrients(food)
            results.append({
                "fdc_id": str(food.get("fdcId", "")),
                "name": food.get("description", "Unknown"),
                "category": food.get("foodCategory", "General"),
                "calories_per_100g": round(nutrients.get("Energy", 0), 1),
                "protein_per_100g": round(nutrients.get("Protein", 0), 1),
                "carbs_per_100g": round(nutrients.get("Carbohydrate, by difference", 0), 1),
                "fats_per_100g": round(nutrients.get("Total lipid (fat)", 0), 1),
                "fiber_per_100g": round(nutrients.get("Fiber, total dietary", 0), 1),
                "source": "USDA FDC",
            })
        except Exception as e:
            logger.warning(f"Skipping malformed food item: {e}")
            continue

    logger.info(f"USDA search returned {len(results)} results for '{query}'")
    return results


async def get_food_detail(fdc_id: str) -> Optional[dict]:
    """Get detailed nutrition info for a specific food by FDC ID."""
    logger.info(f"USDA detail fetch: fdc_id={fdc_id}")

    try:
        async with httpx.AsyncClient(timeout=20.0) as client:
            resp = await client.get(
                f"{USDA_BASE_URL}/food/{fdc_id}",
                params={"api_key": USDA_API_KEY},
                headers={"Accept": "application/json"},
            )

        if resp.status_code == 404:
            logger.warning(f"Food not found: fdc_id={fdc_id}")
            return None

        if resp.status_code >= 400:
            logger.error(f"USDA detail error: HTTP {resp.status_code}")
            raise ValueError(f"USDA API returned HTTP {resp.status_code}")

        food = resp.json()

    except httpx.TimeoutException:
        logger.error(f"USDA detail request timed out for fdc_id={fdc_id}")
        raise ValueError("Nutrition database request timed out")
    except ValueError:
        raise
    except Exception as e:
        logger.exception(f"Unexpected error fetching food detail: {e}")
        raise ValueError(f"Unexpected error: {str(e)}")

    nutrients = {}
    for n in food.get("foodNutrients", []):
        nutrient_info = n.get("nutrient", {})
        name = nutrient_info.get("name", "")
        value = n.get("amount", 0)
        if name:
            nutrients[name] = value

    category = food.get("foodCategory", "General")
    if isinstance(category, dict):
        category = category.get("description", "General")

    return {
        "fdc_id": str(food.get("fdcId", "")),
        "name": food.get("description", "Unknown"),
        "category": category,
        "calories_per_100g": round(nutrients.get("Energy", 0), 1),
        "protein_per_100g": round(nutrients.get("Protein", 0), 1),
        "carbs_per_100g": round(nutrients.get("Carbohydrate, by difference", 0), 1),
        "fats_per_100g": round(nutrients.get("Total lipid (fat)", 0), 1),
        "fiber_per_100g": round(nutrients.get("Fiber, total dietary", 0), 1),
        "sugar_per_100g": round(nutrients.get("Sugars, total including NLEA", 0), 1),
        "sodium_mg_per_100g": round(nutrients.get("Sodium, Na", 0), 1),
        "source": "USDA FDC",
    }
