import { useState } from "react";
import { Link } from "react-router-dom";
import { MdKeyboardArrowLeft, MdKeyboardArrowRight } from "react-icons/md";
import "./style.scss";

export default function SlidingCard({ card }) {
  const [currentIndex, setCurrentIndex] = useState(0);
  const cardsToShow = 5; // ✅ Ensure exactly 5 cards visible
  const totalCards = card.length;

  const goToNext = () => {
    setCurrentIndex((prev) => (prev + 1) % (totalCards - (cardsToShow - 1)));
  };

  const goToPrevious = () => {
    setCurrentIndex((prev) =>
      prev - 1 < 0 ? totalCards - cardsToShow : prev - 1
    );
  };


  return (
    <div className="slidingCard-page">
        <button className="slidingCard-button left" onClick={goToPrevious}>
          <MdKeyboardArrowLeft />
        </button>
      <div className="slidingCard-container">
        <div
          className="slidingCard-wrapper"
          style={{
            transform: `translateX(-${currentIndex * (100 / cardsToShow)}%)`,
          }}
        >
          {card.map((item, index) => (
            <Link to={`http://localhost:3000/${item.name}/${item._id}`} key={index} className="slidingCard-item">
              <div className="slidingCard-image">
                <img src={item.image} alt={item.title} />
              </div>
              <div className="slidingCard-content">
                <div className="slidingCard-title">{item.name}</div>
                <div className="slidingCard-description">{item.description}</div>
              </div>
            </Link>
          ))}
        </div>
      </div>
        <button className="slidingCard-button right" onClick={goToNext}>
          <MdKeyboardArrowRight />
        </button>
    </div>
  );
}
