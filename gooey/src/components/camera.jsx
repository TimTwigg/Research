import { useState, useEffect, useCallback } from "react";
import Webcam from "react-webcam";
import { toast } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";
import "./camera.css";
import square from "./../images/square.png";

function saveBase64AsFile(base64, fileName) {
    var link = document.createElement("a");
    document.body.appendChild(link);
    link.setAttribute("href", base64);
    link.setAttribute("download", fileName);
    link.click();
}

function saveImage(image, filename) {
    saveBase64AsFile(image, filename);
}

const Camera = () => {
    const [devices, SetDevices] = useState([]);
    const [deviceID, SetDeviceID] = useState(0);
    const [image, SetImage] = useState(square);
    const [checked, SetChecked] = useState(false);
    const [gridSize, SetGridSize] = useState(15);
    const [enableCamera, SetEnableCamera] = useState(false);
    const [falsePaths, SetFalsePaths] = useState(true);
    const [lightMode, SetLightMode] = useState(false);
    const [reset, SetReset] = useState(false)

    const videoConstraints = {
        width: 360,
        height: 360,
        deviceId: deviceID
    }

    const handleDevices = useCallback(mediaDevices => {
        SetDevices(mediaDevices.filter(({ kind }) => kind === "videoinput"));
    }, [SetDevices]);

    const TakeImage = async (img) => {
        SetImage(img);
        // generate filename
        let filename = `image_${Date.now()}.png`;
        saveImage(img, filename);
        // send message to flask to trigger program
        const response = await fetch(`http://localhost:5000/data?gridsize=${gridSize}&falsePaths=${falsePaths}&lightMode=${lightMode}&reset=${reset}&filename=${filename}`);
        SetReset(false);
        
        if (response.status === 500) {
            toast("Could not interpret grid from image.", {type: "error", pauseOnFocusLoss: false});
        }
        else {
            toast("Image taken.", {type: "success", pauseOnFocusLoss: false});
        }
    }

    useEffect(() => {
        navigator.mediaDevices.enumerateDevices().then(handleDevices);
        SetReset(true);
    }, [handleDevices, SetReset]);

    return (
        <div className = "Camera">
            <div className = "twelve columns">
                <span className = "twelve columns">
                    <label className = "two columns offset-by-one column" htmlFor = "cameraSelect">Camera</label>
                    <select className = "eight columns" id = "cameraSelect" onChange = {item => SetDeviceID(item.target.value)}>
                        {
                            devices.map((dev, i) => <option key = {i} value = {dev.deviceId}>{dev.label}</option>)
                        }
                    </select>
                </span>
                
                <span className = "twelve columns">
                    <label className = "three columns offset-by-one column" htmlFor = "testCheck">Display Previous State</label>
                    <input type = "checkbox" id = "testCheck" className = "two columns" onChange = {ev => SetChecked(ev.target.checked)}/>
                </span>

                <span className = "twelve columns">
                    <label className = "three columns offset-by-one column" htmlFor = "gridSize">Grid Dimension</label>
                    <input type = "number" id = "gridSize" className = "two columns" defaultValue = {gridSize} onChange = {ev => SetGridSize(parseInt(ev.target.value))}/>
                </span>

                <span className = "twelve columns">
                    <label className = "three columns offset-by-one column" htmlFor = "falsePaths">Generate False Paths</label>
                    <input type = "checkbox" id = "falsePaths" className = "two columns" onChange = {ev => SetFalsePaths(ev.target.checked)} defaultChecked = {falsePaths}/>
                </span>

                <span className = "twelve columns">
                    <label className = "three columns offset-by-one column" htmlFor = "lightMode">Light Mode</label>
                    <input type = "checkbox" id = "lightMode" className = "two columns" onChange = {ev => SetLightMode(ev.target.checked)} defaultChecked = {lightMode}/>
                </span>
            </div>

            <div className = "one-half column">
                <p className = "underline">Camera Feed</p>
                {enableCamera &&
                    <Webcam className = "marginB" videoConstraints = {videoConstraints} audio = {false} screenshotFormat = "image/png">
                        {({ getScreenshot }) => (
                            <div>
                                <button onClick = {() => {TakeImage(getScreenshot())}} className = "five columns offset-by-three columns">Take Image</button>
                            </div>
                        )}
                    </Webcam>
                }
                {!enableCamera &&
                    <div>
                        <img src = {square} alt = "" height = {360}/>
                        <div className = "spacer"/>
                        <button className = "five columns offset-by-three columns" onClick = {() => SetEnableCamera(true)}>Enable Camera</button>
                    </div>
                }
            </div>

            <div className = "one-half column">
                {checked &&
                    <div>
                        <p className = "underline">Previous Image</p>
                        <img src = {image} alt = "" height = {360}/>
                        <div className = "spacer"/>
                        <button className = "five columns offset-by-three columns" onClick = {() => saveImage(image)}>Download</button>
                    </div>
                }
            </div>
        </div>
    );
}

export default Camera;