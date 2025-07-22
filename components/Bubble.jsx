
export default function Bubble({message}){
    const {content, role, fileName} = message;

    return (
      <div className={`${role} bubble`}>
        {role === "user" && fileName && (
          <p style={{ fontWeight: "bold", marginBottom: "4px", color: "#aaa" }}>
            📄 {fileName}
          </p>
        )}
        <p>{content}</p>
      </div>
    );
}