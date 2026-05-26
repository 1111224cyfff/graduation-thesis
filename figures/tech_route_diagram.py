#!/usr/bin/env python3
"""
Generate the technical route diagram for the thesis.
Layout:
- Chapter 1 at top
- Chapter 2 on its own row
- Chapters 3 and 4 side-by-side on one row
- Chapter 5 on its own row
- Chapter 6 at bottom

Within each chapter, secondary sections are arranged horizontally.
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import numpy as np

# Use a Chinese-supporting font
plt.rcParams['font.sans-serif'] = ['SimHei', 'Arial Unicode MS', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

fig, ax = plt.subplots(1, 1, figsize=(18, 12))
ax.set_xlim(0, 18)
ax.set_ylim(0, 12)
ax.axis('off')

# Color scheme
colors = {
    'ch1': '#E8F4FD',  # light blue
    'ch2': '#FFF3E0',  # light orange
    'ch3': '#E8F5E9',  # light green
    'ch4': '#FCE4EC',  # light pink
    'ch5': '#F3E5F5',  # light purple
    'ch6': '#E0F2F1',  # light teal
    'border_ch1': '#0277BD',
    'border_ch2': '#EF6C00',
    'border_ch3': '#2E7D32',
    'border_ch4': '#C2185B',
    'border_ch5': '#7B1FA2',
    'border_ch6': '#00695C',
}

def draw_box(ax, x, y, w, h, text, facecolor, edgecolor, fontsize=9, text_color='black', radius=0.02):
    """Draw a rounded rectangle with text."""
    box = FancyBboxPatch((x, y), w, h,
                         boxstyle=f"round,pad=0.02,rounding_size={radius}",
                         facecolor=facecolor, edgecolor=edgecolor, linewidth=1.5)
    ax.add_patch(box)
    # Wrap text if too long
    ax.text(x + w/2, y + h/2, text, ha='center', va='center',
            fontsize=fontsize, color=text_color, wrap=True,
            linespacing=1.1)
    return box

def draw_chapter_block(ax, left, bottom, width, height, title, sections, color_key, title_h=0.6):
    """Draw a chapter block with title bar and horizontal sections."""
    border_color = colors[f'border_{color_key}']
    face_color = colors[color_key]
    
    # Outer border
    outer = FancyBboxPatch((left, bottom), width, height,
                           boxstyle="round,pad=0.02,rounding_size=0.05",
                           facecolor='white', edgecolor=border_color, linewidth=2)
    ax.add_patch(outer)
    
    # Title bar
    title_box = FancyBboxPatch((left, bottom + height - title_h), width, title_h,
                               boxstyle="round,pad=0.02,rounding_size=0.03",
                               facecolor=border_color, edgecolor=border_color, linewidth=1.5)
    ax.add_patch(title_box)
    ax.text(left + width/2, bottom + height - title_h/2, title,
            ha='center', va='center', fontsize=11, color='white', fontweight='bold')
    
    # Sections area
    sec_bottom = bottom + 0.15
    sec_height = height - title_h - 0.25
    n = len(sections)
    gap = 0.1
    sec_width = (width - gap*(n+1)) / n
    
    for i, sec in enumerate(sections):
        sx = left + gap + i * (sec_width + gap)
        draw_box(ax, sx, sec_bottom, sec_width, sec_height, sec,
                 face_color, border_color, fontsize=8)
    
    return outer

# Layout parameters
margin = 0.5
row_gap = 0.4
ch1_h = 1.0
ch2_h = 2.0
ch34_h = 2.5
ch5_h = 2.0
ch6_h = 1.0

# Compute y positions from top to bottom
total_h = ch1_h + row_gap + ch2_h + row_gap + ch34_h + row_gap + ch5_h + row_gap + ch6_h
y_ch1 = 12 - margin - ch1_h
y_ch2 = y_ch1 - row_gap - ch2_h
y_ch34 = y_ch2 - row_gap - ch34_h
y_ch5 = y_ch34 - row_gap - ch5_h
y_ch6 = y_ch5 - row_gap - ch6_h

full_w = 18 - 2*margin

# Chapter 1: Introduction (full width)
ch1_sections = [
    "1.1 研究背景\n与问题提出",
    "1.2 研究目的\n与意义",
    "1.3 国内外\n研究现状",
    "1.4 文献总结\n与切入点",
    "1.5 主要研究内容\n与技术路线",
]
draw_chapter_block(ax, margin, y_ch1, full_w, ch1_h, "第1章  引言", ch1_sections, 'ch1', title_h=0.45)

# Chapter 2: Sensor System (full width)
ch2_sections = [
    "2.1 系统总体架构\n与硬件选型布置",
    "2.2 多传感器\n外参标定",
    "2.3 通信链路与\n接口规范",
]
draw_chapter_block(ax, margin, y_ch2, full_w, ch2_h, "第2章  吊钩端传感器系统构建与配准", ch2_sections, 'ch2', title_h=0.5)

# Chapters 3 & 4 side by side
ch3_w = full_w * 0.52
ch4_w = full_w * 0.46
gap_34 = full_w - ch3_w - ch4_w

ch3_sections = [
    "3.1 双雷达点云\n实时融合方法",
    "3.2 基于融合点云的\nSLAM定位与静态地图构建",
    "3.3 基于M-detector的\n动态点检测与候选目标状态生成",
]
draw_chapter_block(ax, margin, y_ch34, ch3_w, ch34_h, "第3章  基于融合点云的定位与空间危险区域检测方法", ch3_sections, 'ch3', title_h=0.5)

ch4_sections = [
    "4.1 视觉侧\n高风险目标识别",
    "4.2 雷视\n融合策略",
    "4.3 风险判定与\n分级预警策略",
]
draw_chapter_block(ax, margin + ch3_w + gap_34, y_ch34, ch4_w, ch34_h, "第4章  基于雷视融合的避障预警策略", ch4_sections, 'ch4', title_h=0.5)

# Chapter 5: Experiments (full width)
ch5_sections = [
    "5.1 实验平台与\n测试场景设置",
    "5.2 多传感器\n定位性能实验",
    "5.3 雷视协同\n感知效果分析",
    "5.4 危险区域\n检测效果验证",
    "5.5 系统实时性\n与稳定性验证",
]
draw_chapter_block(ax, margin, y_ch5, full_w, ch5_h, "第5章  实验验证与系统评估", ch5_sections, 'ch5', title_h=0.5)

# Chapter 6: Conclusion (full width)
ch6_sections = [
    "6.1 主要\n研究结论",
    "6.2 创新点\n总结",
    "6.3 不足与\n未来展望",
]
draw_chapter_block(ax, margin, y_ch6, full_w, ch6_h, "第6章  结论与展望", ch6_sections, 'ch6', title_h=0.45)

# Draw arrows between chapters
arrow_style = "Simple, tail_width=0.5, head_width=4, head_length=6"
arrow_color = '#555555'
arrow_lw = 1.2

def draw_arrow(ax, x1, y1, x2, y2):
    ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle="->", color=arrow_color, lw=arrow_lw,
                               connectionstyle="arc3,rad=0"))

# Chapter 1 -> Chapter 2
draw_arrow(ax, 9, y_ch1, 9, y_ch2 + ch2_h)

# Chapter 2 -> Chapter 3 (left side)
draw_arrow(ax, 7, y_ch2, 7, y_ch34 + ch34_h)

# Chapter 2 -> Chapter 4 (right side)
draw_arrow(ax, 11, y_ch2, 11, y_ch34 + ch34_h)

# Chapter 3 -> Chapter 4 (horizontal connection)
draw_arrow(ax, margin + ch3_w, y_ch34 + ch34_h/2, margin + ch3_w + gap_34, y_ch34 + ch34_h/2)

# Chapter 3 -> Chapter 5
draw_arrow(ax, 7, y_ch34, 7, y_ch5 + ch5_h)

# Chapter 4 -> Chapter 5
draw_arrow(ax, 11, y_ch34, 11, y_ch5 + ch5_h)

# Chapter 5 -> Chapter 6
draw_arrow(ax, 9, y_ch5, 9, y_ch6 + ch6_h)

# Save
out_pdf = "/Users/cyf/graduation_thesis/paper/figures/技术路线图_新.pdf"
out_png = "/Users/cyf/graduation_thesis/paper/figures/技术路线图_新.png"
plt.tight_layout(pad=0.5)
plt.savefig(out_pdf, dpi=300, bbox_inches='tight', pad_inches=0.1)
plt.savefig(out_png, dpi=300, bbox_inches='tight', pad_inches=0.1)
print(f"Saved to {out_pdf} and {out_png}")
