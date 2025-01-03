import streamlit as st
import qrcode
import uuid
import lorem
import os 

if 'textInput' not in st.session_state:
    st.session_state.textInput = ''

if 'file_name' not in st.session_state:
    st.session_state.file_name = ''

if 'fill_color' not in st.session_state:
    st.session_state.fill_color = '#000000'

if 'back_color' not in st.session_state:
    st.session_state.back_color = '#ffffff'

st.set_page_config(
    page_title="QR Code Generator", 
    page_icon='<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 448 512"><!--!Font Awesome Free 6.7.2 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license/free Copyright 2025 Fonticons, Inc.--><path fill="#63E6BE" d="M0 80C0 53.5 21.5 32 48 32l96 0c26.5 0 48 21.5 48 48l0 96c0 26.5-21.5 48-48 48l-96 0c-26.5 0-48-21.5-48-48L0 80zM64 96l0 64 64 0 0-64L64 96zM0 336c0-26.5 21.5-48 48-48l96 0c26.5 0 48 21.5 48 48l0 96c0 26.5-21.5 48-48 48l-96 0c-26.5 0-48-21.5-48-48l0-96zm64 16l0 64 64 0 0-64-64 0zM304 32l96 0c26.5 0 48 21.5 48 48l0 96c0 26.5-21.5 48-48 48l-96 0c-26.5 0-48-21.5-48-48l0-96c0-26.5 21.5-48 48-48zm80 64l-64 0 0 64 64 0 0-64zM256 304c0-8.8 7.2-16 16-16l64 0c8.8 0 16 7.2 16 16s7.2 16 16 16l32 0c8.8 0 16-7.2 16-16s7.2-16 16-16s16 7.2 16 16l0 96c0 8.8-7.2 16-16 16l-64 0c-8.8 0-16-7.2-16-16s-7.2-16-16-16s-16 7.2-16 16l0 64c0 8.8-7.2 16-16 16l-32 0c-8.8 0-16-7.2-16-16l0-160zM368 480a16 16 0 1 1 0-32 16 16 0 1 1 0 32zm64 0a16 16 0 1 1 0-32 16 16 0 1 1 0 32z"/></svg>',
    layout="wide"
)
st.title("QR Code Generator")

def gen_qr(text):
    qrcode.make(text)
    file_name = f"{uuid.uuid4()}.png"
    qrcode.make(text).save(file_name)
    return file_name
def gen_qr_with_color(text, fill_color, back_color):
    qr = qrcode.QRCode(
        version=None,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(text)
    qr.make(fit=True)

    file_name = f"{uuid.uuid4()}.png"
    img = qr.make_image(fill_color=fill_color, back_color=back_color)
    img.save(file_name)
    return file_name

m_col1, m_col2 = st.columns([2, 1], vertical_alignment='center')

with m_col1:   
    r1_c1, r1_c2 = st.columns(2)
    with r1_c1:
        st.session_state.fill_color = st.color_picker('Fill color', value=st.session_state.fill_color)
    with r1_c2:
        st.session_state.back_color = st.color_picker('Back color', value=st.session_state.back_color)
    text = st.text_area("Content here", 
                        placeholder="Enter text here for generating QR code",
                        value=st.session_state.textInput,
                        max_chars=1000,
                        )
    
    st.session_state.textInput = text
    m_col1_1, m_col1_2, m_col1_3 = st.columns([1, 1, 1], vertical_alignment='center')
    with m_col1_1:
        if st.button('Generate'):
            if len(st.session_state.textInput) == 0:
                st.toast("Please enter some text")
            elif len(st.session_state.textInput) > 1000:
                st.toast("Your content is too long, please enter less than 1000 characters")
            else:
                with st.spinner("Waiting for QR code to be generated..."):
                    st.session_state.file_name = gen_qr_with_color(
                        text,
                          st.session_state.fill_color,
                          st.session_state.back_color
                        )
                    # st.info(f'{st.session_state.fill_color} - {st.session_state.back_color}')
                    st.toast("QR code generated successfully")
                    st.balloons()
    with m_col1_2:
        if st.button('Reset'):
            st.session_state.textInput = ''
            st.session_state.fill_color = '#000000'
            st.session_state.back_color = '#ffffff'
            st.rerun()
    with m_col1_3:
        if st.session_state.file_name:
            with open (st.session_state.file_name, 'rb') as file:
                btn = st.download_button(
                    label="Download image",
                    data=file,
                    file_name=f"{st.session_state.file_name}",
                    mime="image/png",
                )

    col1, col2 = st.columns(2, vertical_alignment='bottom')
    with col1:
        st.number_input(min_value=1, value=1, key="num_gen_lorem", label="Number paragraph")
    with col2:
        if st.button('Generate Some Text'):
            text = ''
            for _ in range(st.session_state.num_gen_lorem):
                text += lorem.paragraph()
            st.session_state.textInput = text
            st.rerun()

with m_col2:
    if len(st.session_state.file_name) > 0:
        st.image(st.session_state.file_name, caption=f"{os.getcwd()}/{st.session_state.file_name}")