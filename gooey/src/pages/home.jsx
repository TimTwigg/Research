import React from "react";
import GameCard from "../components/game-card";
import Layout from "../components/layout";
import './home.css'

const Home = () => {
    return (
        <Layout title = "home">
            <h1>Home</h1>
            <hr/>
            <div>
                <GameCard name="maze" image = "./../assets/mazeIcon.png" link = "/maze"></GameCard>
            </div>
        </Layout>
    )
}

export default Home;