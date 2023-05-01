import "./game-card.css";

const GameCard = ({ name, image, id, link }) => {
    return (
        <div className = "game-card">
            <a href = {link}><img src={image} alt={name} /></a>
            <h2 className = "game-card-name">{name}</h2>
        </div>
    );
};

export default GameCard;