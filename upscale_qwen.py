import os
import random
import json
from datetime import datetime
from g4f.client import Client as Client_g4f
from gradio_client import Client as Client_gradio
from gradio_client import handle_file
from PIL import Image

today = datetime.now().strftime("%Y_%m_%d")
temp_path = os.path.join("temp", today)
max_process = 3
cur_process = 0
for img in os.listdir(temp_path):
  img_path = os.path.join("temp", img)
  client = Client_gradio("OzzyGT/basic_upscaler")
  result = client.predict(
    image=handle_file(img_path),
    model_selection="DAT-2 RealWebPhoto X4",
    api_name="/upscale_image"
  )
  webp_path = result[1]
  output_path = img_path.replace('temp', 'images')

  with Image.open(webp_path) as img:
    # 儲存原圖
    img.save(output_path, "WEBP", quality=85)
  os.remove(img_path)
  
  cur_process += 1
  if cur_process >= max_process:
    break


  


