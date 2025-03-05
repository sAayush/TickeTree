import Slider from "../../component/slider";
import SlidingCard from "../../component/SlidingCard";
import img1 from "/dummy/image-1.jpg";
import img2 from "/dummy/image2.avif";
import img3 from "/dummy/image3.avif";
import "./style.scss";
const images = [
  { image: img1, title: "Image 1", description: "Description 1" },
  { image: img1, title: "Image 2", description: "Description 2" },
  { image: img1, title: "Image 3", description: "Description 3" },
];
const cards = [
  { image: img3, title: "Image 1", description: "Description 1", url: "https://www.google.com" },
  { image: img2, title: "Image 2", description: "Description 2", url: "https://www.google.com" },
  { image: img3, title: "Image 3", description: "Description 3", url: "https://www.google.com" },
  { image: img2, title: "Image 1", description: "Description 1", url: "https://www.google.com" },
  { image: img3, title: "Image 2", description: "Description 2", url: "https://www.google.com" },
  { image: img2, title: "Image 3", description: "Description 3", url: "https://www.google.com" },
  { image: img3, title: "Image 2", description: "Description 2", url: "https://www.google.com" },
  { image: img2, title: "Image 3", description: "Description 3", url: "https://www.google.com" },
  { image: img3, title: "Image 2", description: "Description 2", url: "https://www.google.com" },
  { image: img2, title: "Image 3", description: "Description 3", url: "https://www.google.com" },
];
function Home() {
  return (
    <div className="home-page">
      <div className="home-page-slider">
        <Slider slider={images} />
      </div>
      <div className="home-page-recommend-movies">
        <div className="home-page-recommend-movies-title">Recommend Movies</div>
        <div className="home-page-recommend-movies-cards">
            <SlidingCard card={cards}/>
        </div>
      </div>
    </div>
  );
}
export default Home;
