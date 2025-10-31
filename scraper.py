import requests, io, json, re
from PyPDF2 import PdfReader

def obtener_precio_y_fecha():
    url = "https://www.federaciondecafeteros.org/static/files/precio_cafe.pdf"
    response = requests.get(url)
    pdf_file = io.BytesIO(response.content)
    reader = PdfReader(pdf_file)
    text = "".join(page.extract_text() for page in reader.pages)

    match_precio = re.search(r'\b[2-3],\d{3},\d{3}\b', text)
    match_fecha = re.search(r"(Enero|Febrero|Marzo|Abril|Mayo|Junio|Julio|Agosto|Septiembre|Octubre|Noviembre|Diciembre)\s+\d{1,2}\s*/\s*\d{4}", text)

    precio = match_precio.group(0) if match_precio else "No disponible"
    fecha = match_fecha.group(0).replace(" /", ",") if match_fecha else "Fecha no encontrada"

    with open("precio.json", "w") as f:
        json.dump({"precio": precio, "ultima_actualizacion": fecha}, f)

if __name__ == "__main__":
    obtener_precio_y_fecha()
