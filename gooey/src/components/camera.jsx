import { useState, useEffect, useCallback } from "react";
import Webcam from "react-webcam";
import "./camera.css";
import square from "./../images/square.png";

function saveBase64AsFile(base64, fileName) {
    var link = document.createElement("a");

    document.body.appendChild(link); // for Firefox

    link.setAttribute("href", base64);
    link.setAttribute("download", fileName);
    link.click();
}

function saveImage(image) {
    saveBase64AsFile(image, "test.png");
}

const Camera = () => {
    const [devices, SetDevices] = useState([]);
    const [deviceID, SetDeviceID] = useState("");
    const [image, SetImage] = useState(square);
    const [checked, SetChecked] = useState(false);

    const videoConstraints = {
        width: 640,
        height: 360,
        deviceId: deviceID
    }

    const handleDevices = useCallback(mediaDevices => {
        SetDevices(mediaDevices.filter(({ kind }) => kind === "videoinput"));
    }, [SetDevices]);

    const DisplayImage = (img) => {
        SetImage(img);
        if (!checked) {
            saveImage(img);
        }
    }

    useEffect(() => {
        navigator.mediaDevices.enumerateDevices().then(handleDevices);
    }, [handleDevices]);

    return (
        <div className = "Camera">
            <div className = "twelve columns">
                <label className = "two columns offset-by-one column" htmlFor = "cameraSelect">Camera</label>
                <select className = "eight columns" id = "cameraSelect" onChange = {item => SetDeviceID(item.target.value)}>
                    {
                        devices.map((dev, i) => <option key = {i} value = {dev.deviceId}>{dev.label}</option>)
                    }
                </select>
                
                <label className = "three columns offset-by-one column" htmlFor = "testCheck">Test Image Before Saving</label>
                <input type = "checkbox" id = "testCheck" className = "two columns" onChange = {(ev) => SetChecked(ev.target.checked)}/>
            </div>

            <div className = "one-half column">
                <Webcam className = "marginB" videoConstraints = {videoConstraints} audio = {false} screenshotFormat = "image/png">
                    {({ getScreenshot }) => (
                        <div>
                            <button onClick = {() => {DisplayImage(getScreenshot())}} className = "five columns offset-by-three columns">Take Image</button>
                        </div>
                    )}
                </Webcam>
            </div>

            <div className = "one-half column">
                {checked &&
                    <div>
                        <img src = {image} alt = "" height = {360}/>
                        <div className = "spacer"/>
                        <button className = "five columns offset-by-three columns" onClick = {() => saveImage(image)}>Save</button>
                    </div>
                }
            </div>
        </div>
    );
}

export default Camera;