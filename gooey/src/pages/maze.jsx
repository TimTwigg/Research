import React from "react";
import Layout from "../components/layout";
import Camera from "../components/camera";

const Maze = () => {
    return (
        <Layout title = "maze">
            <h1>Maze</h1>
            <hr/>
            <p>
                Make a maze.
            </p>
            <Camera/>
        </Layout>
    )
}

export default Maze;