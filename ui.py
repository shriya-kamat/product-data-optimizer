import streamlit as st
import json
from utils import detect_issues, improve_product, evaluate_product, sync_to_woocommerce
from database import insert_product, get_all_products


st.set_page_config(page_title="Product Optimizer", layout="wide")

st.title("🧠 Product Data Optimizer")
st.markdown("### Improve your product data using AI")

# 🎯 Input Section
st.markdown("## 📥 Enter Product Details")

col1, col2 = st.columns(2)

with col1:
    name = st.text_input("Product Name")

with col2:
    category = st.text_input("Category")

description = st.text_area("Description")

# 🚀 Analyze Button
if st.button("🚀 Analyze Product"):

    product = {
        "name": name,
        "description": description,
        "category": category,
        "attributes": {}
    }

    # ⏳ Loading spinner
    with st.spinner("Analyzing with AI..."):

        issues = detect_issues(product)

        improved = improve_product(product)

        insert_product(product, improved)

    # 🔴 Issues Section
    st.markdown("## ⚠️ Issues Detected")

    if issues:
        for issue in issues:
            st.error(issue)
    else:
        st.success("No issues found 🎉")

    # 🔄 Before vs After
    st.markdown("## 🔄 Before vs After")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### ❌ Before")
        st.json(product)

    with col2:
        st.markdown("### ✅ After")
        st.json(improved)

        if st.button("📦 Sync to WooCommerce"):
            result = sync_to_woocommerce(improved)

            st.success(result["message"])
            st.write(f"Product ID: {result['product_id']}")

        st.info("🔗 Simulating WooCommerce API sync")

    evaluation = evaluate_product(improved)

    st.subheader("🧠 AI Evaluation")
    st.write(f"Score: {evaluation['score']}/100")
    st.write(f"Feedback: {evaluation['feedback']}")

    st.info("Rule-based score shows completeness, while AI evaluation checks quality and depth.")

    #Score Section
    def score(p):
        s = 0
        if p["name"]: s += 1
        if len(p["description"]) > 20: s += 1
        if p["category"]: s += 1
        if p["attributes"]: s += 1
        return int((s/4)*100)

    st.markdown("## 📊 Data Quality Score")

    before_score = score(product)
    after_score = score(improved)

    st.progress(before_score / 100)
    st.write(f"Before: {before_score}%")

    st.progress(after_score / 100)
    st.write(f"After: {after_score}%")


    st.markdown("## 📦 Stored Products")

# Button
show = st.button("📦 View Stored Products")

# Display logic
if show:
    products = get_all_products()

    import json

    if not products:
        st.warning("No products stored yet")
    else:
        st.success(f"Found {len(products)} products")

        for p in products:
            st.write(f"Product ID: {p[0]}")

            st.json({
                "original": json.loads(p[1]),
                "improved": json.loads(p[2])
            })