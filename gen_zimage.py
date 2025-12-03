import os
import random
import json
from datetime import datetime
from g4f.client import Client as Client_g4f
from gradio_client import Client as Client_gradio
from gradio_client import handle_file
from PIL import Image

# === 1. 定義豐富的隨機元素庫 (增加多樣性與細節) ===
categories = {
    "themes": [
        "拍內衣形象照 (Lingerie Photoshoot)", 
        "日常生活照 (Casual Daily Life)", 
        "戶外旅遊照 (Luxury Travel)", 
        "健身房運動照 (Fitness & Gym)", 
        "OL上班工作照 (Office Lady Style)", 
        "居家男友視角 (POV at Home)",
        "海邊夕陽泳裝 (Sunset Beach Swimwear)",
        "咖啡廳網美打卡照 (Trendy Café Influencer Shot)",
        "逛街購物戰利品照 (Shopping Haul Outfit Shot)",
        "夜店派對酒吧照 (Nightlife & Club Scene)",
        "頂樓高空酒吧時尚照 (Rooftop Bar Fashion Portrait)",
        "飯店房間慵懶早晨 (Cozy Hotel Morning)",
        "閱讀書本文青風 (Bookish Aesthetic Reading)",
        "藝術感黑白人像 (Artistic Black & White Portrait)",
        "雨天撐傘街拍 (Rainy Day Street Style)",
        "城市夜景霓虹風 (Neon City Night Portrait)"
    ],

    "lighting": [
        "Golden hour sunlight (黃金時段陽光)", 
        "Soft window light (柔和窗光)", 
        "Cinematic studio lighting (電影級攝影棚光)", 
        "Bright natural daylight (明亮自然光)",
        "Rembrandt lighting (倫勃朗光)",
        "Neon sign lighting (霓虹燈打光)",
        "Backlit silhouette (逆光剪影效果)",
        "Softbox beauty lighting (柔光箱人像打光)",
        "Moody low-key lighting (低調暗調光)",
        "Fairy lights bokeh (小燈串散景光點)",
        "Overcast soft sky light (陰天柔和自然光)"
    ],

    "angles": [
        "Eye-level shot (平視)", 
        "Low angle shot (低角度仰拍, 顯腿長)", 
        "High angle selfie (高角度自拍)", 
        "Dutch angle (荷蘭式傾斜, 動感)", 
        "Close-up on face (臉部特寫)",
        "Three-quarter body shot (三分之四身構圖)",
        "Over-the-shoulder shot (從肩後視角拍攝)",
        "Side profile shot (側臉人像構圖)",
        "Mirror reflection shot (鏡中倒影構圖)",
        "From behind walking away (背影邊走邊拍)",
        "Extreme close-up on eyes (眼睛極近距離特寫)"
    ],

    "expressions": [
        "Seductive smile (誘惑微笑)", 
        "Innocent look (無辜眼神)", 
        "Confidence smirk (自信壞笑)", 
        "Biting lip slightly (輕咬嘴唇)", 
        "Looking directly into the camera with intense eyes (深情注視鏡頭)",
        "Playful wink (俏皮眨眼)",
        "Gentle soft smile (溫柔微笑)",
        "Daydreaming gaze away from camera (望向遠方出神)",
        "Shy smile while looking down (害羞低頭微笑)",
        "Cool and distant expression (冷酷高冷臉)",
        "Laughing naturally (自然大笑瞬間)"
    ],

    # 新增：服裝風格
    "outfits": [
        "優雅連身洋裝 (Elegant Dress Style)",
        "oversized 衛衣搭配熱褲 (Oversized Hoodie with Shorts)",
        "運動內衣與瑜伽褲 (Sports Bra & Yoga Pants)",
        "合身西裝外套與鉛筆裙 (Blazer & Pencil Skirt)",
        "牛仔外套配小可愛背心 (Denim Jacket with Crop Top)",
        "絲質睡衣套裝 (Silky Loungewear Set)",
        "比基尼與罩衫 (Bikini with Cover-up)",
        "簡約白T配直筒牛仔褲 (White Tee & Straight Jeans)",
        "針織毛衣配短裙 (Knit Sweater & Skirt)",
        "韓系學院風穿搭 (Korean Preppy Style)"
    ],

    # 新增：場景 / 地點
    "locations": [
        "落地窗旁沙發 (By the big window on a sofa)",
        "高級飯店房間 (Luxury hotel room)",
        "泳池邊躺椅 (Poolside sunbed)",
        "健身房鏡子前 (In front of gym mirror)",
        "都市街頭斑馬線 (City crosswalk streetshot)",
        "屋頂停車場 (Rooftop parking lot)",
        "森林步道 (Forest pathway)",
        "沙灘海岸線 (Sandy beach shoreline)",
        "咖啡廳窗邊座位 (Window seat at a café)",
        "書牆前的閱讀角落 (Reading corner with bookshelves)"
    ],

    # 新增：情緒 / 氣氛
    "moods": [
        "Cozy and intimate (溫馨親密感)",
        "Chic and fashionable (時尚高級感)",
        "Playful and cute (俏皮可愛氛圍)",
        "Cool and independent (酷帥獨立感)",
        "Relaxed weekend vibe (放鬆週末感)",
        "Dreamy and soft (夢幻柔焦風)",
        "Energetic and sporty (充滿活力運動風)",
        "Luxury lifestyle (高級生活質感)",
        "Mystery and allure (神秘魅惑氛圍)",
        "Minimalist clean aesthetic (極簡清爽感)"
    ],

    # 新增：色調 / 風格
    "color_grades": [
        "Warm and golden tones (溫暖金黃色調)",
        "Cool blue city tones (冷色系城市感)",
        "Pastel soft colors (粉彩小清新色調)",
        "High contrast and sharp (高反差銳利風)",
        "Film look grainy (類底片顆粒質感)",
        "Desaturated muted tones (低飽和性冷淡風)",
        "Vibrant and colorful (高飽和鮮豔色調)",
        "Black and white classic (黑白經典人像)"
    ],

    # 新增：道具
    "props": [
        "咖啡杯 (Coffee cup)",
        "手機自拍 (Using phone for mirror selfie)",
        "筆電與桌上文件 (Laptop and work documents)",
        "健身啞鈴或彈力帶 (Dumbbells or resistance bands)",
        "時尚手提包 (Designer handbag)",
        "太陽眼鏡 (Sunglasses)",
        "書本或雜誌 (Book or magazine)",
        "香檳或雞尾酒杯 (Champagne or cocktail glass)",
        "小燈串、蠟燭 (Fairy lights or candles)",
        "毯子與枕頭 (Blanket and pillows for cozy bed scene)"
    ]
}


