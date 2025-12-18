import streamlit as st
import json
import csv
from io import StringIO
from pathlib import Path
from csv_profiler.profiling import profile_rows
from csv_profiler.render import render_markdown

st.set_page_config(page_title="CSV Profiler", layout="centered")
st.title("CSV Profiler")
st.caption("Upload a CSV file to generate a profile report.")

rows_placeholder = st.empty()
report_placeholder = st.empty()

uploaded = st.file_uploader("Upload CSV", type=["csv"])
rows = []

if uploaded:
    try:
        text = uploaded.read().decode("utf-8")
        reader = csv.DictReader(StringIO(text))
        rows = list(reader)
    except Exception as e:
        st.error(f"Cannot read the file: {e}")
        st.stop()

    if not rows:
        st.error("CSV has no rows")
        st.stop()

    if not rows[0].keys():
        st.warning("No headers detected")

if rows:
    if st.checkbox("Show preview of first 5 rows"):
        rows_placeholder.subheader("Preview")
        rows_placeholder.write(rows[:5])

if rows and st.button("Generate report"):
    report = profile_rows(rows)
    st.session_state["report"] = report
    st.rerun()  

if "report" in st.session_state:
    report = st.session_state["report"]

    st.subheader("Report Summary")
    st.write("Rows:", report["n_rows"])
    st.write("Columns:", report["n_cols"])

    md_text = render_markdown(report)
    with st.expander("Markdown Preview"):
        st.markdown(md_text)

    st.subheader("Export")
    report_name = st.text_input("Report Name", value="report")

    st.download_button(
        "Download JSON",
        data=json.dumps(report, indent=2),
        file_name=f"{report_name}.json",
        mime="application/json",
    )

    st.download_button(
        "Download Markdown",
        data=md_text,
        file_name=f"{report_name}.md",
        mime="text/markdown",
    )

    if st.button("Save to outputs/"):
        outputs = Path("outputs")
        outputs.mkdir(exist_ok=True)
        (outputs / f"{report_name}.json").write_text(json.dumps(report, indent=2))
        (outputs / f"{report_name}.md").write_text(md_text)
        st.success(f"Saved to outputs/{report_name}.json and .md")
