import GameCard from "@/components/game-card"

export default function Home() {
    return (
        <>
            <h1>Home</h1>
            <hr/>
            <div className = "ten columns offset-by-one column">
                <GameCard name = "Maze" image = {"/mazeIcon.png"} link = "/maze" className = "two columns"/>
            </div>
        </>
    )
}