def get_random_elements():
    return {
        "theme": random.choice(categories["themes"]),
        "light": random.choice(categories["lighting"]),
        "angle": random.choice(categories["angles"]),
        "expressions": random.choice(categories["expressions"]),
        "outfits": random.choice(categories["outfits"]),
        "locations": random.choice(categories["locations"]),
        "moods": random.choice(categories["moods"]),
        "color_grades": random.choice(categories["color_grades"]),
        "props": random.choice(categories["props"]),
    }

chosen = get_random_elements()

# === 2. 設計大師級 Prompt Template ===
# 這裡加入了針對 IG 演算法會喜歡的元素：高清晰度、完美皮膚、網紅風格
prompt_template = f"""
Act as a world-class AI art director and photographer. Create a prompt for an ultra-realistic, viral Instagram photo.

**Target Subject:** 
A stunningly beautiful, young, sexy Japanese female model (Idol/Influencer aesthetic). She looks like a top-tier gravure idol. 
Key features: Flawless but realistic skin texture (visible pores, faint vellus hair), large expressive eyes, cute yet seductive face, fit and curvy body shape (slim waist, ample chest), straight black silky hair.

**Current Scenario:**
- **Theme/Activity:** {chosen['theme']}
- **Lighting:** {chosen['light']} - Ensure the scene is bright, clear, and professional. NO heavy shadows or dark gloom.
- **Camera Angle:** {chosen['angle']}
- **Expression:** {chosen['expressions']}
- **outfits:** {chosen['outfits']}
- **locations:** {chosen['locations']}
- **moods:** {chosen['moods']}
- **color_grades:** {chosen['color_grades']}
- **props:** {chosen['props']}

**Detailed Instructions:**
1. **Opening:** Start with "A raw, ultra-realistic 8k photograph of..."
2. **Fashion:** Describe her outfit in extreme detail based on the theme. It must be trendy, sexy, and form-fitting to accentuate her curves. Mention fabric textures (e.g., silk, lace, denim, sheer).
3. **Environment:** Describe a high-end, aesthetic background (e.g., luxury cafe, modern apartment, sunny street in Tokyo). Blur the background (bokeh) to focus on her.
4. **Action:** Describe a natural, candid moment. She should look like she is interacting with her fans or the photographer.
5. **Quality Boosters:** Incorporate photography keywords: "Shot on Sony A7R IV", "85mm f/1.4 GM lens", "Depth of field", "Ray tracing", "Global illumination".

**Output Format:**
- Write ONLY the prompt paragraph.
- Do NOT write "Here is the prompt".
- Keep it continuous and descriptive (approx 100-150 words).
"""

