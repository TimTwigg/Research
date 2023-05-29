import { ToastContainer } from "react-toastify";
import Layout from "../components/layout";
import Camera from "../components/camera";

const Maze = () => {
    return (
        <Layout title = "maze">
            <h1>Maze</h1>
            <hr/>
            <Camera/>
            <ToastContainer/>
        </Layout>
    )
}

export default Maze;