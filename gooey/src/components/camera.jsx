import { useState, useEffect, useCallback } from "react";
import Webcam from "react-webcam";
import "./camera.css";
import square from "./../images/square.png";

function saveBase64AsFile(base64, fileName) {
    var link = document.createElement("a");
    document.body.appendChild(link);
    link.setAttribute("href", base64);
    link.setAttribute("download", fileName);
    link.click();
}

function saveImage(image) {
    saveBase64AsFile(image, "capture.png");
}

const Camera = () => {
    const [devices, SetDevices] = useState([]);
    const [deviceID, SetDeviceID] = useState("");
    const [image, SetImage] = useState(square);
    const [checked, SetChecked] = useState(false);
    const [gridSize, SetGridSize] = useState(15);
    const [enableCamera, SetEnableCamera] = useState(false);
    const [falsePaths, SetFalsePaths] = useState(true);

    const videoConstraints = {
        width: 360,
        height: 360,
        deviceId: deviceID
    }

    const handleDevices = useCallback(mediaDevices => {
        SetDevices(mediaDevices.filter(({ kind }) => kind === "videoinput"));
    }, [SetDevices]);

    const TakeImage = async (img) => {
        SetEnableCamera(false);
        SetImage(img);
        const arg_gridsize = gridSize;
        const arg_deviceID = deviceID;
        // fetch("http:localhost:5000/data/" + JSON.stringify(data)).then(res => res.json().then(data => {console.log(data)}))
        const response = await fetch(`http://localhost:5000/data/gridsize=${arg_gridsize}&deviceID=${arg_deviceID}`);
        SetEnableCamera(true);
    }

    useEffect(() => {
        navigator.mediaDevices.enumerateDevices().then(handleDevices);
    }, [handleDevices]);

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