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