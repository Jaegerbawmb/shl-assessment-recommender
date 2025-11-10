import streamlit as st
import requests

st.set_page_config(page_title="SHL Assessment Recommender", layout="wide")
st.title("SHL Assessment Recommender")


api = st.text_input("API base URL", value="http://localhost:8000")
q = st.text_area("Enter JD text or URL", height=180, value="Need a Java developer who can collaborate with external stakeholders.")
k = st.slider("How many results?", 1, 10, 10)

col1, col2 = st.columns(2)

with col1:
    if st.button("Recommend"):
        try:
            r = requests.post(f"{api}/recommend", json={"query": q, "k": k}, timeout=60)
            r.raise_for_status()
            data = r.json()
            st.session_state['results'] = data['recommendations']
        except Exception as e:
            st.error(f"Error: {e}")
with col2:
    st.markdown("**Health Check**")
    try:
        hr = requests.get(f"{api}/health", timeout=10)
        st.json(hr.json())
    except Exception as e:
        st.error(f"Health check failed: {e}")

st.markdown("---")

results = st.session_state.get('results', [])

if results:
    for rec in results:
        with st.container(border=True):
            st.markdown(f"### {rec['name']}")

            st.write(f"**Test Type:** {rec.get('test_type','')}")

            st.write(f"**Score:** {rec.get('score', 0):.3f}")

            st.write(f"**URL:** {rec['url']}")
