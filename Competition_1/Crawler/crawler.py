import requests
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

def fetch_images_with_scroll(query, folder_name="images", num_images=100):
    # Tạo URL tìm kiếm
    search_url = f"https://www.google.com/search?hl=en&tbm=isch&q={query}"
    # Khởi tạo trình duyệt
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Chạy ẩn trình duyệt (không giao diện)
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(options=options)
    driver.get(search_url)
    
    # Tạo thư mục lưu hình
    os.makedirs(folder_name, exist_ok=True)
    
    # Cuộn trang để tải thêm hình
    img_urls = set()
    last_height = driver.execute_script("return document.body.scrollHeight")
    scroll_count = 0
    
    while len(img_urls) < num_images and scroll_count < 50:  # Giới hạn cuộn tối đa 50 lần
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)  # Chờ hình ảnh tải xong
        images = driver.find_elements(By.CSS_SELECTOR, "img")
        for img in images:
            src = img.get_attribute("src")
            if src and "http" in src:
                img_urls.add(src)
        
        # Kiểm tra nếu không cuộn thêm được
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height
        scroll_count += 1
    
    # Tải xuống hình ảnh
    count = 1
    for img_url in img_urls:
        if count >= num_images:
            break
        try:
            response = requests.get(img_url, stream=True)
            
            # Kiểm tra kích thước tệp
            content_length = response.headers.get("content-length")
            if content_length and int(content_length) < 5000:  # Nếu kích thước < 5 KB, bỏ qua
                print(f"Bỏ qua hình ảnh (kích thước < 5 KB): {img_url}")
                continue
            
            # Tải và lưu hình ảnh
            img_data = response.content
            file_path = os.path.join(folder_name, f"22521070-22520211.{folder_name}.{count}.jpg")
            with open(file_path, "wb") as img_file:
                img_file.write(img_data)
            count += 1
            print(f"Đã lưu hình: {file_path}")
        except Exception as e:
            print(f"Lỗi khi tải {img_url}: {e}")
    
    driver.quit()


# Sử dụng hàm
#name_list = ['Honda+car', 'Hyundai+car', 'KIA+car', 'Mazda+car', 'Mitsubishi+car', 'Xe+dap+Xe+ban+tai+Xe+tai+Xe+ba+banh+Xe+may', 'Suzuki+car', 'Toyota+car', 'VinFast+car']
name_list = ['Suzuki+car']
os.makedirs('CS114_Data', exist_ok=True)  # Tạo thư mục nếu chưa có
os.chdir('CS114_Data')

for n in name_list:
    fol_name = n.split("+")[0]
    fetch_images_with_scroll(query=n, folder_name=fol_name, num_images=300)
