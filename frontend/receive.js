document.getElementById('receiveForm').addEventListener('submit', async (e) => {
    e.preventDefault();

    const imageInput = document.getElementById('stegoImageInput');
    const keyIdInput = document.getElementById('keyIdInput');
    const output = document.getElementById('outputMessage');
    const status = document.getElementById('statusText');

    if (!imageInput.files.length || !keyIdInput.value.trim()) {
      status.textContent = 'Please upload an image and enter the key ID.';
      return;
    }

    const formData = new FormData();
    formData.append('image', imageInput.files[0]);
    formData.append('key_id', keyIdInput.value.trim());

    try {
      const res = await fetch('https://quantum-stego.onrender.com/decode', {
        method: 'POST',
        body: formData
      });

      if (!res.ok) {
        const err = await res.text();
        throw new Error(`Server error: ${err}`);
      }

      const text = await res.text();
      output.value = text;
      status.textContent = 'Message decoded successfully!';
    } catch (err) {
      console.error(err);
      output.value = '';
      status.textContent = 'Failed to decode. See console.';
    }
  });