import { useState, useEffect } from "react";
import { FaRegCaretSquareLeft, FaRegCaretSquareRight } from "react-icons/fa";
import "./style.scss";
import { Link } from "react-router-dom";

function Slider({ slider }) {
  const [currentIndex, setCurrentIndex] = useState(0);
  const [fade, setFade] = useState(false);

  const goToPrevious = () => {
    setFade(true);
    setCurrentIndex((prevIndex) =>
      prevIndex > 0 ? prevIndex - 1 : slider.length - 1
    );
    setFade(false);
  };

  const goToNext = () => {
    setFade(true);
    setCurrentIndex((prevIndex) =>
      prevIndex < slider.length - 1 ? prevIndex + 1 : 0
    );
    setFade(false);
  };

  // Auto slide effect
  useEffect(() => {
    const interval = setInterval(() => {
      goToNext();
    }, 10000); // Change slide every 3 seconds

    return () => clearInterval(interval); // Cleanup on unmount
  }, []);

  return (
    <div className="slider-slide">
      <div className="slider-content-top">
        <FaRegCaretSquareLeft
          className="slider-content-top-left"
          onClick={goToPrevious}
        />
        <FaRegCaretSquareRight
          className="slider-content-top-right"
          onClick={goToNext}
        />
      </div>
      <div
        className={`slider-wrapper ${fade ? "fade" : ""}`}
        style={{ transform: `translateX(-${currentIndex * 100}%)` }}
      >
        {slider.map((slide, index) => (
          <Link to={`http://localhost:3000/${slide.name}/${slide._id}`}
            key={index}
            className="slider-container" >
            <div className="slide-background-image">
              <img src={slide.image}/>
            </div>
            <div className="slider-content">
              <div className="slider-content-bottom">
                <h1>{slide.name}</h1>
                <p>{slide.description}</p>
              </div>
            </div>
          </Link>
        ))}
      </div>
    </div>
  );
}

export default Slider;
