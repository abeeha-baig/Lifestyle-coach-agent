import os
import sys
import streamlit as st
from dotenv import load_dotenv

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.workflow import Workflow

load_dotenv()

workflow = Workflow()

st.set_page_config(page_title="Lifestyle Coach", page_icon="🏃‍♀️")
st.title("💡 Lifestyle Coach Agent")
st.markdown("Enter your **lifestyle goal or challenge** below to receive personalized tips and article insights.")

query = st.text_input("🏃‍♀️ Lifestyle Goal or Challenge")

if query:
    result = workflow.run(query)

    st.markdown(f"## 📋 Personalized Recommendations for: _{query}_")
    st.markdown("---")

    if result.tips:
        st.subheader("🌿 Lifestyle Tips")
        for i, tip in enumerate(result.tips, 1):
            st.markdown(f"**{i}.** {tip.text}")
            if tip.source_url:
                st.markdown(f"🔗 [Source]({tip.source_url})")

    if result.analysis:
        st.subheader("🧠 Article Insights")
        for i, article in enumerate(result.analysis, 1):
            st.markdown(f"### Article {i}: {article.title}")
            st.markdown(f"📝 **Summary:** {article.summary}")
            st.markdown(f"💡 **Key Insights:** {article.key_insights}")
            st.markdown(f"🔗 [Source]({article.url})")

    if result.recommendation:
        st.subheader("🎯 Lifestyle Coach Recommendation")
        st.markdown(f"_{result.recommendation}_")

