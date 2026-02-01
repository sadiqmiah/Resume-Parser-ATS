document.addEventListener("DOMContentLoaded", () => {
// Theme toggle
const toggle = document.getElementById("themeToggle");
  if (toggle) {
    toggle.addEventListener("click", () => {
      const current = document.documentElement.getAttribute("data-theme");
      const next = current === "dark" ? "light" : "dark";
      document.documentElement.setAttribute("data-theme", next);
      toggle.textContent = next === "dark" ? "☀️" : "🌙";
    });
  }

// Resume parsing
 const parseBtn = document.getElementById("parseBtn");
  const fileInput = document.getElementById("resumeInput");
  const resultDiv = document.getElementById("result");

  const API_URL = "https://resume-parser-ats-mfj0.onrender.com";

   if (parseBtn) {
    parseBtn.addEventListener("click", async () => {
      if (!fileInput.files.length) {
        resultDiv.textContent = "⚠️ Please upload a PDF resume.";
        return;
      }

    const formData = new FormData();
    formData.append("file", fileInput.files[0]);

    resultDiv.textContent = "⏳ Parsing resume...";

    try {
      const response = await fetch(`${API_URL}/parse`, {
        method: "POST",
        body: formData
      });

      if (!response.ok) {
        const text = await response.text();
        throw new Error(text);
      }

      const data = await response.json();
      renderResult(data);

    } catch (err) {
      console.error(err);
      resultDiv.textContent = "❌ API error. See console.";
    }
  });
 }
});
function renderResult(data) {
  const resultDiv = document.getElementById("result");
  resultDiv.innerHTML = "";

  for (const section in data) {
    const card = document.createElement("div");
    card.className = "json-card";

    const header = document.createElement("div");
    header.className = "json-header";
    header.textContent = section;

    const content = document.createElement("div");
    content.className = "json-content";

    if (Array.isArray(data[section])) {
      data[section].forEach(item => {
        const p = document.createElement("p");
        p.textContent = item;
        content.appendChild(p);
      });
    } else {
      content.textContent = data[section];
    }

    header.addEventListener("click", () => {
      content.classList.toggle("open");
    });

    card.appendChild(header);
    card.appendChild(content);
    resultDiv.appendChild(card);
  }
}
