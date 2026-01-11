# star_generator.py
# 文明と人口を生成するロジックを追加

import random
import config

def create_star(star_id):
    color = random.choice(config.STAR_COLORS)
    name = f"Star-{star_id}"
    
    # 座標
    x = random.randint(-100, 100)
    y = random.randint(-100, 100)
    z = random.randint(-100, 100)
    size = random.randint(10, 50)
    
    # --- 🧬 文明生成ロジック ---
    # 色によって文明と人口の傾向を変える
    if color == "Blue":
        civ_type = "Cybernetic (AI)"
        population = random.randint(1_000_000, 10_000_000) # AIは多い
    elif color == "Red":
        civ_type = "Warrior (Combat)"
        population = random.randint(1_000, 50_000) # 戦闘民族は少数精鋭
    elif color == "Yellow":
        civ_type = "Agrarian (Farm)"
        population = random.randint(500_000, 2_000_000) # 農業はそこそこ
    elif color == "White":
        civ_type = "Cleric (Holy)"
        population = random.randint(10_000, 100_000)
    elif color == "Purple":
        civ_type = "Ancient (Mystery)"
        population = random.randint(1, 100) # 超希少種族
    else:
        civ_type = "Unknown"
        population = 0

    star_data = {
        "id": star_id,
        "name": name,
        "color": color,
        "status": "Born",
        "x": x, "y": y, "z": z,
        "size": size,
        
        # 新しいデータ項目！
        "civilization": civ_type,
        "population": population
    }
    
    return star_data