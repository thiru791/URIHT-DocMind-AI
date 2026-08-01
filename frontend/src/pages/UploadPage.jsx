import { useNavigate } from "react-router-dom";
import Logo from "../components/Logo";
import { useState, useRef } from "react";
import api from "../services/api";

function UploadPage() {
  const [file, setFile] = useState(null);
  const [message, setMessage] = useState("");
  const [loading, setLoading] = useState(false);
  const [drag, setDrag] = useState(false);

  const fileInputRef = useRef(null);
  const navigate = useNavigate();

  const handleFile = (selectedFile) => {
    if (selectedFile && selectedFile.type === "application/pdf") {
      setFile(selectedFile);
      setMessage("");
    } else {
      setMessage("❌ Please select a PDF file");
    }
  };

  const uploadFile = async () => {
    if (!file) {
      setMessage("Please select a PDF.");
      return;
    }

    setLoading(true);

    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await api.post("/upload", formData);

      setMessage(
  `✅ Upload Successful (Document ID: ${response.data.id})`
);

// Wait 1 second so user can see success
setTimeout(() => {
  navigate("/chat");
}, 1000);
    } catch (error) {
      console.log(error);
      setMessage("❌ Upload Failed");
    }

    setLoading(false);
  };

  return (
    <div className="upload-page">
      <div className="upload-card">
        <Logo />

        <p>
          Upload your document and let URIHT DocMind AI analyze it.
        </p>

        <div
          className={`drop-zone ${drag ? "drag-active" : ""}`}
          onClick={() => fileInputRef.current.click()}
          onDragOver={(e) => {
            e.preventDefault();
            setDrag(true);
          }}
          onDragLeave={() => {
            setDrag(false);
          }}
          onDrop={(e) => {
            e.preventDefault();
            setDrag(false);
            handleFile(e.dataTransfer.files[0]);
          }}
        >
          {file ? (
            <div className="file-preview">
              <div className="pdf-icon">📕</div>

              <h3>{file.name}</h3>

              <p>{(file.size / 1024).toFixed(2)} KB</p>
            </div>
          ) : (
            <>
              <div className="upload-icon">☁️</div>

              <h3>Drag & Drop PDF Here</h3>

              <p>Click to browse PDF</p>
            </>
          )}

          <input
            ref={fileInputRef}
            type="file"
            accept=".pdf"
            hidden
            onChange={(e) => handleFile(e.target.files[0])}
          />
        </div>

        <button onClick={uploadFile}>
          {loading ? "Uploading..." : "Upload PDF"}
        </button>

        <h3>{message}</h3>
      </div>
    </div>
  );
}

export default UploadPage;