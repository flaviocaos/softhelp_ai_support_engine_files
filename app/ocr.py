from PIL import Image
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
def ocr_image(path: str) -> str:
    img = Image.open(path).convert('RGB')
    return pytesseract.image_to_string(img)
def classify_from_ocr(text: str):
    t = (text or '').lower()
    tags = {}
    if 'username or password is incorrect' in t or 'usuario o contraseña incorrectos' in t:
        tags['issue'] = 'login_incorrect_credentials'
    if 'unexpected error' in t or 'critical error' in t:
        tags['issue'] = 'critical_error'
    return tags
