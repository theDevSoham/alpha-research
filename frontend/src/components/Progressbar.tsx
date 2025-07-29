import { useEffect, useState } from "react";

interface Props {
  jobId: string;
  onComplete: () => void;
}

export default function ProgressBar({ jobId, onComplete }: Props) {
  const [progress, setProgress] = useState(0);

  useEffect(() => {
    // const wsProtocol = window.location.protocol === "https:" ? "wss" : "ws";
    // const wsUrl = `ws://localhost:8000/ws/progress/${jobId}`;
    const wsUrl = `ws://localhost:8000/ws/progress/${jobId}`;
    const socket = new WebSocket(wsUrl);

    socket.onopen = (ev) => {
      console.log("Socket connection successful: ", ev.type);
    };

    socket.onmessage = (event) => {
      const data = JSON.parse(event.data);
      if (data.progress !== undefined) {
        setProgress(data.progress > 0 ? data.progress : 0);

        if (data.progress === -1) {
          socket.close();
          alert("Task failed!");
        }

        if (data.progress === 100) onComplete();
      }
    };

    socket.onerror = (err) => {
      console.error("WebSocket error:", err);
    };

    socket.onclose = () => {
      console.log("WebSocket closed for job", jobId);
    };

    return () => {
      if (socket && socket.readyState !== socket.CLOSED) {
        socket.close();
      }
    };
  }, [jobId]);

  return (
    <div className="w-full bg-gray-200 rounded-full h-4 mt-4">
      <div
        className="bg-blue-600 h-4 rounded-full transition-all duration-500"
        style={{ width: `${progress}%` }}
      />
      <p className="text-sm text-gray-600 mt-1">{progress}%</p>
    </div>
  );
}
