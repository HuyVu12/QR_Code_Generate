import streamlit as st
import qrcode
import uuid

st.title("QR Code Generator")

st.write("Enter some text for generating QR code:")
text = st.text_area("Text")

def gen_qr(text):
    qrcode.make(text)
    file_name = f"{uuid.uuid4()}.png"
    qrcode.make(text).save(file_name)
    print(f"QR code saved to {file_name}")
    return file_name

if text:
    file_name = gen_qr(text)
    st.image(file_name, caption=f"QR code for {text}")