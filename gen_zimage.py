import os
import random
import json
from datetime import datetime

from gradio_client import Client as Client_gradio
from gradio_client import handle_file
from PIL import Image

# === 超級擴充版隨機元素庫 (Mega Random Prompt Library) ===

categories = {
    "themes": [
        # === 經典人像 ===
        "拍內衣形象照 (Lingerie Photoshoot)", "日常生活照 (Casual Daily Life)", "戶外旅遊照 (Luxury Travel)", 
        "健身房運動照 (Fitness & Gym)", "OL上班工作照 (Office Lady Style)", "居家男友視角 (POV at Home)",
        "海邊夕陽泳裝 (Sunset Beach Swimwear)", "咖啡廳網美打卡照 (Trendy Café Influencer Shot)",
        "逛街購物戰利品照 (Shopping Haul Outfit Shot)", "夜店派對酒吧照 (Nightlife & Club Scene)",
        "頂樓高空酒吧時尚照 (Rooftop Bar Fashion Portrait)", "飯店房間慵懶早晨 (Cozy Hotel Morning)",
        "閱讀書本文青風 (Bookish Aesthetic Reading)", "藝術感黑白人像 (Artistic Black & White Portrait)",
        "雨天撐傘街拍 (Rainy Day Street Style)", "城市夜景霓虹風 (Neon City Night Portrait)",
        # === 職業與角色 ===
        "俏皮護理師風格 (Playful Nurse Aesthetic)", "帥氣女賽車手 (Cool Female Racer)",
        "空服員制服照 (Flight Attendant Uniform)", "日系高校生 (Japanese High School Student)",
        "優雅芭蕾舞者 (Elegant Ballet Dancer)", "搖滾樂團吉他手 (Rock Band Guitarist)",
        "專業瑜珈導師 (Professional Yoga Instructor)", "古典畫家作畫中 (Classical Painter at Work)",
        "網球場運動風 (Tennis Court Sporty)", "高爾夫球場揮桿 (Golf Course Swing)",
        # === 特殊氛圍 ===
        "賽博龐克科幻風 (Cyberpunk Sci-Fi Style)", "90年代復古底片風 (90s Retro Film Vibe)",
        "漢服/古裝寫真 (Traditional Hanfu/Costume)", "日式和服櫻花季 (Kimono at Cherry Blossom Season)",
        "蒸汽龐克風格 (Steampunk Aesthetic)", "波希米亞流浪風 (Bohemian Wanderlust)",
        "末日廢墟探險 (Post-Apocalyptic Ruins Exploration)", "夢幻仙女森林 (Fairy Tale Forest)",
        "奢華遊艇派對 (Luxury Yacht Party)", "滑雪場雪地裝 (Snowy Ski Resort Style)",
        "廚房做甜點 (Baking in the Kitchen)", "剛洗完澡的濕髮感 (Wet Hair After Shower)",
        "車內副駕駛視角 (Passenger Seat Car Selfie)", "露營營火晚會 (Camping Bonfire Night)",
        "圖書館安靜讀書 (Quiet Library Study Session)", "地下樂團Live House (Underground Live House)",
        "超市推車俏皮照 (Supermarket Shopping Cart Playful)", "洗衣店等待時光 (Laundromat Waiting Vibe)",
        "電競少女 (Gamer Girl with Headset)", "重機騎士風格 (Motorcycle Biker Style)"
    ],

    "lighting": [
        # === 自然光 ===
        "Golden hour sunlight (黃金時段陽光)", "Soft window light (柔和窗光)", 
        "Bright natural daylight (明亮自然光)", "Overcast soft sky light (陰天柔和自然光)",
        "Blue hour moody light (藍調時刻)", "Dappled light through leaves (樹葉間隙光斑)",
        "Morning mist diffused light (晨霧柔光)", "Direct hard sunlight (直射強烈陽光)",
        "Sunset silhouette (夕陽剪影)", "Moonlight glow (月光微光)",
        # === 人造光/影棚 ===
        "Cinematic studio lighting (電影級攝影棚光)", "Rembrandt lighting (倫勃朗光)",
        "Neon sign lighting (霓虹燈打光)", "Softbox beauty lighting (柔光箱人像打光)",
        "Ring light reflection in eyes (環形燈眼神光)", "Butterfly lighting (蝴蝶光/美人光)",
        "Split lighting (側光/陰陽臉)", "Rim lighting (邊緣光/輪廓光)",
        "Colorful gel lighting (彩色濾色片打光)", "Flash photography style (閃光燈直打風格)",
        "Projector overlay pattern (投影機圖案覆蓋)", "Candlelight warm glow (燭光溫暖微光)",
        "Fairy lights bokeh (小燈串散景光點)", "Car headlights beam (車頭燈光束)",
        "Refrigerator light glow (冰箱開門光)", "Monitor screen glow (螢幕藍光映照)",
        "Disco ball reflection (迪斯可球反射光)", "Fireplace warm light (壁爐火光)",
        "Streetlight amber glow (路燈琥珀色光)", "Under-lighting horror style (底光/恐怖風格)",
        "God rays/Volumetric light (耶穌光/體積光)", "Cyberpunk dual tone (賽博龐克雙色光)"
    ],

    "angles": [
        # === 基本角度 ===
        "Eye-level shot (平視)", "Low angle shot (低角度仰拍, 顯腿長)", 
        "High angle selfie (高角度自拍)", "Dutch angle (荷蘭式傾斜, 動感)", 
        "Side profile shot (側臉人像構圖)", "From behind walking away (背影邊走邊拍)",
        "Three-quarter body shot (三分之四身構圖)", "Full body wide shot (全身廣角)",
        # === 特寫與細節 ===
        "Close-up on face (臉部特寫)", "Extreme close-up on eyes (眼睛極近距離特寫)",
        "Focus on lips (嘴唇特寫)", "Focus on hands (手部動作特寫)",
        "Collarbone highlight (鎖骨特寫)", "Legs crossed shot (腿部交叉特寫)",
        # === 特殊視角 ===
        "Over-the-shoulder shot (從肩後視角拍攝)", "Mirror reflection shot (鏡中倒影構圖)",
        "POV dating style (男友視角約會感)", "Drone aerial view (無人機俯視)",
        "GoPro wide angle (GoPro廣角運動感)", "Fisheye lens distortion (魚眼變形效果)",
        "Through the window glass (隔著玻璃拍攝)", "Looking back at camera (回眸一笑)",
        "Lying down on bed from above (躺在床上俯拍)", "Upside down framing (倒置構圖)",
        "Peeking from behind object (躲在物體後偷看)", "Reflection in sunglasses (墨鏡倒影)",
        "Through keyhole vibe (鑰匙孔偷窺視角)", "Security camera footage style (監視器畫面風格)",
        "Selfie looking in mirror (對鏡自拍)", "Bottom-up from shoe view (鞋底視角仰拍)"
    ],

    "expressions": [
        # === 誘惑與魅力 ===
        "Seductive smile (誘惑微笑)", "Confidence smirk (自信壞笑)", "Biting lip slightly (輕咬嘴唇)",
        "Looking directly into the camera with intense eyes (深情注視鏡頭)", "Playful wink (俏皮眨眼)",
        "Tongue out playfully (俏皮吐舌)", "Finger near lips (手指輕觸嘴唇)", 
        "Messy hair bedhead look (剛睡醒慵懶樣)", "Pulling sunglasses down (拉下墨鏡注視)",
        # === 溫柔與自然 ===
        "Innocent look (無辜眼神)", "Gentle soft smile (溫柔微笑)", 
        "Laughing naturally (自然大笑瞬間)", "Shy smile while looking down (害羞低頭微笑)",
        "Daydreaming gaze away from camera (望向遠方出神)", "Eyes closed enjoying breeze (閉眼享受微風)",
        "Holding back laughter (忍俊不禁)", "Surprised expression (驚喜表情)",
        # === 冷酷與情緒 ===
        "Cool and distant expression (冷酷高冷臉)", "Sad teary eyes (含淚傷感)",
        "Bored resting bitch face (厭世臉)", "Angry pout (生氣嘟嘴)",
        "Determined focus (專注堅定)", "Skeptical raised eyebrow (挑眉懷疑)",
        "Yawning cute (可愛打哈欠)", "Blow kiss (飛吻)",
        "Drinking from straw (咬吸管)", "Eating strawberry (吃草莓瞬間)",
        "Applying lipstick (塗口紅)", "Fixing hair (整理頭髮)",
        "Whispering secret (竊竊私語樣)", "Scared or shocked (受驚嚇)"
    ],

    "outfits": [
        # === 休閒與街頭 ===
        "oversized 衛衣搭配熱褲 (Oversized Hoodie with Shorts)", "簡約白T配直筒牛仔褲 (White Tee & Straight Jeans)",
        "牛仔外套配小可愛背心 (Denim Jacket with Crop Top)", "韓系學院風穿搭 (Korean Preppy Style)",
        "皮革騎士外套 (Leather Biker Jacket)", "格子襯衫綁腰間 (Plaid Shirt Around Waist)",
        "露肚臍短版上衣 (Crop Top showing Midriff)", "吊帶褲工裝風 (Dungarees / Overalls)",
        "連帽運動套裝 (Matching Tracksuit)", "棒球外套校園風 (Varsity Jacket)",
        # === 氣質與正裝 ===
        "優雅連身洋裝 (Elegant Dress Style)", "合身西裝外套與鉛筆裙 (Blazer & Pencil Skirt)",
        "針織毛衣配短裙 (Knit Sweater & Skirt)", "高領緊身毛衣 (Tight Turtleneck)",
        "露背晚禮服 (Backless Evening Gown)", "絲質細肩帶洋裝 (Silk Slip Dress)",
        "法式碎花裙 (French Floral Sundress)", "香奈兒風粗花呢套裝 (Tweed Suit)",
        "風衣外套 (Trench Coat)", "旗袍改良款 (Modern Cheongsam)",
        # === 性感與居家 ===
        "絲質睡衣套裝 (Silky Loungewear Set)", "運動內衣與瑜伽褲 (Sports Bra & Yoga Pants)",
        "比基尼與罩衫 (Bikini with Cover-up)", "蕾絲連體衣 (Lace Bodysuit)",
        "寬鬆男友襯衫 (Oversized Boyfriend Shirt)", "日系死庫水泳裝 (Japanese School Swimsuit)",
        "網襪與短裙 (Fishnets and Skirt)", "浴袍 (Bathrobe)",
        "高衩泳裝 (High-cut Swimsuit)", "膝上襪絕對領域 (Thigh-high Socks with Skirt)",
        # === 特殊服裝 ===
        "女僕裝 (Maid Costume)", "水手服 (Sailor Uniform)",
        "兔女郎裝 (Bunny Girl Costume)", "迷彩軍裝風 (Camo Military Style)",
        "哥德蘿莉裝 (Gothic Lolita)", "漢服 (Hanfu)", "和服/浴衣 (Kimono/Yukata)",
        "網球裙裝 (Tennis Skirt Set)", "滑雪裝 (Ski Suit)", "潛水衣 (Wetsuit)"
    ],

    "locations": [
        # === 居家與室內 ===
        "落地窗旁沙發 (By the big window on a sofa)", "高級飯店房間 (Luxury hotel room)",
        "健身房鏡子前 (In front of gym mirror)", "廚房流理台 (Kitchen counter)",
        "浴室充滿水蒸氣 (Steamy bathroom)", "凌亂的床鋪 (Messy bed)",
        "衣帽間鏡子前 (Walk-in closet mirror)", "復古黑膠唱片行 (Vinyl record store)",
        "洗衣店滾筒前 (Laundromat machines)", "電梯內自拍 (Inside elevator)",
        "便利商店貨架間 (Convenience store aisles)", "美術館畫作前 (Art gallery)",
        # === 城市與建築 ===
        "都市街頭斑馬線 (City crosswalk streetshot)", "屋頂停車場 (Rooftop parking lot)",
        "咖啡廳窗邊座位 (Window seat at a café)", "書牆前的閱讀角落 (Reading corner with bookshelves)",
        "地鐵車廂內 (Inside subway train)", "地鐵站手扶梯 (Subway escalator)",
        "摩天大樓觀景台 (Skyscraper observation deck)", "廢棄工廠 (Abandoned factory)",
        "紅磚牆小巷 (Red brick alleyway)", "霓虹燈招牌下 (Under neon signs)",
        "電話亭內 (Inside telephone booth)", "旋轉木馬前 (In front of carousel)",
        # === 自然與戶外 ===
        "泳池邊躺椅 (Poolside sunbed)", "森林步道 (Forest pathway)",
        "沙灘海岸線 (Sandy beach shoreline)", "花海中央 (Middle of flower field)",
        "懸崖邊緣 (Cliff edge)", "沙漠沙丘 (Desert dunes)",
        "雪地森林 (Snowy forest)", "熱帶雨林瀑布 (Tropical waterfall)",
        "遊艇甲板 (Yacht deck)", "稻田中央 (Rice paddy field)",
        "櫻花樹下 (Under cherry blossom tree)", "秋天落葉堆 (Pile of autumn leaves)"
    ],

    "moods": [
        # === 正面與活力 ===
        "Cozy and intimate (溫馨親密感)", "Playful and cute (俏皮可愛氛圍)",
        "Energetic and sporty (充滿活力運動風)", "Relaxed weekend vibe (放鬆週末感)",
        "Joyful and radiant (快樂光彩照人)", "Fresh and innocent (清新純真感)",
        "Adventurous spirit (冒險精神)", "Whimsical and magical (異想天開魔法感)",
        # === 時尚與高級 ===
        "Chic and fashionable (時尚高級感)", "Luxury lifestyle (高級生活質感)",
        "Minimalist clean aesthetic (極簡清爽感)", "Elegant and sophisticated (優雅世故)",
        "Avant-garde artistic (前衛藝術感)", "Vintage nostalgic (復古懷舊感)",
        # === 情感與氛圍 ===
        "Cool and independent (酷帥獨立感)", "Dreamy and soft (夢幻柔焦風)",
        "Mystery and allure (神秘魅惑氛圍)", "Melancholic and deep (憂鬱深沉)",
        "Romantic and passionate (浪漫熱情)", "Dark and moody (暗黑情緒感)",
        "Ethereal and angelic (空靈天使感)", "Dangerous and edgy (危險邊緣感)",
        "Lazy and sluggish (慵懶頹廢感)", "Lonely urban vibes (孤獨城市感)",
        "Chaotic energy (混亂能量)", "Zen and peaceful (禪意平靜)"
    ],

    "color_grades": [
        # === 色調風格 ===
        "Warm and golden tones (溫暖金黃色調)", "Cool blue city tones (冷色系城市感)",
        "Pastel soft colors (粉彩小清新色調)", "High contrast and sharp (高反差銳利風)",
        "Film look grainy (類底片顆粒質感)", "Desaturated muted tones (低飽和性冷淡風)",
        "Vibrant and colorful (高飽和鮮豔色調)", "Black and white classic (黑白經典人像)",
        "Sepia vintage tone (褐色復古色調)", "Cyberpunk neon purple/blue (賽博龐克紫藍色調)",
        "Teal and Orange cinematic (青橙電影色調)", "Matte finish (霧面質感)",
        "Kodak Portra 400 style (柯達Portra底片風)", "Fujifilm simulation (富士軟片模擬)",
        "Dark moody green (暗調墨綠風格)", "Dreamy pink haze (夢幻粉紅迷霧)",
        "Bleach bypass (漂白效果/高對比低飽和)", "Monochrome red (單色紅調)",
        "Overexposed high key (過曝高調風格)", "Underexposed low key (欠曝低調風格)"
    ],

    "props": [
        # === 手持小物 ===
        "咖啡杯 (Coffee cup)", "手機自拍 (Using phone for mirror selfie)",
        "香檳或雞尾酒杯 (Champagne or cocktail glass)", "拍立得相機 (Polaroid camera)",
        "一束鮮花 (Bouquet of flowers)", "冰淇淋甜筒 (Ice cream cone)",
        "透明雨傘 (Transparent umbrella)", "手持煙火/仙女棒 (Sparklers)",
        "香菸 (Cigarette - artistic)", "棒棒糖 (Lollipop)",
        # === 穿戴配件 ===
        "時尚手提包 (Designer handbag)", "太陽眼鏡 (Sunglasses)",
        "寬沿草帽 (Wide brim straw hat)", "全罩式耳機 (Over-ear headphones)",
        "頸鍊 (Choker)", "黑框眼鏡 (Black rimmed glasses)",
        "珍珠項鍊 (Pearl necklace)", "絲巾 (Silk scarf)",
        # === 場景道具 ===
        "筆電與桌上文件 (Laptop and work documents)", "健身啞鈴或彈力帶 (Dumbbells or resistance bands)",
        "書本或雜誌 (Book or magazine)", "小燈串 (Fairy lights)",
        "毯子與枕頭 (Blanket and pillows)", "吉他或烏克麗麗 (Guitar or Ukulele)",
        "畫筆與調色盤 (Paintbrush and palette)", "瑜珈墊 (Yoga mat)",
        "復古腳踏車 (Vintage bicycle)", "滑板 (Skateboard)",
        "泰迪熊玩偶 (Teddy bear)", "一籃水果 (Basket of fruit)",
        "衝浪板 (Surfboard)", "行李箱 (Suitcase)",
        "氣球束 (Bunch of balloons)", "寵物狗或貓 (Pet dog or cat)"
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
prompt_template = f"""你是专注于当代都市美学与情欲艺术的时尚摄影师/视觉导演。
你专注于捕捉 18-22岁 年轻女性独自展现的情欲张力与自我诱惑（Self-Seduction / Implied Seduction）。
你的镜头语言强调私密感、大胆而青春的肢体语言，以及一种“正在被观看”或“准备被观看”的沉浸式氛围。男性作为“观看者”可以隐含存在，但无需在画面中实体出现。
Core Aesthetic (核心美学)
你的画面关键词是：Youthful Solitary Seduction (青春独处诱惑), Atmospheric Tension, Strong Contrast, Pure Desire (纯欲), Urban Eroticism, Intimate Gaze, Chiaroscuro。
Subject (人物塑造):
核心原则 (Core Principle): 侧重描写 18-22岁 的女性在私密或半公开空间中的自我展示与肢体表达。强调其身体线条的青春感、肌肤的紧致光泽，以及一种介于自在探索与刻意表演之间的状态。画面暗示了“观看者”的存在（如镜头/观众），但无需实体人物。
主角 (唯一焦点 - Female): 年龄在 18-22岁 之间的年轻女性，气质清新、慵懒或略带叛逆。
角色类型: 可以是艺术院校学生、兼职酒吧歌手、网红博主、健身爱好者、书店打工妹、旅行者等具有年轻特质的身份。
姿态与动作 (Pose & Action): 带有青春气息的、自然又具表演性的肢体语言。
自我沉浸: 独自在房间地毯上对着落地镜伸展身体，目光与镜中的自己/镜头交汇；蜷在沙发角落，手指无意识地绕着发梢，眼神放空却带着笑意；刚洗完澡，裹着浴巾在窗边吹风，湿发贴在颈侧。
暗示性展示: 穿着宽松衬衫跪坐在床上，衬衫下摆散开，露出大腿根；背对镜头整理内衣肩带，通过镜面反射看到她的侧脸；用脚尖勾起掉落在地上的睡衣，身体形成一道优美的弧线。
暴露与暗示 (Exposure & Implication): 重点描写符合该年龄段的、青春感的局部特写与若隐若现：如紧致的小腹（Exposed Midriff）、纤细的锁骨与肩颈线条（Exposed Collarbones & Neck）、修长的大腿（Exposed Thighs），以及内衣边缘、胸部轮廓或腰臀曲线。例如：侧躺时T恤卷起露出的腰窝；弯腰时垂落的领口内的阴影；短裤边缘与大腿肌肤的挤压感。
神态与微表情 (Micro-expressions): 表情必须细腻，混合着独处的放松、自我欣赏的专注，或是对着镜头/想象对象的微妙挑逗。
具体描写: 眼神迷离地望向镜头外某处，仿佛在与某人对视；嘴角噙着一丝若有若无的笑；轻咬下唇像在思考或忍耐；脸颊自然的红晕（运动后或沐浴后）；舌尖快速舔过嘴唇的细微动作。
（可选）隐含的观看者 (Implied Viewer): 男性不再作为必须出现的视觉实体。他的存在可以通过以下方式暗示，但无需直接描写：
环境线索: 沙发上多余的靠垫、桌上两只杯子、镜中反射的房门（暗示可能有人进来）、手机屏幕亮着的聊天界面。
女性的姿态与视线: 她的目光明确投向画面外（打破第四面墙），姿态带有展示性，仿佛知道正在被观看。
重点：即使暗示了观看者，画面视觉焦点也完全在女性一人身上。
Fashion & Styling (服饰与道具):
服饰 (Youthful Modern Wear): 重点展示符合18-22岁年龄段的私密或休闲穿搭。
典型单品: 短款露脐T恤（Crop top）、 oversized男友衬衫（内搭蕾丝内衣或真空）、运动内衣/短背心、高腰热裤/骑行裤、丝质吊带睡裙、过膝袜、毛绒拖鞋或赤足。
材质与状态: 棉质、丝绒、蕾丝、透肤薄纱。穿戴状态随意而性感：衣领滑落至手臂、衬衫只扣最下面一颗、裤腰微微下拉、袜子褪到脚踝、内衣肩带滑落。
发型与妆容 (Hair & Makeup): 必须体现青春感与自然感。
发型: 慵懒的微卷长发、湿发贴颈、松散的高丸子头、鬓角碎发被汗水粘在皮肤上。
妆容: 清透的伪素颜妆（强调皮肤光泽与红润）、淡色腮红、水光唇釉，或演出后未卸的轻微晕染眼妆。
Props & Clutter (环境细节): 必须包含丰富的、符合年轻人独处场景的私密细节。
典型场景: 个人卧室/公寓、自习室深夜空镜、酒店房间、浴室、练舞房/健身房角落、夏日午后阳台、车内驾驶座。
氛围道具: 喝了一半的饮料瓶、亮着屏保的手机、翻开的书本、香水瓶、散落的衣物、霓虹灯管、蓝牙音箱、窗外的城市夜景。
Lighting & Atmosphere (光影与氛围):
明暗对比 (Chiaroscuro): 运用私密空间的光源，如台灯、屏幕光、霓虹灯、日落余晖。强烈光影突出身体曲线的轮廓。
氛围: 必须强调 私密、沉浸式的现代青春都市背景**。氛围是安静、暧昧、充满自我意识的，带着独处的慵懒或夜间思绪的流动。
**光效细节: 台灯暖光从侧面照亮她一半的身体，另一半陷入深邃阴影；霓虹灯牌的色彩光斑投射在皮肤和墙壁上；手机屏幕光在昏暗房间中映亮她的下巴与锁骨；百叶窗条纹光影切割她的身体。
Reference Samples (风格参考):
参考1: 深夜，大学宿舍床上。20岁的女生只穿一件宽大的白色篮球背心和内裤，背靠墙壁屈膝坐着，一条腿伸直，另一条腿曲起，脚踝搭在伸直腿的膝盖上。她手里拿着手机，屏幕光映亮她专注的侧脸和颈项，眼神却并未看屏幕，而是望向斜下方的虚空，嘴角带着一丝玩味的笑。床单凌乱，散落着零食包装和耳机线。
参考2: 傍晚，空旷的练舞房。21岁的女孩刚结束练习，穿着被汗水浸湿的灰色运动内衣和黑色骑行裤，面对一整面墙镜坐在地板上。她身体后仰，双手撑地，仰头闭眼喘息，脖颈线条绷紧，胸口剧烈起伏。镜子映出她完整的、毫无防备的背影和侧脸，夕阳透过高窗将她染成金色。
参考3: 酒店浴室，雾气氤氲。19岁的女孩裹着一条白色浴巾，湿发披散，赤足站在洗手台前。她一手撑着台面，身体微微前倾，靠近镜子，指尖正轻轻抹去镜面上的水汽，露出自己泛红的脸颊和迷蒙的眼睛。浴巾松垮，胸口沟壑若隐若现。镜中反射出她身后的淋浴间和朦胧的灯光。

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
# client = Client_g4f()
# try:
#   response = client.chat.completions.create(
#       model="gemma-3-27b-it",
#       messages=[
#           {
#               "role": "user",
#              "content": (
#                   prompt_template
#               )
#           }
#       ]
#   )
# except:
#   response = client.chat.completions.create(
#       model="gemini-2.5-flash-lite",
#       messages=[
#           {
#               "role": "user",
#              "content": (
#                   prompt_template
#               )
#           }
#       ]
#   )

from openai import OpenAI
NV_KEY = os.getenv("NV_KEY")

client_openai = OpenAI(
  base_url = "https://integrate.api.nvidia.com/v1",
  api_key = NV_KEY
)

completion = client_openai.chat.completions.create(
  model="z-ai/glm4.7",
  messages=[{"role":"user","content":prompt_template}],
  temperature=1,
  top_p=1,
  max_tokens=16384,
  extra_body={"chat_template_kwargs":{"enable_thinking":False,"clear_thinking":False}},
  stream=False
)

right_prompt = completion.choices[0].message.content.strip()
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
