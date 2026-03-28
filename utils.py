from groq import Groq
import json

def detect_issues(product):
    issues = []

    if not product.get("category"):
        issues.append("Missing category")

    if len(product.get("description", "")) < 20:
        issues.append("Description too short")

    if "attributes" not in product or not product["attributes"]:
        issues.append("Missing attributes")

    return issues

client = Groq(api_key="")

def improve_product(product):
    print("🚀 Calling Groq...")

    prompt = f"""
You are an AI that improves e-commerce product data.

Given the product:
{product}

Fill missing fields and improve description.

Return ONLY valid JSON. No explanation.

Format:
{{
  "name": "...",
  "description": "...",
  "category": "...",
  "attributes": {{
    "material": "...",
    "size": "..."
  }}
}}
"""

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",  
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        print("✅ Got response")

        result = response.choices[0].message.content.strip()

        #Clean JSON safely
        start = result.find("{")
        end = result.rfind("}") + 1
        result = result[start:end]

        improved = json.loads(result)

        return improved

    except Exception as e:
        print("❌ Error in AI:", e)
        return product
    
def evaluate_product(product):
    prompt = f"""
    Evaluate the quality of this product data.

    Product:
    {product}

    Give a score out of 100 and a short reason.

    Return JSON:
    {{
        "score": number,
        "feedback": "..."
    }}
    """

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        result = response.choices[0].message.content.strip()

        start = result.find("{")
        end = result.rfind("}") + 1
        result = result[start:end]

        return json.loads(result)

    except:
        return {"score": 50, "feedback": "Evaluation failed"}
    
def sync_to_woocommerce(product):
    return {
        "status": "success",
        "message": "Product synced to WooCommerce",
        "product_id": 1001
    }