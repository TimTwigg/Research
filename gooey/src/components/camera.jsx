import { useState, useEffect, useCallback } from "react";
import Webcam from "react-webcam";

const Camera = () => {
    const [devices, SetDevices] = useState([]);
    const [deviceID, SetDeviceID] = useState("");

    const videoConstraints = {
        width: 1280,
        height: 720,
        deviceId: deviceID
    }

    const handleDevices = useCallback(mediaDevices => {
        SetDevices(mediaDevices.filter(({ kind }) => kind === "videoinput"));
    }, [SetDevices]);

    useEffect(() => {
        navigator.mediaDevices.enumerateDevices().then(handleDevices);
    }, [handleDevices]);

    return (
        <div className = "container Camera">
            <Webcam className = "six columns marginB" videoConstraints = {videoConstraints}/>
            <select className = "six columns" onChange = {item => SetDeviceID(item.target.value)}>
                {
                    devices.map((dev, i) => <option key = {i} value = {dev.deviceId}>{dev.label}</option>)
                }
            </select>
        </div>
    );
}

export default Camera;