import requests
import io
import json
import re
from PyPDF2 import PdfReader
from datetime import datetime
from requests.adapters import HTTPAdapter, Retry

def obtener_precio_y_fecha():
    url = "https://www.federaciondecafeteros.org/static/files/precio_cafe.pdf"

    # 🧠 Configuración segura de sesión
    session = requests.Session()
    retries = Retry(
        total=5,  # reintenta hasta 5 veces
        backoff_factor=5,  # espera 5s, luego 10s, 15s...
        status_forcelist=[429, 500, 502, 503, 504],
    )
    session.mount("https://", HTTPAdapter(max_retries=retries))

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120 Safari/537.36"
        ),
        "Accept": "application/pdf",
        "Accept-Language": "es-CO,es;q=0.9,en;q=0.8",
    }

    try:
        print("🌐 Descargando PDF de la Federación...")
        response = session.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        print("✅ PDF descargado correctamente")

        pdf_file = io.BytesIO(response.content)
        reader = PdfReader(pdf_file)
        text = "".join(page.extract_text() or "" for page in reader.pages)

        # 🔍 Buscar precio y fecha con expresiones regulares
        match_precio = re.search(r"\b[2-3],\d{3},\d{3}\b", text)
        match_fecha = re.search(
            r"(Enero|Febrero|Marzo|Abril|Mayo|Junio|Julio|Agosto|Septiembre|Octubre|Noviembre|Diciembre)\s+\d{1,2}\s*/\s*\d{4}",
            text,
        )

        precio = match_precio.group(0) if match_precio else "No disponible"
        fecha = match_fecha.group(0).replace(" /", ",") if match_fecha else "Fecha no encontrada"

        print(f"💰 Precio encontrado: {precio}")
        print(f"📅 Fecha encontrada: {fecha}")

        with open("precio.json", "w") as f:
            json.dump(
                {
                    "precio": precio,
                    "ultima_actualizacion": fecha,
                    "actualizado_en": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                },
                f,
                ensure_ascii=False,
                indent=2,
            )

        print("📦 Archivo precio.json actualizado")

    except requests.exceptions.Timeout:
        print("⏰ El servidor tardó demasiado en responder. Se mantiene el último valor.")
    except requests.exceptions.RequestException as e:
        print(f"⚠️ Error de red: {e}. Se mantiene el último valor.")
    except Exception as e:
        print(f"💥 Error inesperado: {e}")
    finally:
        print("🏁 Proceso finalizado.")


if __name__ == "__main__":
    obtener_precio_y_fecha()
