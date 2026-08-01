import { Routes, Route } from "react-router-dom";

import HomePage from "./pages/HomePage";
import UploadPage from "./pages/UploadPage";
import ChatPage from "./pages/ChatPage";

function App() {
  return (
    <Routes>
      <Route path="/" element={<HomePage />} />
      <Route path="/upload" element={<UploadPage />} />
      <Route path="/chat" element={<ChatPage />} />
    </Routes>
  );
}

export default App;