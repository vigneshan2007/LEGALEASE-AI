import os
import html

import requests
import streamlit as st

from dotenv import load_dotenv

from utils.document_formatter import (
    format_docx,
    format_pdf
)


# Load environment variables

load_dotenv()


# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(

    page_title="LegalEase",

    page_icon="⚖️",

    layout="wide"
)


# Backend URL

API_URL = os.getenv(
    "BACKEND_URL",
    "http://127.0.0.1:8000"
)


# --------------------------------------------------
# CUSTOM CSS
# --------------------------------------------------

st.markdown(
    """
    <style>

    .main-title {

        text-align: center;

        font-size: 42px;

        font-weight: 800;

        margin-bottom: 0;

    }


    .subtitle {

        text-align: center;

        color: #777;

        margin-bottom: 25px;

    }


    .preview {

        background: #111827;

        color: #f3f4f6;

        padding: 24px;

        border-radius: 14px;

        min-height: 420px;

        max-height: 650px;

        overflow: auto;

        white-space: pre-wrap;

        font-family: Georgia, serif;

        line-height: 1.7;

    }


    .small-note {

        font-size: 0.9rem;

        color: #666;

    }

    </style>
    """,
    unsafe_allow_html=True
)


# --------------------------------------------------
# HEADER
# --------------------------------------------------

st.markdown(
    '<div class="main-title">⚖️ LegalEase</div>',
    unsafe_allow_html=True
)


st.markdown(
    '<div class="subtitle">'
    'AI-Powered Legal Document Generator'
    '</div>',
    unsafe_allow_html=True
)


# Legal disclaimer

st.warning(
    "LegalEase creates AI-assisted drafts for information "
    "and editing. It is not a substitute for legal advice "
    "or jurisdiction-specific review."
)


# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

with st.sidebar:

    st.header(
        "Document Details"
    )


    # Document type

    document_type = st.selectbox(

        "Document Type",

        [

            "Freelance Work Contract",

            "Employment Contract",

            "Non-Disclosure Agreement (NDA)",

            "Lease Agreement",

            "Service Agreement",

            "General Agreement",

            "Other"

        ]
    )


    if document_type == "Other":

        document_type = st.text_input(
            "Enter document type",
            "Legal Agreement"
        )


    # Effective date

    effective_date = st.text_input(

        "Effective Date",

        "24/09/2026"
    )


    # Parties

    parties = st.text_area(

        "Parties Involved",

        "Jane Doe (Service Provider), "
        "Example Corp (Client)",

        height=110
    )


    # Terms

    terms = st.text_area(

        "Terms & Conditions",

        "Payment to be made within 30 days of invoice; "
        "Provider will deliver the agreed work by the deadline; "
        "Confidential information must be protected; "
        "Either party may terminate with 15 days notice",

        height=180
    )


    # Logo

    logo = st.file_uploader(

        "Optional Logo",

        type=[
            "png",
            "jpg",
            "jpeg"
        ]
    )


    # Generate button

    generate = st.button(

        "Generate Document",

        type="primary",

        use_container_width=True
    )


# --------------------------------------------------
# GENERATE DOCUMENT
# --------------------------------------------------

if generate:

    if not all(
        [
            document_type.strip(),
            effective_date.strip(),
            parties.strip(),
            terms.strip()
        ]
    ):

        st.error(
            "Please fill in all required fields."
        )

    else:

        payload = {

            "document_type":
                document_type,

            "parties":
                parties,

            "terms":
                terms,

            "effective_date":
                effective_date
        }


        try:

            with st.spinner(
                "Generating your legal draft..."
            ):

                response = requests.post(

                    f"{API_URL}/generate",

                    json=payload,

                    timeout=120
                )


            if response.ok:

                result = response.json()

                st.session_state[
                    "document"
                ] = result["document"]


                st.session_state[
                    "doc_type"
                ] = document_type


                st.success(
                    "Document generated successfully."
                )


            else:

                try:

                    detail = response.json().get(
                        "detail",
                        response.text
                    )

                except Exception:

                    detail = response.text


                st.error(
                    f"Backend error: {detail}"
                )


        except requests.RequestException as error:

            st.error(

                "Could not connect to FastAPI. "
                "Please make sure the backend is running "
                f"at {API_URL}.\n\n"
                f"Details: {error}"

            )


# --------------------------------------------------
# DOCUMENT PREVIEW
# --------------------------------------------------

if "document" in st.session_state:

    st.subheader(
        "Document Preview"
    )


    # Editable document

    edited_document = st.text_area(

        "Edit Document",

        value=st.session_state[
            "document"
        ],

        height=600,

        key="editor"
    )


    # Save edited version

    st.session_state[
        "document"
    ] = edited_document


    # HTML preview

    safe_document = html.escape(
        edited_document
    )


    st.markdown(

        f'<div class="preview">'
        f'{safe_document}'
        f'</div>',

        unsafe_allow_html=True
    )


    # --------------------------------------------------
    # FILE GENERATION
    # --------------------------------------------------

    if logo:

        logo_bytes = logo.getvalue()

    else:

        logo_bytes = None


    # TXT

    txt_data = edited_document.encode(
        "utf-8"
    )


    # DOCX

    docx_data = format_docx(

        edited_document,

        st.session_state[
            "doc_type"
        ],

        logo_bytes
    )


    # PDF

    pdf_data = format_pdf(

        edited_document,

        st.session_state[
            "doc_type"
        ],

        logo_bytes
    )


    # --------------------------------------------------
    # DOWNLOAD BUTTONS
    # --------------------------------------------------

    st.subheader(
        "Download Document"
    )


    col1, col2, col3 = st.columns(3)


    with col1:

        st.download_button(

            "⬇️ Download TXT",

            data=txt_data,

            file_name=
                "legalease_document.txt",

            mime="text/plain",

            use_container_width=True
        )


    with col2:

        st.download_button(

            "⬇️ Download DOCX",

            data=docx_data,

            file_name=
                "legalease_document.docx",

            mime=
                "application/vnd.openxmlformats-officedocument.wordprocessingml.document",

            use_container_width=True
        )


    with col3:

        st.download_button(

            "⬇️ Download PDF",

            data=pdf_data,

            file_name=
                "legalease_document.pdf",

            mime="application/pdf",

            use_container_width=True
        )


# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.markdown("---")


st.markdown(

    '<div class="small-note">'
    'LegalEase • AI-assisted drafting • '
    'Always verify important legal documents '
    'with a qualified professional.'
    '</div>',

    unsafe_allow_html=True
)