# === Step 1: 用 g4f GPT-4o 生成高品質繪圖 prompt ===
client = Client_g4f()
try:
  response = client.chat.completions.create(
      model="gemma-3-27b-it",
      messages=[
          {
              "role": "user",
             "content": (
                  prompt_template
              )
          }
      ]
  )
except:
  response = client.chat.completions.create(
      model="gemini-2.5-flash-lite",
      messages=[
          {
              "role": "user",
             "content": (
                  prompt_template
              )
          }
      ]
  )
right_prompt = response.choices[0].message.content.strip()
image_prompt = right_prompt + """8k photo, Large breasts, deep cleavage, ample cleavage, sexy photo, beautilful girl without makeup"""
if 'sorry' in image_prompt or 'The model does not exist' in image_prompt:
	image_prompt = str(chosen)
print("🎨 Prompt:", image_prompt)

# === Step 2: 定義並選取圖片尺寸（所有尺寸皆 ≥ 1024） ===
image_sizes = [
    {"name": "portrait", "width": 800, "height": 1000}
]

size_choice = random.choice(image_sizes)
width = size_choice["width"]
height = size_choice["height"]

# === Step 3: 調用 Z-Image-Turbo 模型產圖 ===
client = Client_gradio("victor/Z-Image-Turbo-MCP")
result = client.predict(
    prompt=image_prompt,
    resolution='864x1152 ( 3:4 )',
    seed=42,
    steps=12,
    shift=3,
    random_seed=True,
    api_name="/generate_image"
)

# === Step 4: 建立日期資料夾與檔名 ===
today = datetime.now().strftime("%Y_%m_%d")
folder_path = os.path.join("images", today)
os.makedirs(folder_path, exist_ok=True)

existing_files = [f for f in os.listdir(folder_path) if f.endswith("_thumb.webp")]
image_index = len(existing_files) + 1
# filename = f"{today}_{image_index:02}.webp"
# output_path = os.path.join(folder_path, filename)

# # === Step 5: 將 .webp 轉存為 .webp ===
# webp_path = result[0]

# with Image.open(webp_path) as img:
#     img.save(output_path, "WEBP", quality=85)  # 可調整品質（預設 80–85）

# print(f"✅ 圖片已儲存：{output_path}")

base_filename = f"{today}_{image_index:02}"
output_path = os.path.join(folder_path, f"{base_filename}.webp")
thumb_path = os.path.join(folder_path, f"{base_filename}_thumb.webp")

# === Step 5: 讀取原始 .webp 並儲存原圖與縮圖 ===
webp_path = result[0]  # ← 你的來源 .webp 圖檔路徑

client = Client_gradio("OzzyGT/basic_upscaler")
result = client.predict(
		image=handle_file(webp_path),
		model_selection="DAT-2 RealWebPhoto X4",
		api_name="/upscale_image"
)

webp_path = result[1]

with Image.open(webp_path) as img:
    # 儲存原圖
    img.save(output_path, "WEBP", quality=85)

    # 建立縮圖
    thumbnail_width = 400
    ratio = thumbnail_width / img.width
    new_size = (thumbnail_width, int(img.height * ratio))

    thumb = img.convert("RGB").resize(new_size, Image.LANCZOS)
    thumb.save(thumb_path, "WEBP", quality=80)





# === Step 6: 更新 data.json ===
json_path = os.path.join(folder_path, "data.json")
timestamp = datetime.utcnow().isoformat() + "Z"

new_entry = {
    "filename": output_path,
    "thumb_path": thumb_path,
    "prompt": image_prompt,
    "width": width,
    "height": height,
    "style": size_choice["name"],
    "timestamp": timestamp
}

if os.path.exists(json_path):
    with open(json_path, "r") as f:
        data = json.load(f)
else:
    data = {"date": today, "images": []}

data["images"].append(new_entry)

with open(json_path, "w") as f:
    json.dump(data, f, indent=2)

print(f"📄 data.json 已更新：{json_path}")

# === Step 7: 更新 README.md 每行最多顯示 10 張圖片 ===
readme_path = os.path.join(folder_path, "README.md")
image_files = sorted([f for f in os.listdir(folder_path) if ((f.endswith(".webp")) and (not f.endswith("_thumb.webp")))])

readme_lines = ["# Generated Images", ""]
row = []

for i, image_file in enumerate(image_files, 1):
    row.append(f'<img src="{image_file}" width="100"/>')
    if i % 9 == 0:
        readme_lines.append(" ".join(row))
        row = []

if row:
    readme_lines.append(" ".join(row))

with open(readme_path, "w") as f:
    f.write("\n\n".join(readme_lines))

print(f"📄 README.md 已更新：{readme_path}")
