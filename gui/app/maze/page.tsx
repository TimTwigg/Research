"use client"
import { useState, useEffect, useCallback, useRef } from "react"
import Webcam from "react-webcam"
import { ToastContainer, toast } from "react-toastify"
import "react-toastify/dist/ReactToastify.css"
import "@/styles/maze.css"

function saveBase64AsFile(base64: string, fileName: string) {
    var link = document.createElement("a");
    document.body.appendChild(link);
    link.setAttribute("href", base64);
    link.setAttribute("download", fileName);
    link.click();
}

function saveImage(image: string, filename: string) {
    saveBase64AsFile(image, filename);
}

export default function Maze() {
    const [devices, SetDevices] = useState(Array<MediaDeviceInfo>);
    const [deviceID, SetDeviceID] = useState("");
    const [image, SetImage] = useState("/square.png");
    const [prevState, SetPrevState] = useState(true);
    const [gridSize, SetGridSize] = useState(15);
    const [enableCamera, SetEnableCamera] = useState(false);
    const [falsePaths, SetFalsePaths] = useState(true);
    const [lightMode, SetLightMode] = useState(false);
    const [reset, SetReset] = useState(false);

    const webcamRef = useRef<Webcam>(null);
    const capture = useCallback(() => {
        if (webcamRef != null) {
            TakeImage(webcamRef.current!.getScreenshot()!);
        }
    },[webcamRef]);

    const videoConstraints = {
        width: 360,
        height: 360,
        deviceId: deviceID
    }

    const handleDevices = useCallback((mediaDevices: MediaDeviceInfo[]) => {
        SetDevices(mediaDevices.filter(({ kind }) => kind === "videoinput"));
    }, [SetDevices]);

    const TakeImage = async (img: string) => {
        SetImage(img);
        // generate filename
        let filename = `img_${Date.now()}.png`;
        saveImage(img, filename);
        // send message to flask to trigger program
        var response;
        try {
            response = await fetch(`http://localhost:5000/data?gridsize=${gridSize}&falsePaths=${falsePaths}&lightMode=${lightMode}&reset=${reset}&filename=${filename}`);
        } catch (e) {
            response = {status: 502}
        }
        SetReset(false);
        document.getElementById("imageCategory")!.innerText = "Grid";
        
        if (response === undefined || response.status === 502) {
            toast("Server not running.", {type: "error", pauseOnFocusLoss: false, pauseOnHover: false});
        }
        else if (response.status === 500) {
            toast("Could not interpret grid from image.", {type: "error", pauseOnFocusLoss: false, pauseOnHover: false});
        }
        else {
            toast("Image taken.", {type: "success", pauseOnFocusLoss: false, pauseOnHover: false});
        }
    }

    const resetState = () => {
        SetReset(true);
        document.getElementById("imageCategory")!.innerText = "Blank";
    }

    useEffect(() => {
        navigator.mediaDevices.enumerateDevices().then(handleDevices);
        SetReset(true);
    }, [handleDevices, SetReset]);


    return (<>
        <ToastContainer/>
        <h1>Maze</h1>
        <hr/>
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
                    <input type = "checkbox" id = "testCheck" className = "two columns" defaultChecked = {prevState} onChange = {ev => SetPrevState(ev.target.checked)}/>
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

            <div className = "twelve columns">
                <p className = "one-half column"><u>Taking:</u> <span id = "imageCategory">Blank</span></p>
                <button className = "four columns offset-by-two columns" onClick = {() => resetState()}>Reset</button>
            </div>

            <div className = "one-half column">
                <p className = "underline">Camera Feed</p>
                {enableCamera &&
                    <>
                        <Webcam className = "marginB" videoConstraints = {videoConstraints} audio = {false} screenshotFormat = "image/png" ref = {webcamRef}/>
                        <button onClick = {capture} className = "five columns offset-by-three columns">Take Image</button>
                        <button onClick = {() => SetEnableCamera(false)} className = "five columns offset-by-three columns">Disable Camera</button>
                    </>
                }
                {!enableCamera &&
                    <div>
                        <img src = {"/square.png"} alt = "" height = {360}/>
                        <div className = "spacer"/>
                        <button className = "five columns offset-by-three columns" onClick = {() => SetEnableCamera(true)}>Enable Camera</button>
                    </div>
                }
            </div>

            <div className = "one-half column">
                {prevState &&
                    <div>
                        <p className = "underline">Previous Image</p>
                        <img src = {image} alt = "" height = {360}/>
                        <div className = "spacer"/>
                        <button className = "five columns offset-by-three columns" onClick = {() => saveImage(image, `img_${Date.now()}.png`)}>Download</button>
                    </div>
                }
            </div>
        </div>
    </>)
}