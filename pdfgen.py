import click
import requests
from fpdf import FPDF
from PIL import Image
from io import BytesIO


def generatePdfFromImages(imageUrls: list[str]) -> FPDF:
    pdf = FPDF(unit="pt")  # Use points for better sizing
    click.echo(f"Generating PDF with {len(imageUrls)} images")
    page = 1
    for url in imageUrls:
        click.echo(f"Processing image {page}/{len(imageUrls)}: {url}")
        page += 1
        response = requests.get(url)
        img = Image.open(BytesIO(response.content))
        width, height = img.size

        # Ensure RGB mode (some JPEGs might be CMYK or RGBA)
        if img.mode != "RGB":
            img = img.convert("RGB")

        # Save to memory as JPEG
        img_bytes = BytesIO()
        img.save(img_bytes, format="JPEG")
        img_bytes.seek(0)

        pdf.add_page(format=(width, height))
        pdf.image(img_bytes, x=0, y=0, w=width, h=height)

    return pdf
