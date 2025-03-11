import { useParams } from "react-router-dom";
import { FaShareAlt } from "react-icons/fa";
import img2 from "/dummy/image2.avif";
import "./style.scss";
import { useState } from "react";
import Star from "../../component/star";

export default function ShowMovie() {
  const [copied, setCopied] = useState(false);
  const shareUrl = window.location.href; // Get the current page URL

  const { name, id } = useParams(); // Extracting movie name and ID
  const handleCopyLink = () => {
    // Create a temporary input field
    const input = document.createElement("input");
    input.value = shareUrl;
    document.body.appendChild(input);

    // Select and copy the text
    input.select();
    document.execCommand("copy");
    document.body.removeChild(input);

    // Show copied message
    setCopied(true);
    setTimeout(() => setCopied(false), 2000); // Reset after 2 seconds
  };
  return (
    <div className="showMovie-page">
      {/* Movie banner */}
      <div className="showMovies-page-top">
        <div className="showMovies-detail">
          <div className="share-container">
            <button className="movies-share-button" onClick={handleCopyLink}>
              <FaShareAlt />{" "}
              {copied && <div className="share-alert">Copied!</div>}
            </button>
          </div>
          <div className="movie-image">
            <img src={img2} />
          </div>
          <div className="movie-details">
            <h1>{name}</h1>
            <p>
              Lorem ipsum, dolor sit amet consectetur adipisicing elit.
              Inventore voluptatem iste voluptatum ea veritatis ab laudantium,
              tenetur quis cum, repudiandae unde non sed nulla, illo explicabo
              neque eaque minus tempora.
            </p>
            <div className="movie-rating">
              <Star stars={2} />
              <button className="rate-now-button">Rate Now</button>
            </div>
            <button className="book-ticket-button">Book Tickets</button>
          </div>
        </div>
      </div>
    </div>
  );
}
