#================================
# Part 3: API Integration

#================================
# Task 3.1: Fetch Product Details

# a.fetch all products
# Fetches product data from external API
# Used to enrich internal sales records

import requests


def fetch_all_products():
    """
    This function fetches all products
    from the DummyJSON Products API.

    We use limit=100 to make sure we get
    all available products in one call.
    """

    api_url = "https://dummyjson.com/products?limit=100"
    products_list = []

    try:
        result = requests.get(api_url)

        # If API does not respond correctly
        if result.status_code != 200:
            print("Failed to fetch products from API")
            return products_list

        response_data = result.json()

        if "products" in response_data:
            products_list = response_data["products"]

        print("Successfully fetched products from API")
        return products_list

    except Exception as error:
        # If any error happens (network, API down etc.)
        print("API Error:", error)
        return products_list


#===============================
# b.create_product_mapping
#===============================
# Creates mapping for quick product lookup
# API product ID → category, brand, rating

def create_product_mapping(api_products):
    mapping = {}

    for item in api_products:
        title = item.get("title")
        if not title:
            continue

        clean_title = title.lower().strip()

        mapping[clean_title] = {
            "title": title,                         
            "category": item.get("category"),
            "brand": item.get("brand"),
            "rating": item.get("rating")
        }

    return mapping


