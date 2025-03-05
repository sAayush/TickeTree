import { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import { FaChevronLeft, FaChevronRight } from "react-icons/fa"; // Navigation icons
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
    <div className="slidingCard-container">
      <button className="slidingCard-button left" onClick={goToPrevious}>
        <FaChevronLeft />
      </button>
      <div
        className="slidingCard-wrapper"
        style={{
          transform: `translateX(-${currentIndex * (100 / cardsToShow)}%)`,
        }}
      >
        {card.map((item, index) => (
          <Link to={item.url} key={index} className="slidingCard-item">
            <div className="slidingCard-image">
              <img src={item.image} alt={item.title} />
            </div>
            <div className="slidingCard-content">
              <div className="slidingCard-title">{item.title}</div>
              <div className="slidingCard-description">{item.description}</div>
            </div>
          </Link>
        ))}
      </div>
      <button className="slidingCard-button right" onClick={goToNext}>
        <FaChevronRight />
      </button>
    </div>
  );
}
