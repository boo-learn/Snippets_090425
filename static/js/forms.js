const codeCount = document.getElementById('count');
const textArea = document.querySelector('textarea[name="code"]');
const maxlength = textArea.getAttribute("maxlength");

const formDataKey = "formDataDraft";

const numChars = textArea.value.length;
codeCount.textContent = `${numChars}/${maxlength}`;

textArea.addEventListener('input', () => {
    const numChars = textArea.value.length;
    codeCount.textContent = `${numChars}/${maxlength}`;
})

// 1. Сохранение данных формы (по таймеру)
function saveDraft() {
    const name = document.querySelector('input[name="name"]');
    const lang = document.querySelector('select[name="lang"]');
    const code = document.querySelector('textarea[name="code"]');
    const formData = {
        name: name.value,
        lang: lang.value,
        code: code.value,
    }
    sendMessage("Данные формы сохранены");
    localStorage.setItem(formDataKey, JSON.stringify(formData));
}

// 2. Восстановления (localStorage --> form)
function restoreDraft() {
    const data = localStorage.getItem(formDataKey);
    const formData = JSON.parse(data);
    const name = document.querySelector('input[name="name"]');
    const lang = document.querySelector('select[name="lang"]');
    const code = document.querySelector('textarea[name="code"]');
    name.value = formData.name;
    lang.value = formData.lang;
    code.value = formData.code;
    sendMessage("Данные формы восстановлены");
    localStorage.clear();
}

// 3. Проверки данных формы
function checkDraft() {
    const data = localStorage.getItem(formDataKey);
    if (data) {
        if (confirm("Восстановить данные формы?")) {
            restoreDraft();
        }
    }
}

setInterval(saveDraft, 5000);

document.addEventListener('DOMContentLoaded', function () {
    checkDraft();
});
