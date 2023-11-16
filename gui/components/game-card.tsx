import "@/styles/game-card.css"

type GameCardProps = {
    name: string,
    image: string,
    link: string,
    className?: string
}

export default function GameCard({ name, image, link, className } : GameCardProps) {
    return (
        <div className = {"game-card " + className}>
            <a href = {link}>
                <img src = {image} alt = {name}/>
                <h2 className = "game-card-name">{name}</h2>
            </a>
        </div>
    )
}