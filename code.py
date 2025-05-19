import streamlit as st
from PIL import Image
import os
import io
import zipfile

st.title("Fatiador de Imagens Grandes")
st.write("Envie uma ou mais imagens para cortar em partes iguais.")

uploaded_files = st.file_uploader("Selecione as imagens", type=["png", "jpg", "jpeg"], accept_multiple_files=True)

modo = st.radio("Modo de fatiamento", options=["horizontal", "vertical"])
num_fatias = st.slider("Número de fatias por imagem", min_value=2, max_value=10, value=5)

if uploaded_files:
    pasta_saida = "fatias_temp"
    os.makedirs(pasta_saida, exist_ok=True)
    contador = 1
    zip_buffer = io.BytesIO()

    with zipfile.ZipFile(zip_buffer, "w") as zipf:
        for arquivo in uploaded_files:
            imagem = Image.open(arquivo)
            largura, altura = imagem.size

            for i in range(num_fatias):
                if modo == 'horizontal':
                    largura_fatia = largura // num_fatias
                    box = (i * largura_fatia, 0, (i + 1) * largura_fatia, altura)
                else:
                    altura_fatia = altura // num_fatias
                    box = (0, i * altura_fatia, largura, (i + 1) * altura_fatia)

                fatia = imagem.crop(box)
                nome_arquivo = f"fatia_{contador}.png"

                # Salva no ZIP
                buffer = io.BytesIO()
                fatia.save(buffer, format="PNG")
                zipf.writestr(nome_arquivo, buffer.getvalue())

                # Mostra na tela
                st.image(fatia, caption=nome_arquivo)
                contador += 1

    # Download final
    st.download_button(
        label="📦 Baixar todas as fatias (ZIP)",
        data=zip_buffer.getvalue(),
        file_name="fatias.zip",
        mime="application/zip"
    )
