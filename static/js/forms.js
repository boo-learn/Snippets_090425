const codeCount = document.getElementById('count');
const textArea = document.querySelector('textarea[name="code"]');
const maxlength = textArea.getAttribute("maxlength");

const numChars = textArea.value.length;
codeCount.textContent = `${numChars}/${maxlength}`;

textArea.addEventListener('input', () => {
    const numChars = textArea.value.length;
    codeCount.textContent = `${numChars}/${maxlength}`;
})