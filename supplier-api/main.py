import os
import uuid
from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel
from mangum import Mangum

app = FastAPI(title="Sneaker Supplier API", version="1.0.0")

# ── Auth ─────────────────────────────────────────────
# Node equivalent: an Express middleware checking req.headers['x-api-key'].
# In FastAPI it's a plain function; endpoints call it explicitly.
API_KEY = os.getenv("SUPPLIER_API_KEY", "dev-secret-key")

def require_api_key(x_api_key: str | None):
    if x_api_key != API_KEY:
        # Like res.status(401).json(...) + return in Express,
        # but raised as an exception — FastAPI turns it into the response.
        raise HTTPException(status_code=401, detail="Invalid or missing API key")

# ── "Database" ───────────────────────────────────────
# Plain dict = JS object literal. REPLACE keys with your real sku values!
SUPPLIER_CATALOG = {
    "NK-AM90-001": {
        "name": "Air Max 90",
        "brand": "Nike",
        "unit_price": 750.00,   # NOK, wholesale
        "variants": [
            {"size": "41", "colour": "White/Grey", "available": 120},
            {"size": "44", "colour": "Black/Black", "available": 80},
        ],
    },
    "AD-UB22-001": {
        "name": "Ultraboost 22",
        "brand": "Adidas",
        "unit_price": 1099.00,
        "variants": [
            {"size": "40", "colour": "Core Black", "available": 60},
            {"size": "42", "colour": "Core Black", "available": 0},  # deliberately out of stock
        ],
    },
}

# ── Request body schema ──────────────────────────────
# Pydantic model = your Module 2 structured-output trick, reversed:
# there it validated the LLM's output; here it validates incoming JSON.
# Express needs a library (joi/zod) for this; FastAPI has it built in.
class OrderRequest(BaseModel):
    sku: str
    size: str
    colour: str
    quantity: int

# ── Endpoints ────────────────────────────────────────
@app.get("/products/{sku}")
def get_product(sku: str, x_api_key: str | None = Header(default=None)):
    # Decorator ≈ app.get('/products/:sku', handler); {sku} ≈ req.params.sku.
    # Header(default=None) tells FastAPI to read the x-api-key header into that arg.
    require_api_key(x_api_key)
    product = SUPPLIER_CATALOG.get(sku)   # dict.get ≈ obj[sku], but None if absent
    if product is None:
        raise HTTPException(status_code=404, detail=f"SKU {sku} not found")
    return {"sku": sku, **product}        # ** = JS spread: {sku, ...product}

@app.post("/orders")
def place_order(order: OrderRequest, x_api_key: str | None = Header(default=None)):
    require_api_key(x_api_key)

    # STEP 1 — does the SKU exist? (fixed: order.sku, not sku)
    product = SUPPLIER_CATALOG.get(order.sku)
    if product is None:
        raise HTTPException(status_code=404, detail=f"SKU {order.sku} not found")
    
    # STEP 2 — find the variant that matches size AND colour.
    matching_variant = None
    for variant in product["variants"]:
        if variant["size"] == order.size and variant["colour"] == order.colour:
            matching_variant = variant
            break
    if matching_variant is None:
        raise HTTPException(status_code=404, detail=f"Variant not sold: {order.sku} size {order.size} in {order.colour}")

    # STEP 3 — enough stock?
    if matching_variant["available"] < order.quantity:
        raise HTTPException(status_code=400, detail=f"Only {matching_variant['available']} units available, you asked for {order.quantity}")

    # STEP 4 — success. Replace the placeholder return.
    order_id = f"ORD-{uuid.uuid4().hex[:8].upper()}"
    return {
        "order_id": order_id,
        "sku": order.sku,
        "size": order.size,
        "colour": order.colour,
        "quantity": order.quantity,
        "unit_price": product["unit_price"],
        "total_cost": product["unit_price"] * order.quantity,
    }

# Lambda adapter for later — translates Lambda events into requests the app understands.
handler = Mangum(app)
