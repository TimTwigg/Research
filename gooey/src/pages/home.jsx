import React from "react";
import GameCard from "../components/game-card";
import './home.css'

const Home = () => {
    return (
        <div className="home">
            <h1>Home</h1>
            <div>
                <GameCard name="test"></GameCard>
            </div>
        </div>
    )
}

export default Home;