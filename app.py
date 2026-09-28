import streamlit as st
import requests
from docx import Document
from fpdf import FPDF


# --------------------------------------------------
# PAGE SETTINGS
# --------------------------------------------------

st.set_page_config(
    page_title="LegalEase",
    page_icon="⚖️",
    layout="wide"
)


# --------------------------------------------------
# TITLE
# --------------------------------------------------

st.title("⚖️ LegalEase")

st.subheader("AI-Powered Legal Document Generator")

st.write(
    "Generate, edit and download professional legal documents."
)


# --------------------------------------------------
# INPUT SECTION
# --------------------------------------------------

st.header("Document Details")

document_type = st.text_input(
    "Document Type",
    placeholder="Example: Employment Contract"
)

parties = st.text_area(
    "Parties Involved",
    placeholder="Example: ABC Technologies Pvt. Ltd. and Rahul Kumar"
)

terms = st.text_area(
    "Terms and Conditions",
    placeholder="Example: Job Role: Software Developer\nSalary: Rs. 30,000 per month\nWorking Hours: 9 AM to 5 PM"
)

effective_date = st.text_input(
    "Effective Date",
    placeholder="Example: 01-10-2026"
)


# --------------------------------------------------
# GENERATE DOCUMENT
# --------------------------------------------------

if st.button("Generate Document"):

    if not document_type or not parties or not terms or not effective_date:

        st.warning("Please fill in all the fields.")

    else:

        data = {
            "document_type": document_type,
            "parties": parties,
            "terms": terms,
            "dates": effective_date
        }

        try:

            with st.spinner("Generating legal document..."):

                response = requests.post(
                    "http://127.0.0.1:8000/generate",
                    json=data,
                    timeout=120
                )


            # ------------------------------------------
            # SUCCESS
            # ------------------------------------------

            if response.status_code == 200:

                result = response.json()

                document = result["document"]

                st.session_state["document"] = document

                st.success("Document generated successfully!")


            # ------------------------------------------
            # GEMINI QUOTA ERROR
            # ------------------------------------------

            elif response.status_code == 429:

                st.error(
                    "Gemini API quota has been exceeded. "
                    "Please wait until the quota resets before generating another document."
                )


            # ------------------------------------------
            # OTHER SERVER ERROR
            # ------------------------------------------

            else:

                try:

                    error = response.json()

                    st.error(
                        error.get(
                            "detail",
                            "Failed to generate document."
                        )
                    )

                except Exception:

                    st.error(
                        "Failed to generate document."
                    )


        except requests.exceptions.ConnectionError:

            st.error(
                "Cannot connect to FastAPI. "
                "Make sure Uvicorn is running."
            )


        except requests.exceptions.Timeout:

            st.error(
                "The request took too long. Please try again later."
            )


        except Exception as e:

            st.error(
                "An unexpected error occurred."
            )

            st.write(str(e))


# --------------------------------------------------
# DOCUMENT EDITOR
# --------------------------------------------------
if "document" not in st.session_state:
    st.session_state["document"]="legal ease simple document for testing."
if "document" in st.session_state:

    st.header("Document Preview and Editing")

    edited_document = st.text_area(
        "Edit Document",
        value=st.session_state["document"],
        height=600
    )


    # --------------------------------------------------
    # DOWNLOAD TXT
    # --------------------------------------------------

    st.download_button(
        "Download TXT",
        data=edited_document,
        file_name="LegalEase_Document.txt",
        mime="text/plain"
    )


    # --------------------------------------------------
    # CREATE DOCX
    # --------------------------------------------------

    doc = Document()

    for paragraph in edited_document.split("\n"):

        doc.add_paragraph(paragraph)


    doc.save("LegalEase_Document.docx")


    with open(
        "LegalEase_Document.docx",
        "rb"
    ) as file:

        st.download_button(
            "Download DOCX",
            data=file,
            file_name="LegalEase_Document.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )


    # --------------------------------------------------
    # CREATE PDF
    # --------------------------------------------------

    pdf = FPDF()

    pdf.add_page()

    pdf.set_font(
      "Arial",
          size=12
    )

    for paragraph in edited_document.split("\n"):

        safe_paragraph = (
              paragraph
             .replace("’", "'")
             .replace("“", '"')
             .replace("”", '"')
             .replace("–", "-")
             .replace("—", "-")
             .replace("₹", "Rs.")
    )

    pdf.multi_cell(
        0,
        10,
        safe_paragraph.encode(
            "latin-1",
            "replace"
        ).decode("latin-1")
    )


    pdf.output(
        "LegalEase_Document.pdf"
    )


    with open(
        "LegalEase_Document.pdf",
        "rb"
    ) as file:

        st.download_button(
            "Download PDF",
            data=file,
            file_name="LegalEase_Document.pdf",
            mime="application/pdf")
        