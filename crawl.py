import requests
from bs4 import BeautifulSoup
import json
import time

# Các category muốn crawl
CATEGORIES = {
    "Điện thoại": "https://www.thegioididong.com/dtdd",
    "Laptop": "https://www.thegioididong.com/laptop",
    "Tablet": "https://www.thegioididong.com/may-tinh-bang"
}
# Header giả lập trình duyệt
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/117.0 Safari/537.36"
}
# Hàm crawl một category
def crawl_category(name, url):
    print(f"Đang crawl {name} từ {url} ...")
    r = requests.get(url, headers=HEADERS)
    r.raise_for_status()

    soup = BeautifulSoup(r.text, "html.parser")
    products = []
    items = soup.select("a.main-contain")

    for item in items:
        # tên sản phẩm
        title_tag = item.find("h3")
        title = title_tag.get_text(" ", strip=True) if title_tag else ""

        # giá
        price_tag = item.find("strong")
        price = price_tag.get_text(strip=True) if price_tag else ""

        # ảnh
        img = item.find("img")
        img_url = ""
        if img:
            img_url = img.get("data-src") or img.get("src") or ""
            if img_url and not img_url.startswith("http"):
                img_url = "https:" + img_url

        # link chi tiết
        link = "https://www.thegioididong.com" + item["href"]

        products.append({
            "category": name,
            "title": title,
            "price": price,
            "image": img_url,
            "link": link
        })

    return products

# Hàm crawl tất cả các category và lưu vào file JSON
def crawl_tgdd_multi(output="tgdd_all.json"):
    all_products = []

    for cat, url in CATEGORIES.items():
        try:
            products = crawl_category(cat, url) # crawl tất cả sản phẩm trong 1 danh mục, trả về list
            all_products.extend(products) # thêm vào list tổng
            time.sleep(2)  # nghỉ 2s tránh spam
        except Exception as e: # nếu lỗi thì in ra và bỏ qua
            print(f"❌ Lỗi khi crawl {cat}: {e}")

    # Lưu JSON
    with open(output, "w", encoding="utf-8") as f:
        json.dump(all_products, f, ensure_ascii=False, indent=2)

    print(f"✅ Crawl xong {len(all_products)} sản phẩm, lưu vào {output}")

# Chạy hàm crawl
if __name__ == "__main__": 
    crawl_tgdd_multi()
