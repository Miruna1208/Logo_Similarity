import os
import re
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from PIL import Image
import io
import cairosvg 

os.makedirs("logos", exist_ok=True)

HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
LOGO_KEYWORDS = ["logo", "icon", "brand", "mark", "emblem"]

def has_logo_or_icon(value):
    if not value:
        return False
    if isinstance(value, list):
        return any(any(k in v.lower() for k in LOGO_KEYWORDS) for v in value)
    return any(k in value.lower() for k in LOGO_KEYWORDS)

def extract_background_image(style_value):
    match = re.search(r'url\(["\']?(.*?)["\']?\)', style_value or "")
    if match:
        return match.group(1)
    return None

def save_image_as_png(url, save_path):
    try:
        resp = requests.get(url, headers=HEADERS, timeout=8)
        resp.raise_for_status()
        if url.lower().endswith(".svg"):
            cairosvg.svg2png(bytestring=resp.content, write_to=save_path)
        else:
            img = Image.open(io.BytesIO(resp.content))
            img = img.convert("RGBA")
            img.save(save_path, format="PNG")
        return save_path
    except Exception:
        return None

def take_logo(url):
    domain_name = url.split("//")[-1].split("/")[0]
    try:
        r = requests.get(url, headers=HEADERS, timeout=8)
        r.raise_for_status()
    except Exception:
        return None

    soup = BeautifulSoup(r.text, "html.parser")

    icon_tags = soup.find_all("link", rel=lambda x: x and any(k in x.lower() for k in ["icon", "mask-icon", "apple-touch-icon"]))
    for tag in icon_tags:
        href = tag.get("href")
        if href:
            icon_url = urljoin(url, href)
            save_path = f"logos/{domain_name}.png"
            result = save_image_as_png(icon_url, save_path)
            if result:
                return result

    img_tag = soup.find("img", attrs={"class": has_logo_or_icon}) or soup.find("img", attrs={"id": has_logo_or_icon})
    if not img_tag:
        for img in soup.find_all("img"):
            src_candidates = [img.get("src"), img.get("data-src"), img.get("data-lazy")]
            src_candidates += img.get("srcset", "").split(",") if img.get("srcset") else []
            src_candidates = [s for s in src_candidates if s]
            for src in src_candidates:
                if has_logo_or_icon(src):
                    img_tag = img
                    break
            if img_tag:
                break

    if not img_tag:
        header = soup.find("header") or soup.find("nav")
        if header:
            img_tag = header.find("img")

    if not img_tag:
        containers = soup.find_all(lambda tag: tag.name in ["div", "section", "a", "figure", "span"] and (
            has_logo_or_icon(tag.get("class")) or has_logo_or_icon(tag.get("id"))
        ))
        for container in containers:
            style = container.get("style")
            bg_url = extract_background_image(style)
            if bg_url:
                bg_url = urljoin(url, bg_url)
                save_path = f"logos/{domain_name}.png"
                result = save_image_as_png(bg_url, save_path)
                if result:
                    return result
            picture_tag = container.find("picture")
            if picture_tag:
                source_tag = picture_tag.find("source")
                if source_tag and source_tag.get("srcset"):
                    src = urljoin(url, source_tag["srcset"].split()[0])
                    save_path = f"logos/{domain_name}.png"
                    result = save_image_as_png(src, save_path)
                    if result:
                        return result
            svg_tag = container.find("svg")
            if svg_tag:
                try:
                    save_path = f"logos/{domain_name}.png"
                    cairosvg.svg2png(bytestring=str(svg_tag).encode("utf-8"), write_to=save_path)
                    return save_path
                except Exception:
                    pass

    if img_tag and img_tag.get("src"):
        img_url = urljoin(url, img_tag.get("src"))
        save_path = f"logos/{domain_name}.png"
        result = save_image_as_png(img_url, save_path)
        if result:
            return result

    svg_tag = soup.find("svg", attrs={"class": has_logo_or_icon}) or soup.find("svg", attrs={"id": has_logo_or_icon})
    if svg_tag:
        try:
            save_path = f"logos/{domain_name}.png"
            cairosvg.svg2png(bytestring=str(svg_tag).encode("utf-8"), write_to=save_path)
            return save_path
        except Exception:
            pass

    return None
