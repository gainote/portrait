import os
import random
import json
from datetime import datetime
from g4f.client import Client as Client_g4f
from gradio_client import Client as Client_gradio
from gradio_client import handle_file
from PIL import Image

types = ["拍內衣形象照", "日常生活照", "戶外旅遊照", "運動照", "上班工作照"]

def pick_elements(category, n=1):
    return random.sample(category, n)

chosen = {
    "types": pick_elements(types)
}

prompt_template = f"""
請作為一名專業的影像生成提示詞（Prompt）設計師。你的任務是為 AI 影像生成模型創建一個高度詳細、描述豐富的 prompt。每次生成都應遵循以下嚴格的結構和內容要求，以確保產出的影像具有電影級的真實感、藝術品質和豐富的細節。
提示詞結構要求：
開頭定調 (Opening Statement)： 必須以 This is a high-resolution photograph of... 或 The image is a cinematic, ultra-detailed photograph featuring... 開頭，強調高解析度、寫實性和細節。
核心主體描述 (Core Subject Description)：
人物概況： 包含性別、大致年齡（如 "in her late 20s"）、種族/外貌特徵（如 "East Asian woman"）。
膚色與質感： 描述膚色（如 "fair complexion," "tanned skin"）和可能的質感（如 "smooth skin"）。
髮型： 髮色、長度、質地和具體髮型（如 "long, straight black hair," "curly red hair tied in a bun"）。
表情與姿態： 臉部表情（如 "smiling warmly," "contemplative expression"）、眼神（如 "expressive eyes"）和具體的肢體動作（如 "her left arm is raised, with her hand resting on the back of her head," "standing casually with hands in pockets"）。
臉部特徵： 鼻形、唇形、唇膏顏色、臉型等（如 "delicate facial features, with high cheekbones, a small nose, and full lips painted with a soft pink lipstick"）。
衣著與配件 (Attire & Accessories)：
服裝類型： 詳細說明上衣、下裝、外套等具體衣物（如 "a light gray sports bra," "a deep burgundy V-neck crop top," "low-rise, light blue denim shorts"）。
服裝細節： 剪裁、材質、款式、顏色、以及對身材的影響（如 "accentuates her ample breasts," "deep V-neckline, which reveals a significant amount of cleavage," "smooth, stretchy fabric that clings to her body"）。
配件： 任何珠寶、手錶、包包、帽子等（如 "a delicate gold necklace with a small, black cross pendant," "long, dangling earrings that feature a crescent moon and star design"）。
背景環境 (Background Setting)：
場景類型： 描述是室內、室外、城市、自然等。
具體物件： 場景中的主要元素，如家具、建築、自然景觀、特定道具（如 "a wooden door to her left and a traditional Japanese-style sliding door to her right," "modern, well-lit gym," "cityscape with tall buildings is visible outside the window"）。
背景細節： 顏色、材質、紋理（如 "soft, mauve curtain that is slightly textured," "walls are painted a neutral color"）。
光線與氛圍 (Lighting & Ambiance)：
光線類型： 自然光、人造光、光源方向（如 "soft and even," "bright and even," "natural light to flood the room"）。
光線效果： 光線如何影響主體和場景（如 "casting a gentle glow on her skin and highlighting the contours of her body," "illuminating her face and the surrounding area"）。
整體氛圍： 影像想要傳達的情緒或感覺（如 "intimate and inviting," "casual, intimate setting," "clean and modern," "warm and intimate moment"）。
特殊元素/互動 (Optional: Special Elements/Interaction)：
如果需要，可以包含其他角色、動物、或主體與環境/其他物件的互動（如 "a white cat with a fluffy coat is playfully pawing at her chest"）。這些元素應詳細描述其動作和對整體氛圍的貢獻。
輸出格式要求：
每次生成應只輸出一個完整的 prompt，不包含任何額外說明或對話。
prompt 應是流暢、連貫的英文段落。
長度應足夠詳盡，一般至少包含 5-8 句話，甚至更多。
請避免模糊或籠統的詞語，力求具體和可視化。
現在，請根據上述 instruction，為一個年輕火辣性感的日系AV女優的 IG 日常照片(畫面要明亮清晰、不要昏暗 陰影過多) 穿著性感 {', '.join(chosen['types'])} 創作一個詳細的影像生成 prompt。"""

# === Step 1: 用 g4f GPT-4o 生成高品質繪圖 prompt ===
client = Client_g4f()

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {
            "role": "user",
            "content": (
                prompt_template
            )
        }
    ]
)

image_prompt = response.choices[0].message.content.strip()+ """8k photo, Large breasts, deep cleavage, ample cleavage，sexy photo, beautilful korean girl without makeup"""
print("🎨 Prompt:", image_prompt)

# === Step 2: 定義並選取圖片尺寸（所有尺寸皆 ≥ 1024） ===
image_sizes = [
    {"name": "portrait", "width": 800, "height": 1000}
]

size_choice = random.choice(image_sizes)
width = size_choice["width"]
height = size_choice["height"]

# === Step 3: 調用 FLUX Space 模型產圖 ===
client = Client_gradio("Qwen/Qwen-Image")
result = client.predict(
		prompt=image_prompt,
		seed=0,
		randomize_seed=True,
		aspect_ratio="3:4",
		guidance_scale=4,
		num_inference_steps=50,
		prompt_enhance=True,
		api_name="/infer"
)

# === Step 4: 建立日期資料夾與檔名 ===
today = datetime.now().strftime("%Y_%m_%d")
folder_path = os.path.join("images", today)
temp_path = os.path.join("temp", today)
os.makedirs(folder_path, exist_ok=True)
os.makedirs(temp_path, exist_ok=True)

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
temp_path = os.path.join(temp_path, f"{base_filename}.webp")

# === Step 5: 讀取原始 .webp 並儲存原圖與縮圖 ===
webp_path = result[0]  # ← 你的來源 .webp 圖檔路徑

with Image.open(webp_path) as img:
    # 儲存原圖
    img.save(output_path, "WEBP", quality=85)
    img.save(temp_path, "WEBP", quality=85)

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
