import streamlit as st
from html import escape
import os
import base64
st.set_page_config(page_title="幼儿园活动计划", layout="wide")

# Streamlit 页面整体使用楷体
st.markdown(
    """
    <style>
    html, body, [class*="css"], [data-testid="stAppViewContainer"],
    [data-testid="stHeader"], [data-testid="stSidebar"],
    input, textarea, button, select, label, p, div, span {
        font-family: "KaiTi", "楷体", "STKaiti", serif !important;
    }
    textarea, input {
        font-size: 16px !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("假期活动教案")
st.caption("幼儿园活动计划")
st.info("字体提示：楷体。若电脑未安装楷体，浏览器可能改用后备字体。")

# ===== 可修改的基本资料 =====
col1, col2 = st.columns(2)
with col1:
    centre_class = st.selectbox("班级", ["豆豆班", "幼小班", "幼儿班"],width=200)
    plan_month = st.selectbox("假期教案月份", ["三月", "六月", "九月", "十二月"],width=200)
    category = st.text_input("活动主题",width=300)
    activity_name = st.text_input("活动名称",width=300)
with col2:
    duration = st.number_input("活动时间（分钟）", min_value=1, max_value=180, value=30,width=150)
    activity_no = st.selectbox("活动序号", ["活动1", "活动2", "活动3","活动4","活动5","活动6","活动7","活动8","活动9",
    "活动10","活动11","活动12","活动13","活动14","活动15","活动16","活动17","活动18","活动19","活动20"],width=150)
    skill = st.selectbox(
        "必要生活技能",
        ["专注力与自控能力", "换位思考", "沟通能力", "建立联系", "思辨能力", "接受挑战", "自主学习、参与式学习"],width=300
    )
    executivefunction = st.selectbox("执行功能",["工作记忆","抑制控制","认知弹性"],width=200)

st.divider()
st.subheader("活动目标")
objectives_text = st.text_area(
    "幼儿能够（每行填写一个目标）",
    value="1.    \n2.    \n3.    ",
    height=130,width=1200
)

st.subheader("活动准备")
preparation_text = st.text_area("儿歌／材料／教具", value="", height=120)

st.subheader("活动过程")
intro_text = st.text_area("一、活动导入（5分钟）", value="", height=140)
presentation_text = st.text_area("二、活动环节（20分钟）", value="", height=190)
summary_text = st.text_area("三、活动结束（5分钟）", value="", height=120)

st.subheader("活动拓展")
extension_text = st.text_area("家园合作／户外学习／其他延伸活动", value="", height=100)
safety_text = st.text_area("安全注意事项（可选）", value="", height=90)


def text_to_html(value: str) -> str:
    """转义输入内容并保留换行，避免输入文字被当成 HTML。"""
    return "<br>".join(escape(line) for line in value.splitlines()) or "&nbsp;"


def make_print_html() -> str:
    objectives = [line.strip() for line in objectives_text.splitlines() if line.strip()]
    if objectives:
        objectives_html = "".join(
            f"<tr><td class='num'>{i}</td><td>{text_to_html(item)}</td></tr>"
            for i, item in enumerate(objectives, 1)
        )
    else:
        objectives_html = "<tr><td colspan='2'>&nbsp;</td></tr>"

    safe_class = escape(centre_class)
    safe_month = escape(plan_month)
    safe_category = escape(category) or "&nbsp;"
    safe_activity = escape(activity_name) or "&nbsp;"
    safe_duration = escape(str(duration))
    safe_no = escape(activity_no)
    safe_skill = escape(skill)
    safe_executivefunction  = escape(executivefunction)
    
    # 自动读取同目录下的 pcf.png 并转换为 Base64
    img_base64 = ""
    if os.path.exists("pcf.png"):
        with open("pcf.png", "rb") as f:
            encoded = base64.b64encode(f.read()).decode()
            img_base64 = f"data:image/png;base64,{encoded}"

    # 返回完整的 HTML（包含右上角图标、独立格子的班级/主题、以及所有教案内容）
    return f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>幼儿园活动计划 - {safe_month}{safe_no}</title>
<style>
    @page {{ size: A4; margin: 15mm; }}
    * {{ box-sizing: border-box; font-family: "KaiTi", "楷体", "STKaiti", serif !important; }}
    body {{ color: #111; font-size: 12pt; line-height: 1.55; margin: 0; }}
    h1 {{ text-align: center; font-size: 18pt; margin: 0 0 4mm; font-weight: bold; }}
    .code {{ text-align: center; margin-bottom: 5mm; font-size: 11pt; }}
    .meta {{ width: 100%; border-collapse: collapse; margin-bottom: 5mm; }}
    .meta td {{ border: 1px solid #333; padding: 7px 9px; vertical-align: top; width: 50%; }}
    .section-title {{ font-size: 14pt; font-weight: bold; margin: 5mm 0 2mm; }}
    table {{ border-collapse: collapse; width: 100%; }}
    .objectives td, .content-table td {{ border: 1px solid #333; padding: 7px 9px; vertical-align: top; }}
    .objectives .num {{ width: 12mm; text-align: center; }}
    .label {{ width: 30mm; font-weight: bold; white-space: nowrap; }}
    .content {{ min-height: 12mm; overflow-wrap: anywhere; }}
    .footer {{ margin-top: 5mm; font-size: 10pt; }}
    
    /* 右上角图标样式 */
    .top-right-icon {{
        position: absolute;
        top: 10px;
        right: 10px;
        width: 45px;
        height: 45px;
        z-index: 9999;
    }}

    @media screen {{ body {{ max-width: 190mm; margin: 12mm auto; padding: 10mm; border: 1px solid #ccc; }} }}
    @media print {{ body {{ width: auto; margin: 0; padding: 0; border: 0; }} .no-print {{ display: none !important; }} tr, td {{ break-inside: avoid; }} }}
</style>
</head>
<body>

<!-- 右上角图标 -->
<img src="{img_base64}" alt="Logo" class="top-right-icon">

<div class="no-print" style="text-align:right;margin-bottom:10px;">
  <button onclick="window.print()" style="font-size:12pt;padding:7px 14px;cursor:pointer;">打印／另存为 PDF</button>
</div>
<h1>假期活动教案</h1>
<div class="code">{safe_month}假期活动 ｜ 活动序号：{safe_no}</div>

<table class="meta">
  <tr>
    <td><b>班级：</b>{safe_class}</td>
    <td><b>活动主题：</b>{safe_category}</td>
  </tr>
  <tr><td><b>活动名称：</b>{safe_activity}</td><td><b>活动时间：</b>{safe_duration} 分钟</td></tr>
  <tr><td colspan="2"><b>必要生活技能：</b>{safe_skill}</td></tr>
  <tr><td colspan="2"><b>执行功能：</b>{safe_executivefunction}</td></tr>
</table>

<div class="section-title">活动目标</div>
<table class="objectives">{objectives_html}</table>
<div class="section-title">活动准备</div>
<table class="content-table"><tr><td class="content">{text_to_html(preparation_text)}</td></tr></table>
<div class="section-title">活动过程</div>
<table class="content-table">
  <tr><td class="label">一、活动导入</td><td class="content">{text_to_html(intro_text)}</td></tr>
  <tr><td class="label">二、活动环节</td><td class="content">{text_to_html(presentation_text)}</td></tr>
  <tr><td class="label">三、活动结束</td><td class="content">{text_to_html(summary_text)}</td></tr>
</table>
<div class="section-title">活动拓展</div>
<table class="content-table"><tr><td class="content">{text_to_html(extension_text)}</td></tr></table>
<div class="section-title">安全注意事项</div>
<table class="content-table"><tr><td class="content">{text_to_html(safety_text)}</td></tr></table>
</body>
</html>'''
st.divider()
st.subheader("生成打印版")
st.write("点击下载后，按 Ctrl + P 打印或选择‘另存为 PDF’。打印页面将优先使用楷体。")

# 生成教案的 HTML 内容
html_output = make_print_html()

# 将 HTML 内容转为 Base64 格式，以便通过图片超链接触发下载
b64_html_content = base64.b64encode(html_output.encode("utf-8")).decode()
filename = f"{plan_month}假期教案_楷体打印版.html"

# 读取绿色下载按钮图片 (请确保你的图片文件名为 download_icon.png 并且和 py 文件在同目录下)
btn_img_base64 = ""
if os.path.exists("download_icon.png"):
    with open("download_icon.png", "rb") as f:
        encoded_btn = base64.b64encode(f.read()).decode()
        btn_img_base64 = f"data:image/png;base64,{encoded_btn}"

# 渲染自定义的图片下载按钮
if btn_img_base64:
    download_link_html = f"""
    <div style="text-align: center; margin: 15px 0;">
        <a href="data:text/html;charset=utf-8;base64,{b64_html_content}" download="{filename}" title="点击下载教案">
            <img src="{btn_img_base64}" alt="下载教案" style="width: 140px; height: auto; cursor: pointer; border-radius: 6px; transition: transform 0.2s;" onmouseover="this.style.transform='scale(1.05)'" onmouseout="this.style.transform='scale(1)'">
        </a>
    </div>
    """
    st.markdown(download_link_html, unsafe_allow_html=True)
else:
    st.warning("未找到名为 'download_icon.png' 的下载按钮图片，请确认它与 Python 脚本在同一目录下。")
