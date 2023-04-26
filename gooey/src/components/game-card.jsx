const GameCard = ({ name, image, id }) => {
    return (
        <div class="game-card">
            <img src={image} alt={name} />
            <h2 class="game-card-name">{name}</h2>
        </div>        
    );
};

export default GameCard;