const GameCard = ({ name, image, id }) => {
    return (
        <div className = "game-card">
            <img src={image} alt={name} />
            <h2 className = "game-card-name">{name}</h2>
        </div>
    );
};

export default GameCard;