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
    // sendMessage("Данные формы сохранены");
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
    discardDraft();
}

// 3. Проверки данных формы
function checkDraft() {
    const data = localStorage.getItem(formDataKey);
    if (data) {
        showRestorePrompt()
    }
}

setInterval(saveDraft, 5000);

function showRestorePrompt() {
    const promptDiv = document.createElement('div');
    promptDiv.className = 'alert alert-info alert-dismissible fade show';
    promptDiv.setAttribute("id", "promptDiv");
    promptDiv.innerHTML = `
        <strong>Найден черновик!</strong> 
        Хотите восстановить сохраненные данные?
        <button type="button" class="btn btn-primary btn-sm ms-2" onclick="restoreDraft()">
            Восстановить черновик
        </button>
        <button type="button" class="btn btn-secondary btn-sm ms-2" onclick="discardDraft()">
            Отменить
        </button>
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;

    // Вставляем после заголовка
    const titleRow = document.querySelector('.row:first-child');
    titleRow.parentNode.insertBefore(promptDiv, titleRow.nextSibling);
}

function discardDraft() {
    localStorage.removeItem(formDataKey);

    // Удаляем prompt если он есть
    const alertElement = document.querySelector('#promptDiv');
    if (alertElement) {
        alertElement.remove();
    }
}

document.addEventListener('DOMContentLoaded', function () {
    checkDraft();
});
