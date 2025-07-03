import os
import re
import time
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from PIL import Image
import requests
from selenium.webdriver.firefox.service import Service
from urllib.parse import urljoin

BASE_URL = "https://manhuaplus.com/manga/emperors-domination/"
OUTPUT_DIR = "output"


def sanitize_filename(name):
    return re.sub(r'[\\/*?:"<>|]', "", name)


def get_chapter_links(driver):
    print("[*] Getting list of chapters...")
    driver.get(BASE_URL)
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "ul.main li.wp-manga-chapter > a"))
    )
    links = driver.find_elements(By.CSS_SELECTOR, "ul.main li.wp-manga-chapter > a")
    chapter_list = [(a.text.strip(), a.get_attribute("href")) for a in links]
    print(f"[+] Found {len(chapter_list)} chapters.")
    return chapter_list
    

def get_image_urls(driver, chapter_url):
    driver.get(chapter_url)
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.reading-content img"))
        )
        time.sleep(1)  # Wait 1 second after opening the chapter
        # Scroll over the reading-content container to load all images
        reading_content = driver.find_element(By.CSS_SELECTOR, "div.reading-content")
        last_height = driver.execute_script("return arguments[0].scrollHeight", reading_content)
        while True:
            driver.execute_script("arguments[0].scrollTo(0, arguments[0].scrollHeight);", reading_content)
            time.sleep(1)  # Wait for images to load
            new_height = driver.execute_script("return arguments[0].scrollHeight", reading_content)
            if new_height == last_height:
                break
            last_height = new_height
    except TimeoutException:
        print(f"[!] Timeout waiting for images in {chapter_url}")
        return []
    img_tags = driver.find_elements(By.CSS_SELECTOR, "div.reading-content img")
    print(f"[DEBUG] Found {len(img_tags)} images in reading-content")
    # Convert relative URLs to absolute
    img_urls = []
    for img in img_tags:
        src = img.get_attribute("src")
        if src:
            abs_url = urljoin(chapter_url, src.strip())
            img_urls.append(abs_url)
    return img_urls


def download_images(image_urls, temp_folder):
    image_paths = []
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15",
        "Mozilla/5.0 (X11; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0"
    ]
    for i, url in enumerate(image_urls):
        print(f"[DEBUG] Image URL: {url}")
        try:
            ext = url.split(".")[-1].split("?")[0]
            filename = os.path.join(temp_folder, f"tmp_{i:03}.{ext}")
            headers = {
                "User-Agent": user_agents[i % len(user_agents)],
                "Referer": BASE_URL
            }
            r = requests.get(url, headers=headers, timeout=10)
            content_type = r.headers.get("Content-Type", "")
            if "html" in content_type or r.content[:15].lower().startswith(b'<!doctype html'):
                with open(filename + ".html", "wb") as f:
                    f.write(r.content)
                print(f"[ERROR] Downloaded HTML instead of image for {url}")
                continue
            with open(filename, "wb") as f:
                f.write(r.content)
            image_paths.append(filename)
        except Exception as e:
            print(f"[!] Error downloading {url}: {e}")
    return image_paths


def images_to_pdf(images, output_path):
    pil_images = []
    for img_path in images:
        try:
            image = Image.open(img_path).convert("RGB")
            pil_images.append(image)
        except Exception as e:
            print(f"[!] Error opening image {img_path}: {e}")
    if pil_images:
        pil_images[0].save(output_path, save_all=True, append_images=pil_images[1:])
        print(f"[+] PDF saved: {output_path}")
        return True
    else:
        print(f"[!] PDF was not generated due to lack of images.")
        return False


def scrape_one_chapter(driver, title, chapter_url):
    manga_name = sanitize_filename(BASE_URL.rstrip('/').split('/')[-1])
    # Extract chapter name from the URL
    chapter_part = chapter_url.split(manga_name)[-1].replace("/", "").replace("chapter", "Chapter ") or "unknown_chapter"
    clean_title = sanitize_filename(chapter_part)
    chapter_folder = os.path.join(OUTPUT_DIR, f"{manga_name}_{clean_title}")
    os.makedirs(chapter_folder, exist_ok=True)
    print(f"\n[*] Processing: {clean_title} (folder: {chapter_folder})")
    image_urls = get_image_urls(driver, chapter_url)
    images = download_images(image_urls, chapter_folder)
    pdf_filename = f"{manga_name}_{clean_title}.pdf"
    pdf_path = os.path.join(chapter_folder, pdf_filename)
    pdf_created = images_to_pdf(images, pdf_path)
    # Clean up images after PDF creation
    for img in images:
        try:
            os.remove(img)
        except Exception as e:
            print(f"[!] Error deleting image {img}: {e}")
    return pdf_created


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    options = Options()
    options.headless = True
    service = Service(executable_path="/snap/bin/geckodriver")  # Change if your path is different
    driver = webdriver.Firefox(service=service, options=options)
    try:
        chapters = get_chapter_links(driver)
        chapters.reverse()  # chronological order
        for idx, (title, url) in enumerate(chapters):
            try:
                scrape_one_chapter(driver, title, url)
                time.sleep(1)  # 1 second timeout between chapters
            except Exception as e:
                print(f"[!] Error processing chapter {title}: {e}")
    finally:
        driver.quit()


if __name__ == "__main__":
    main()
