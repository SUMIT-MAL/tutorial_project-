import json
from langchain_core.tools import StructuredTool


def compact_result(raw):
    # Parse JSON returned by the MCP tool.
    if isinstance(raw, str):
        try:
            raw = json.loads(raw)
        except json.JSONDecodeError:
            return raw[:4000]

    if isinstance(raw, dict):
        # Some MCP responses may nest the actual result.
        products = (
            raw.get("products")
            or raw.get("results")
            or raw.get("items")
        )

        if isinstance(products, list):
            compact_products = []

            for p in products[:1]:
                if not isinstance(p, dict):
                    continue

                price = p.get("price")
                if isinstance(price, dict):
                    currency = price.get("currency")
                    price = price.get("selling_price", price.get("amount"))
                else:
                    currency = p.get("currency")

                compact_products.append({
                    "title": p.get("title"),
                    "brand": p.get("brand"),
                    "price": price,
                    "currency": currency,
                    "url": p.get("url"),
                    "image": p.get("image"),
                    "in_stock": p.get("in_stock"),
                    "key_specs": (p.get("key_specs") or [])[:4],
                })

            # Deliberately discard the large "filters" array.
            return json.dumps(
                {
                    "search_query": raw.get("search_query"),
                    "products": compact_products,
                },
                ensure_ascii=False,
                separators=(",", ":"),
            )

    # Keep other response formats bounded.
    return json.dumps(raw, ensure_ascii=False)[:4000]


def wrap_mcp_tool(original_tool):
    async def call_mcp(**kwargs):
        result = await original_tool.ainvoke(kwargs)
        return compact_result(result)

    return StructuredTool(
        name=original_tool.name,
        description=original_tool.description,
        args_schema=original_tool.args_schema,
        coroutine=call_mcp,
    )
