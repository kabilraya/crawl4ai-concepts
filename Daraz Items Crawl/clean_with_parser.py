from bs4 import BeautifulSoup
from textwrap import dedent
def parse_html_result(result):
    soup = BeautifulSoup(result.html,'lxml')
    
    title = soup.select_one(".pdp-mod-product-badge-title")
    product_name = title.get_text(strip = True) if title else "Title Not Found"

    image_element = soup.select_one("img.gallery-preview-panel")

    img_src = image_element["src"] if image_element else "Image not found"

    price_element = soup.select_one("span.pdp-price_size_xl")
    price = price_element.get_text(strip = True) if price_element else "Price not found"

    description_items = soup.select("article.lzd-article ul li")
    description_text = "\n".join(f"- {li.get_text(strip=True)}" for li in description_items)

    
    specs_container = soup.select_one("div.pdp-mod-specification")
    specs_text = specs_container.get_text(separator='\n', strip=True) if specs_container else "Specifications not found"

    clean_markdown = f"""
## {product_name}

**Product URL:** <{result.url}>

![Product Image]({img_src})

---

## Price
{price}

---

## Description
{description_text}

---

## Specifications
{specs_text}
"""
    
    print(clean_markdown)

    
    with open("product-details-clean.md", "a", encoding="utf-8") as f:
        f.write(clean_markdown + "\n\n\n ---End of Product--- \n\n\n")
    

