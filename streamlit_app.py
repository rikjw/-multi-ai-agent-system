import os

# --- PRE-IMPORT GUARD ---
os.environ["OTEL_SDK_DISABLED"] = "true"
os.environ["CREWAI_TELEMETRY_OPT_OUT"] = "true"
os.environ["CREWAI_DISABLE_TELEMETRY"] = "true"

import streamlit as st
from crew import ResearchCrew
from fpdf import FPDF
from dotenv import load_dotenv

load_dotenv()

# Key Mapping
for key in ["OPENAI_API_KEY", "SERPER_API_KEY"]:
    if key in st.secrets:
        os.environ[key] = st.secrets[key]


def create_pdf(text):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("helvetica", size=12)
    clean_text = text.encode("latin-1", "replace").decode("latin-1")
    pdf.multi_cell(0, 10, text=clean_text)
    return pdf.output()


st.set_page_config(page_title="AI Research Pro", layout="wide")
st.title("🤖 Agentic Research Newsroom")

topic = st.text_input(
    "What is your research goal?", placeholder="e.g., 2026 AI developments"
)

if st.button("Run Agents"):
    if not topic:
        st.warning("Please enter a research topic.")
    elif not os.getenv("OPENAI_API_KEY") or not os.getenv("SERPER_API_KEY"):
        st.error("Missing API Keys! Check your secrets.toml or .env.")
    else:
        with st.status("🛠️ Agents are collaborating...", expanded=True) as status:
            try:
                result = ResearchCrew().crew().kickoff(inputs={"topic": topic})
                report_content = str(result.raw)
                status.update(label="✅ Success!", state="complete", expanded=False)

                st.subheader("Final Report")
                st.markdown(report_content)

                pdf_bytes = create_pdf(report_content)
                st.download_button(
                    label="📥 Download PDF",
                    data=bytes(pdf_bytes),
                    file_name="research_report.pdf",
                    mime="application/pdf",
                )
            except Exception as e:
                st.error(f"Error: {e}")
