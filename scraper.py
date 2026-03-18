import json
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError

def scrape_ekantipur():
    with sync_playwright() as p:
        # Launch browser in headless mode (change to headless=False to watch)
        browser = p.chromium.launch(headless=True)
        print("Browser launched...")
        page = browser.new_page(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")
        print("New page created...")

        # ==========================================
        # 1. Scrape Entertainment (मनोरञ्जन) News
        # ==========================================
        print("Navigating to Entertainment section...")
        page.goto("https://ekantipur.com/entertainment", wait_until="domcontentloaded", timeout=60000)
        
        try:
            page.wait_for_selector(".category-inner-wrapper", timeout=20000)
        except PlaywrightTimeoutError:
            print("Warning: .category-inner-wrapper not found quickly → falling back to body load")
            page.wait_for_selector("body", timeout=10000)

        # Extract top 5 articles
        # articles_elements = page.locator(".category-inner-wrapper").all()
        articles_elements = page.locator(".category-inner-wrapper").all()[:5]
        
        entertainment_news = []
        for i, article in enumerate(articles_elements):
            # Title
            title_el = article.locator("h2 a, h3 a, .teaser-title a").first
            title = title_el.text_content().strip() if title_el.count() > 0 else None
            
            # Author
            author_el = article.locator(".author-name a, .byline, .author").first
            author = author_el.text_content().strip() if author_el.count() > 0 else None
            
            # Category
            header_cat_el = page.locator(".category-name a, h1, .section-title").first
            category = header_cat_el.text_content().strip() if header_cat_el.count() > 0 else "मनोरञ्जन"

            # Image URL
            img_el = article.locator("img.lazy, img[src*='jpg'], img[data-src], .category-image img").first
            image_url = None
            if img_el.count() > 0:
                image_url = (
                    img_el.get_attribute("src") or
                    img_el.get_attribute("data-src") or
                    img_el.get_attribute("data-lazy-src") or
                    img_el.get_attribute("data-original")
                )

            if title:
                entertainment_news.append({
                    "title": title,
                    "image_url": image_url,
                    "category": category,
                    "author": author
                })

        print(f"Extraction details: {len(entertainment_news)} articles found.")
        page.screenshot(path="entertainment.png", full_page=False)
        print("Captured entertainment.png")

        # ==========================================
        # 2. Scrape Cartoon of the Day (व्यंग्यचित्र)
        # ==========================================
        print("Navigating to Cartoon section...")
        page.goto("https://ekantipur.com/cartoon", wait_until="domcontentloaded", timeout=60000)

        # Try multiple possible selectors for the featured cartoon container
        cartoon_selectors = [
            ".teaser-lead",           # often used for featured item
            ".feature",               # featured / lead story
            ".teaser",                # common teaser block
            ".story-teaser", 
            ".main-cartoon", 
            "[class*='cartoon']",     # contains cartoon/vyangya
            "[class*='vyangya']",
            "section.featured", 
            ".lead-story",
            ".cartoon-item",
        ]

        cartoon_container = None
        used_selector = None

        for selector in cartoon_selectors:
            try:
                container = page.locator(selector).first
                if container.count() > 0 and container.is_visible(timeout=5000):
                    cartoon_container = container
                    used_selector = selector
                    print(f"Found cartoon container using: {selector}")
                    break
            except:
                pass

        if not cartoon_container:
            # Ultimate fallback: any large image + title block
            print("No specific container found → using fallback (large image + nearby title)")
            cartoon_container = page.locator("img[src*='cartoon'], img[width][height]").locator("xpath=ancestor::div[1]").first
            used_selector = "fallback-large-image-ancestor"

        page.screenshot(path="cartoon-debug.png", full_page=True)
        print("Captured cartoon-debug.png → check this if extraction fails!")

        if cartoon_container:
            # Title
            c_title_el = cartoon_container.locator("h1, h2, h1 a, h2 a, .teaser-title, .headline, .title").first
            c_title = c_title_el.text_content().strip() if c_title_el.count() > 0 else "No title found"

            # Author (very common: after dash in title, or .author/byline)
            c_author = None
            if " - " in c_title:
                parts = c_title.split(" - ", 1)
                c_title = parts[0].strip()
                c_author = parts[1].strip()
            else:
                author_el = cartoon_container.locator(".author, .byline, .author-name, [class*='author']").first
                if author_el.count() > 0:
                    c_author = author_el.text_content().strip()

            # Image
            c_img_el = cartoon_container.locator("img.lazy, img:not([src*='logo']):not([src*='placeholder']), .cartoon-image img").first
            c_image_url = None
            if c_img_el.count() > 0:
                c_image_url = (
                    c_img_el.get_attribute("src") or
                    c_img_el.get_attribute("data-src") or
                    c_img_el.get_attribute("data-lazy-src") or
                    c_img_el.get_attribute("data-original")
                )

            cartoon_data = {
                "title": c_title,
                "image_url": c_image_url,
                "author": c_author or "Unknown"
            }
        else:
            cartoon_data = {"title": "Failed to locate cartoon", "image_url": None, "author": None}
            print("Warning: Could not locate cartoon container")

        # ==========================================
        # 3. Save to JSON
        # ==========================================
        output_data = {
            "entertainment_news": entertainment_news,
            "cartoon_of_the_day": cartoon_data,
            "debug": {"cartoon_used_selector": used_selector}
        }

        with open("output.json", "w", encoding="utf-8") as f:
            json.dump(output_data, f, ensure_ascii=False, indent=4)

        print("Scraping completed. Data saved to output.json.")
        browser.close()

if __name__ == "__main__":
    scrape_ekantipur()