import "./game-card.css";

const GameCard = ({ name, image, id, link, className }) => {
    return (
        <div className = {"game-card" + " " + className}>
            <a href = {link}><img src = {image} alt = {name} /></a>
            <h2 className = "game-card-name">{name}</h2>
        </div>
    );
};

export default GameCard;