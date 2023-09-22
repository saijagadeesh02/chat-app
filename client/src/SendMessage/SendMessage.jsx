import { useEffect, useState } from "react";



function SendMessage ({socket}) {
    
    const [message, setMessage] = useState("");
    const [messageStack, setMessageStack] = useState([]);

    function handleMessage(e){
        setMessage(e.target.value);
    }


    function emitMessage(){
        // Prepare the final packet with sid and message
        var finalPacket = { "sid" : socket.id, "message" : message}
        // Send the message to the server
        socket.emit("my_event", finalPacket)
        // Clear the input box
        setMessage("")
        // Append the latest message to the list of messages
        setMessageStack(prevArray => {
            return [...prevArray, finalPacket["message"]]
        });
    }


 
    return  (<div>
                <div>
                    {messageStack.map((val, idx) => <li key={idx}>{val}</li>)}
                </div>
                <div>
                    <input id="msg" value={message} onChange={handleMessage}></input>
                    <button id="submit" type="submit" onClick={emitMessage}>Send</button>
                </div>
            </div>)
}

export default SendMessage;