import "./style.scss";  
import { Link } from "react-router-dom";
export default function Card({card}) {
    return (
        <div className="card-container">
            {card.map((card,index) => (
                <Link to={card.url} key={card.index}>

                    <div className="card-item" key={card.index}>
                        <div className="card-image" key={card.index}>
                            <img src={card.image} alt={card.title} />
                        </div>
                        <div className="card-content"></div>
                        <div className="card-title">{card.title}</div>
                        <div className="card-description">{card.description}</div>
                    </div>
                </Link>
            ))}
        </div>
    )
}