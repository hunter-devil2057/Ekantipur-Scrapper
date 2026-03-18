# Ekantipur News & Cartoon Scraper 📰🎨

A robust Python-based web scraper built with **Playwright** to extract the latest entertainment news and the "Cartoon of the Day" from [ekantipur.com](https://ekantipur.com).

## 🚀 Features

- **Entertainment News**: Extracts the top 5 articles including titles, authors, categories, and high-quality image URLs.
- **Cartoon of the Day**: Automatically identifies and extracts the featured daily cartoon, including the artist's name and the image link.
- **Robust Navigation**: Optimized with `domcontentloaded` wait strategies to bypass heavy ads and trackers, ensuring consistent performance even on slow networks.
- **Smart Image Extraction**: Prioritizes actual processed image links (`thumb.php`) for the best visual quality.
- **Fallback Logic**: includes multi-selector support and fallback mechanisms for structural changes in the website.
- **Snapshots**: Automatically captures visual proof of the scraped sections.

## 🛠️ Prerequisites

- **Python 3.10+**
- **uv** (Recommended for fast dependency management) or **pip**

## 📦 Installation

1. **Clone the repository**:

   ```bash
   git clone https://github.com/your-username/ekantipur-scraper.git
   cd ekantipur-scraper
   ```

2. **Setup Environment**:
   It is recommended to use `uv` for a seamless experience:

   ```bash
   uv venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   uv sync
   ```

   _Alternatively, using pip with the provided `requirements.txt`:_

   ```bash
   pip install -r requirements.txt
   playwright install chromium
   ```

3. **Install Browser Binaries**:
   ```bash
   playwright install chromium
   ```

## 🚀 Usage

Run the scraper with a single command:

```bash
uv run scraper.py
```

### Output

The script generates the following files:

- `output.json`: Structured data containing news and cartoon details.
- `entertainment.png`: A snapshot of the entertainment news section.
- `cartoon.png`: A snapshot of the cartoon of the day.
- `cartoon-debug.png`: A full-page debug snapshot for troubleshooting.

## 📄 Output Format Example

```json
{
  "entertainment_news": [
    {
      "title": "...",
      "image_url": "https://assets-cdn-api.ekantipur.com/thumb.php?src=...",
      "category": "मनोरञ्जन",
      "author": "..."
    }
  ],
  "cartoon_of_the_day": {
    "title": "गजब छ बा!",
    "image_url": "...",
    "author": "अविन"
  }
}
```

## ⚖️ Troubleshooting

- **Navigation Timeouts**: The script uses `wait_until="domcontentloaded"` to avoid hanging on third-party ads. If you still face timeouts, increase the `timeout` parameter in `page.goto()`.
- **Bot Detection**: The scraper includes a standard `User-Agent` to minimize friction with anti-bot systems.

## 🤝 Contributing

Contributions are welcome! Feel free to open an issue or submit a pull request for improvements.

## 📬 Contact & Connect

Feel free to reach out if you have any questions, suggestions, or just want to connect!

- **Email**: [manishshiwakoti42@gmail.com](mailto:manishshiwakoti42@gmail.com)
- **LinkedIn**: [Manish Shiwakoti](https://www.linkedin.com/in/manish-shiwakoti-01721b260/)
- **Instagram**: [@shiwakoti.manish](https://www.instagram.com/shiwakoti.manish/)

---

⭐ If you find this project helpful, please consider giving it a star on GitHub!
