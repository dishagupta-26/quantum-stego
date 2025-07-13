console.log("💡 Send.js loaded");

  const form = document.getElementById('sendForm');
  const fileInput = document.getElementById('imageInput');
  const msgInput = document.getElementById('secretMessage');
  const status = document.getElementById('statusMessage');

  document.getElementById('encodeBtn').addEventListener('click', async e => {

    status.textContent = 'Encoding image… please wait.';

    if (!fileInput.files.length || !msgInput.value.trim()) {
      status.textContent = 'Please select an image and enter a message.';
      return;
    }

    const formData = new FormData();
    formData.append('image', fileInput.files[0]);
    formData.append('message', msgInput.value);

try {
  const response = await fetch('https://quantum-stego.onrender.com/encode', {
    method: 'POST',
    body: formData
  });

  const contentType = response.headers.get("Content-Type");
  console.log("Status:", response.status);
  console.log("Content-Type:", contentType);

  if (!response.ok) throw new Error('Server error');

  const data = await response.json();
  const imageResponse = await fetch(`https://quantum-stego.onrender.com/encoded/${data.image}`);
  const blob = await imageResponse.blob();
  const url = window.URL.createObjectURL(blob);

  const a = document.createElement('a');
  a.href = url;
  a.download = data.image;
  document.body.appendChild(a);
  a.click();
  a.remove();
  window.URL.revokeObjectURL(url);

  status.textContent = `Image encoded and downloaded. Save this key ID for decoding: ${data.key_id}`;
} catch (err) {
  console.error("❌ Error:", err);
  status.textContent = 'Failed to encode image. See console for details.';
}
  });