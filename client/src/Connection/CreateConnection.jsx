import { io } from "socket.io-client";
import { useEffect, useState } from "react";

import SendMessage from "../SendMessage/SendMessage";
import config from "../Config";

const SERVER = "http://localhost";
const PORT = "5000";

function createNewConnection() {
    const newSocket = io(`${SERVER}:${PORT}`);
    return newSocket
}

function SendConnection() {

    const [socket, setSocket] = useState();
    const roomId = "12345";

    useEffect(() => {
        let curSocket = createNewConnection();

        curSocket.on(config.messageEvent, (data) => {
            console.log(`Message from server: ${data}`)
        })

        setSocket(curSocket);

        // Clean up the socket connection when the component unmounts
        return () => {
            curSocket.disconnect(); // Disconnect the socket when unmounting
        };

    }, []);

    console.log("some message")

    return <div>
        <SendMessage socket={socket} roomId={roomId}></SendMessage>
    </div>

}

export default SendConnection;