import { useState } from "react";
import LoadingBubble from "../components/LoadingBubble";
import Bubble from "../components/Bubble";
import UploadFileIcon from '@mui/icons-material/UploadFile';

export default function App() {
  const [messages, setMessages] = useState([]);
  const [role, setRole] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [fileName, setFileName] = useState("");
  const [file, setFile] = useState(null); 
  
  const isFormValid = file && role.trim().length > 0;

  const noMsg = messages.length === 0;

  const handleSubmit = async (e) => {
    e.preventDefault();
    if(!isFormValid) return;
    setIsLoading(true);
   try{
      const userMessage = {
        role: "user",
        content: role,
        fileName: fileName, 
      };

    const updatedMessages = [...messages, userMessage];
    setMessages(updatedMessages);

    const formData = new FormData();
    formData.append("job_role", role);
    if (file) formData.append("resume", file);

    const res = await fetch("http://localhost:5000/api/chat", {
      method: "POST",
      body: formData,
    });
    if (!res.ok) {
    throw new Error(`Server error: ${res.status}`);
    }
    const responseText = await res.json();

    setMessages((prev) => [
      ...prev,
      {
        role: "assistant",
        content: responseText.questions || "Questions could not be generated. Try again.",
      },
    ]);
   }catch(err){
    console.error(err);
   }finally{
      setFile(null);
      setFileName("");
      setIsLoading(false);
      setRole("");
   }

  };

  const handleFileUpload = (e) => {
  const uploadedFile = e.target.files[0];
  if (uploadedFile) {
    setFileName(uploadedFile.name);
    setFile(uploadedFile);  
    e.target.value = null;
  }
  };


  return (
    <main>
      <section className={noMsg ? "" : "msgExists"}>
        {noMsg ? (
          <>
            <p className="welcomeText">
              Welcome to PrepPilot – where your resume meets reality.
              Discover what interviewers will ask before the interview. 
              Upload your resume, enter the job title, 
              and let our AI generate role-specific questions just for you.
            </p>
          </>
        ) : (
          <div className="chat-container  custom-scrollbar">
            {messages.map((message, index) => (
              <Bubble key={index} message={message} />
            ))}
            {isLoading && <LoadingBubble />}
          </div>
        )}
      </section>

  <div style={{ width: "100%", padding: "0 20px" }}>
    {fileName && (
      <p style={{ marginBottom: "8px", color: "#ccc", fontWeight: "bold", textAlign: "left" }}>
        📄 {fileName}
      </p>
    )}

    <form onSubmit={handleSubmit} className="inputForm">
      <input
        onChange={(e) => setRole(e.target.value)}
        value={role}
        className="queryBox"
        placeholder="Enter job role  (eg: Data Engineer)"
      />
      <label className="fileUploadLabel">
        <UploadFileIcon className="fileUpload" />
        <input type="file" hidden onChange={handleFileUpload} />
      </label>
      <input type="submit" />
    </form>
  </div>
    </main>
  );
}
