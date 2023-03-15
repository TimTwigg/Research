

const GameCard = ({ game }) => {
    const { name, image, id } = game;
    return (
        <div className="game-card" onClick={() => onGameClick(id)}>
        <img src={image} alt={name} />
        <div className="game-card__name">{name}</div>
        </div>
    );
    }