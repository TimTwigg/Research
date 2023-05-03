import React from "react";
import GameCard from "../components/game-card";
import Layout from "../components/layout";
import "./home.css";
import maze from "./../images/mazeIcon.png";

const Home = () => {
    return (
        <Layout title = "home">
            <h1>Home</h1>
            <hr/>
            <div className = "ten columns offset-by-one column">
                <GameCard name = "Maze" image = {maze} link = "/maze" className = "two columns"/>
            </div>
        </Layout>
    )
}

export default Home;