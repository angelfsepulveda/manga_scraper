# MangaPlus Selenium Scraper

This project is an automated scraper to download manga chapters from [manhuaplus.com](https://manhuaplus.com) and save them as PDF files, using Python, Selenium, and Pillow.

---

## What does this script do?

- **Automatically navigates** the manga page on manhuaplus.com.
- **Extracts the list of available chapters.**
- **Opens each chapter** in a Firefox browser controlled by Selenium.
- **Performs automatic scrolling** to load all images in the chapter.
- **Downloads all images** from each chapter.
- **Generates a PDF** for each chapter, saving the file in a folder with the manga and chapter name.
- **Deletes temporary images** after creating the PDF.

---

## Requirements

- Python 3.8+
- [Selenium](https://pypi.org/project/selenium/)
- [Pillow](https://pypi.org/project/Pillow/)
- [requests](https://pypi.org/project/requests/)
- Firefox installed
- [geckodriver](https://github.com/mozilla/geckodriver/releases) installed and accessible in your PATH

Install the dependencies with:
```bash
pip install selenium pillow requests
```

On Ubuntu you can install Firefox and geckodriver with:
```bash
sudo apt update
sudo apt install firefox firefox-geckodriver
```

---

## Quick Usage

1. **Set the manga URL**
   - Edit the `BASE_URL` variable in `main.py` and set the URL of the manga you want to download.

2. **Run the script**
   ```bash
   python main.py
   ```

3. **Results**
   - An `output/` folder will be created.
   - Inside `output/` there will be a subfolder for each chapter, named after the manga and chapter.
   - Inside each subfolder will be the PDF of the chapter.

---

## Technical Explanation (for programmers)

- **Selenium** is used to open Firefox in headless mode and browse the web like a real user.
- The script extracts chapter links using CSS selectors.
- For each chapter:
  - Opens the chapter page.
  - Waits for the images to be present.
  - Scrolls over the `.reading-content` container to load lazy-loaded images.
  - Extracts all image URLs (`<img src=...>`), converting relative URLs to absolute.
  - Downloads each image using `requests` with custom headers to avoid blocks.
  - Saves the images in a temporary folder specific to the chapter.
  - Uses Pillow to convert the images to a PDF.
  - Deletes the temporary images after creating the PDF.
- The PDF and folder names are generated from the manga and chapter names, extracted from the URL.

---

## Non-technical Explanation (for users)

- This program "simulates" a person browsing the manga website.
- It goes chapter by chapter, opens the page, scrolls to the bottom so all images load, and downloads them.
- It combines all the images from each chapter into a single PDF file, so you can read the manga offline.
- Everything is saved in an organized way in folders, and you don't need to do anything manually except run the script.

---

## Notes and Recommendations

- The script may take some time depending on the number of chapters and your connection speed.
- If the site changes its HTML structure, you may need to update the selectors in the script.
- Do not abuse scraping: respect wait times and do not download hundreds of chapters in a short time.
- This script is for personal and educational use only.

---

## Questions or Issues?

If you have questions or the script stops working, check the error messages in the console and make sure that:
- You have Firefox and geckodriver installed.
- The manga URL is correct.
- The site has not changed its structure.

You can open an issue or ask for help if you need additional support. 