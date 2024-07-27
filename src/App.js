// App.js
import React, { useState } from 'react';
import axios from 'axios';

function App() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [imageUrls, setImageUrls] = useState([]);

  const handleFileChange = (e) => {
    setSelectedFile(e.target.files[0]);
  };

  const handleUpload = async () => {
    if (!selectedFile) return;

    const formData = new FormData();
    formData.append('image', selectedFile);

    try {
      const response = await axios.post('http://localhost:5000/detect-license-plates', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      });
      setImageUrls(response.data.files);
    } catch (error) {
      console.error('Error uploading file:', error);
    }
  };

  return (
    <div>
      <h1>License Plate Detector</h1>
      <input type="file" onChange={handleFileChange} />
      <button onClick={handleUpload}>Upload</button>
      <div>
        {imageUrls.map((url, index) => (
          <img key={index} src={`http://localhost:5000${url}`} alt={`License Plate ${index + 1}`} />
        ))}
      </div>
    </div>
  );
}

export default App;
