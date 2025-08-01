import streamlit as st
import pandas as pd
from io import BytesIO
from fpdf import FPDF

# Required parts and quantities
required_parts = {
    "Aft pintle sin": 2,
    "Aft pintle sin nut": 2,
    "Ban link": 4,
    "Bar": 1,
    "Cross link": 1,
    "Cuff": 2
}

# Normalize part descriptions
def normalize(desc):
    return desc.strip().lower()

# Generate report
def generate_report(df):
    df['Desc'] = df['Desc'].astype(str).str.strip()
    df['A/C'] = df['A/C'].astype(str).str.strip()

    grouped = df.groupby(['A/C', 'Desc']).size().reset_index(name='available')
    grouped['Desc'] = grouped['Desc'].apply(normalize)

    report_rows = []
    aircrafts = grouped['A/C'].unique()

    for ac in aircrafts:
        for part, req_qty in required_parts.items():
            part_norm = normalize(part)
            match = grouped[(grouped['A/C'] == ac) & (grouped['Desc'] == part_norm)]

            available_qty = int(match['available'].values[0]) if not match.empty else 0

            if available_qty < req_qty:
                result = 'Less'
            elif available_qty > req_qty:
                result = 'More'
            else:
                result = 'OK'

            report_rows.append({
                'A/C': ac,
                'Desc': part,
                'Required': req_qty,
                'Available': available_qty,
                'Result': result
            })

    return pd.DataFrame(report_rows)

# Excel download
def get_excel_download(report_df):
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        report_df.to_excel(writer, index=False, sheet_name='Inventory Report')
    return output.getvalue()

# PDF download
def get_pdf_download(report_df):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=10)
    pdf.cell(200, 10, txt="Aircraft Inventory Report", ln=True, align='C')
    pdf.ln(10)

    headers = ["A/C", "Desc", "Required", "Available", "Result"]
    for h in headers:
        pdf.cell(38, 10, h, border=1)
    pdf.ln()

    for _, row in report_df.iterrows():
        pdf.cell(38, 10, str(row['A/C']), border=1)
        pdf.cell(38, 10, str(row['Desc']), border=1)
        pdf.cell(38, 10, str(row['Required']), border=1)
        pdf.cell(38, 10, str(row['Available']), border=1)
        pdf.cell(38, 10, str(row['Result']), border=1)
        pdf.ln()

    pdf_output = BytesIO()
    pdf.output(pdf_output)
    return pdf_output.getvalue()

# Sidebar navigation
st.sidebar.title("📌 Navigation")
page = st.sidebar.radio("Go to", ["Upload File", "Full Report", "Imperfect Records", "Search by Aircraft"])

# Upload page
if page == "Upload File":
    st.title("📤 Upload Aircraft Inventory File")
    uploaded_file = st.file_uploader("Upload Excel File", type=["xlsx"])
    if uploaded_file:
        st.session_state['df'] = pd.read_excel(uploaded_file)
        st.success("✅ File uploaded successfully! Now navigate to other pages.")

# Shared logic for other pages
elif page in ["Full Report", "Imperfect Records", "Search by Aircraft"]:
    if 'df' not in st.session_state:
        st.warning("⚠️ Please upload a file first.")
    else:
        report_df = generate_report(st.session_state['df'])

        # Page-specific views
        if page == "Full Report":
            st.title("📋 Full Inventory Report")
            st.dataframe(report_df)

        elif page == "Imperfect Records":
            st.title("⚠️ Imperfect Inventory Records")
            imperfect_df = report_df[report_df['Result'] != 'OK']
            st.dataframe(imperfect_df)

        elif page == "Search by Aircraft":
            st.title("🔍 Search Inventory by Aircraft")
            selected_ac = st.selectbox("Select Aircraft", sorted(report_df['A/C'].unique()))
            filtered_df = report_df[report_df['A/C'] == selected_ac]
            st.dataframe(filtered_df)

        # Download buttons (available on all pages)
        st.markdown("### 📥 Download Report")
        excel_data = get_excel_download(report_df)
        st.download_button(
            label="Download as Excel",
            data=excel_data,
            file_name="inventory_report.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

        pdf_data = get_pdf_download(report_df)
        st.download_button(
            label="Download as PDF",
            data=pdf_data,
            file_name="inventory_report.pdf",
            mime="application/pdf"
        )
