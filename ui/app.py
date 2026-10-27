
import json
import requests
import streamlit as st

API_URL = "http://127.0.0.1:8000/ai-mcp-respones"

st.set_page_config(
    page_title="PC Builder AI",
    page_icon="🖥️",
    layout="wide",
)

st.title("🖥️ PC Builder AI")
st.write("Build your ideal PC with AI-powered component recommendations.")


def format_price(price):
    try:
        return f"₹{float(price):,.0f}"
    except (ValueError, TypeError):
        return str(price) if price is not None else "Price unavailable"


def find_build(data, depth=0):
    """Find the PC build object inside a nested JSON response."""

    if depth > 15:
        return None

    if isinstance(data, dict):
        # Prefer a valid PC build object.
        if isinstance(data.get("parts"), list):
            return data

        # Search nested fields, including strings containing JSON.
        for key in ("result", "data", "output", "content", "text"):
            if key in data:
                result = find_build(data[key], depth + 1)
                if result is not None:
                    return result

        for value in data.values():
            result = find_build(value, depth + 1)
            if result is not None:
                return result

    elif isinstance(data, list):
        for item in data:
            result = find_build(item, depth + 1)
            if result is not None:
                return result

    elif isinstance(data, str):
        try:
            parsed = json.loads(data)
            if parsed != data:
                return find_build(parsed, depth + 1)
        except (json.JSONDecodeError, TypeError):
            pass

    return None


def render_build(build):
    parts = build.get("parts", [])

    total = build.get(
        "total-price-of-the-bulid",
        build.get("total-price-of-the-build", build.get("total_price", 0)),
    )

    st.success("Your PC build is ready!")

    col1, col2 = st.columns(2)
    col1.metric("💰 Total Build Price", format_price(total))
    col2.metric("🧩 Number of Components", len(parts))

    st.divider()
    st.subheader("Your PC Components")

    if not parts:
        st.warning("The agent returned no components.")
        return

    for index, part in enumerate(parts, start=1):
        if not isinstance(part, dict):
            continue

        with st.container(border=True):
            image_col, details_col = st.columns([1, 2], gap="large")

            with image_col:
                image_url = part.get("image", "")

                if isinstance(image_url, str) and image_url.startswith(
                    ("https://", "http://")
                ):
                    st.image(image_url, use_container_width=True)
                else:
                    st.caption("No product image available.")

            with details_col:
                name = part.get(
                    "pc-part-name",
                    part.get("name", f"Component {index}"),
                )

                st.subheader(f"{index}. {name}")
                st.markdown(f"### {format_price(part.get('price'))}")
                st.write(part.get("description", "No description available."))

                link = part.get(
                    "shoping-link",
                    part.get("shopping-link", ""),
                )

                if isinstance(link, str) and link.startswith(
                    ("https://", "http://")
                ):
                    st.link_button("🛒 View Product", link)

    with st.expander("View complete build JSON"):
        st.json(build)


with st.form("pc_build_form"):
    query = st.text_area(
        "Describe the PC you want",
        placeholder="Example: Build a gaming PC under ₹230000",
        height=100,
    )

    submitted = st.form_submit_button(
        "🚀 Generate PC Build",
        use_container_width=True,
    )


if submitted:
    if not query.strip():
        st.warning("Please enter your PC requirements.")
    else:
        try:
            with st.spinner("Your PC Builder Agent is working..."):
                response = requests.post(
                    API_URL,
                    params={"query": query.strip()},
                    timeout=240,
                )

            try:
                data = response.json()
            except ValueError:
                st.error("FastAPI did not return valid JSON.")
                st.code(response.text[:10000])
                st.stop()

            # Find the build even if it is nested in the response.
            build = find_build(data)

            if build is not None:
                if not response.ok:
                    st.warning(
                        f"The API returned HTTP {response.status_code}, "
                        "but included valid build data."
                    )

                # Show a separate warning only if the error is also present.
                error = data.get("error") if isinstance(data, dict) else None
                if error:
                    st.warning(f"Agent warning: {error}")

                render_build(build)

            else:
                st.error(f"API request failed: HTTP {response.status_code}")

                if isinstance(data, dict) and data.get("error"):
                    st.error(data["error"])

                st.write("Raw API response:")
                st.json(data)

        except requests.exceptions.ConnectionError:
            st.error(
                "Cannot connect to FastAPI. "
                "Start your backend on port 8000."
            )

        except requests.exceptions.Timeout:
            st.error("The agent request timed out. Please try again.")

        except requests.exceptions.RequestException as exc:
            st.error(f"Request failed: {exc}")
