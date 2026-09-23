const imageInput = document.getElementById("imageInput");
const imagePreview = document.getElementById("imagePreview");
const analyzeButton = document.getElementById("analyzeButton");
const loading = document.getElementById("loading");
const result = document.getElementById("result");

// =========================
// แสดงตัวอย่างรูป
// =========================

imageInput.addEventListener("change", function () {


const file = imageInput.files[0];

if (!file) {
    imagePreview.innerHTML =
        "<p>ยังไม่ได้เลือกรูปอาหาร</p>";
    return;
}

const imageURL = URL.createObjectURL(file);

imagePreview.innerHTML = `
    <img src="${imageURL}" alt="รูปอาหาร">
`;

result.innerHTML =
    "<p>พร้อมวิเคราะห์รูปอาหาร</p>";


});

// =========================
// วิเคราะห์อาหาร
// =========================

analyzeButton.addEventListener("click", async function () {


const file = imageInput.files[0];

if (!file) {
    alert("กรุณาเลือกรูปอาหารก่อน");
    return;
}

// ป้องกันการกดซ้ำ
analyzeButton.disabled = true;

// แสดง Loading
loading.classList.remove("hidden");

result.innerHTML = "";

// สร้าง FormData
const formData = new FormData();

// ต้องตรงกับ request.files["image"] ใน app.py
formData.append("image", file);


try {

    const response = await fetch(
        "/analyze",
        {
            method: "POST",
            body: formData
        }
    );


    const data = await response.json();


    if (data.success) {

        result.innerHTML = `
            <div class="ai-result">
                ${formatResult(data.result)}
            </div>
        `;

    } else {

        result.innerHTML = `
            <p>
                ❌ ${data.error}
            </p>
        `;
    }


} catch (error) {

    result.innerHTML = `
        <p>
            ❌ ไม่สามารถเชื่อมต่อกับเซิร์ฟเวอร์ได้
        </p>
    `;

    console.error(error);

} finally {

    loading.classList.add("hidden");

    analyzeButton.disabled = false;
}


});

// =========================
// จัดรูปแบบผลลัพธ์
// =========================

function formatResult(text) {


return text
    .replace(/\n/g, "<br>")
    .replace(/1\./g, "<br><strong>1.</strong>")
    .replace(/2\./g, "<br><strong>2.</strong>")
    .replace(/3\./g, "<br><strong>3.</strong>")
    .replace(/4\./g, "<br><strong>4.</strong>")
    .replace(/5\./g, "<br><strong>5.</strong>");


}
