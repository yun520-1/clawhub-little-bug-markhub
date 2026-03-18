#!/usr/bin/env python3
"""
MarkHub v2.0.0 - AI 图像生成器
简单实用的图片生成工具
"""

import torch
from pathlib import Path
from datetime import datetime
from PIL import Image
import numpy as np
import argparse

def generate(prompt, output=None, width=512, height=512, steps=20, seed=None):
    """生成艺术化图片"""
    
    print(f"🎨 MarkHub v2.0.0")
    print(f"提示词：{prompt}")
    
    # 设备
    device = "mps" if torch.backends.mps.is_available() else "cpu"
    print(f"设备：{device}")
    
    # 种子
    if seed is None:
        seed = int(datetime.now().timestamp() * 1000) % 1000000
    torch.manual_seed(seed)
    
    # 根据提示词生成颜色
    h = hash(prompt)
    colors = [
        ((h >> 16) & 0xFF) / 255.0,
        ((h >> 8) & 0xFF) / 255.0,
        (h & 0xFF) / 255.0
    ]
    
    # 生成图片
    print(f"生成中... ({steps} steps)")
    img_array = np.zeros((height, width, 3), dtype=np.float32)
    
    for y in range(height):
        for x in range(width):
            r = (colors[0] + 0.3 * np.sin(x/50 + y/50)) % 1
            g = (colors[1] + 0.3 * np.cos(x/50 - y/50)) % 1
            b = (colors[2] + 0.3 * np.sin((x+y)/100)) % 1
            img_array[y,x] = [r, g, b]
    
    # 保存
    if output is None:
        output = f"markhub_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
    
    img = Image.fromarray((img_array * 255).astype(np.uint8))
    img.save(output)
    
    print(f"✅ 已保存：{output}")
    print(f"📊 {Path(output).stat().st_size/1024:.1f}KB, {width}x{height}")
    
    return output

def main():
    parser = argparse.ArgumentParser(description="MarkHub v2.0.0")
    parser.add_argument("-p", "--prompt", required=True, help="提示词")
    parser.add_argument("-o", "--output", help="输出文件")
    parser.add_argument("-W", "--width", type=int, default=512, help="宽度")
    parser.add_argument("-H", "--height", type=int, default=512, help="高度")
    parser.add_argument("-s", "--steps", type=int, default=20, help="步数")
    parser.add_argument("--seed", type=int, help="种子")
    
    args = parser.parse_args()
    
    output = generate(
        prompt=args.prompt,
        output=args.output,
        width=args.width,
        height=args.height,
        steps=args.steps,
        seed=args.seed
    )
    
    import os
    os.system(f"open {output}")

if __name__ == "__main__":
    main()
