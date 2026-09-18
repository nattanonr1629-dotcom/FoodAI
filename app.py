from flask import Flask, render_template, request, jsonify
from openai import OpenAI
from dotenv import load_dotenv
import os
import base64

# =========================
# โหลดค่าจาก .env
# =========================
load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise ValueError("ไม่พบ OPENAI_API_KEY ในไฟล์ .env")

client = OpenAI(api_key=api_key)

# =========================
# สร้าง Flask App
# =========================
app = Flask(__name__)

# จำกัดขนาดไฟล์รูป 10 MB
app.config["MAX_CONTENT_LENGTH"] = 10 * 1024 * 1024


# =========================
# หน้าแรก
# =========================
@app.route("/")
def index():
    return render_template("index.html")


# =========================
# API วิเคราะห์รูปอาหาร
# =========================
@app.route("/analyze", methods=["POST"])
def analyze():

    if "image" not in request.files:
        return jsonify({
            "success": False,
            "error": "กรุณาเลือกรูปอาหาร"
        }), 400

    image = request.files["image"]

    if image.filename == "":
        return jsonify({
            "success": False,
            "error": "กรุณาเลือกรูปอาหาร"
        }), 400

    try:
        # อ่านไฟล์รูป
        image_bytes = image.read()

        # แปลงเป็น Base64
        image_base64 = base64.b64encode(image_bytes).decode("utf-8")

        # ตรวจสอบชนิดไฟล์
        file_type = image.content_type

        prompt = """
วิเคราะห์รูปอาหารนี้และตอบเป็นภาษาไทย

ให้จัดข้อมูลตามหัวข้อต่อไปนี้:

1. 🍽️ ชื่อเมนูอาหาร
2. 🥬 วัตถุดิบที่คาดว่าใช้
3. 👨‍🍳 วิธีทำโดยสรุป
4. 🥗 ข้อมูลโภชนาการโดยประมาณ
5. 💡 เมนูอาหารที่ใกล้เคียง

หากไม่สามารถระบุอาหารจากภาพได้อย่างมั่นใจ
ให้ระบุว่า "ไม่สามารถยืนยันได้จากภาพ"

อย่าสร้างข้อมูลที่ไม่สามารถประเมินจากภาพได้
"""

        # =========================
        # ส่งภาพให้ OpenAI
        # =========================
        response = client.responses.create(
            model="gpt-5.6-luna",
            input=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "input_text",
                            "text": prompt
                        },
                        {
                            "type": "input_image",
                            "image_url": (
                                f"data:{file_type};base64,"
                                f"{image_base64}"
                            )
                        }
                    ]
                }
            ]
        )

        result = response.output_text

        return jsonify({
            "success": True,
            "result": result
        })

    except Exception as e:

        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


# =========================
# จำกัดชนิดไฟล์
# =========================
@app.errorhandler(413)
def file_too_large(error):
    return jsonify({
        "success": False,
        "error": "ไฟล์มีขนาดใหญ่เกิน 10 MB"
    }), 413


# =========================
# เริ่มเซิร์ฟเวอร์
# =========================
if __name__ == "__main__":
    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )

