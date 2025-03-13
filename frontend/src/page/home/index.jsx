import Slider from "../../component/slider";
import SlidingCard from "../../component/SlidingCard";
import img1 from "/dummy/img1.jpg";
import img2 from "/dummy/img2.jpg";
import img3 from "/dummy/img3.jpg";
import "./style.scss";
const images = [
  { _id: 1, image: img1, name: "Image_2", description: "Description 2" },
  { _id: 2, image: img2, name: "Image_1", description: "Description 1" },
  { _id: 3, image: img3, name: "Image_3", description: "Description 3" },
]
const cards = [
  { _id: 1, image: img3, name: "Image_1", description: "Description 1" },
  { _id: 2, image: img2, name: "Image_2", description: "Description 2" },
  { _id: 3, image: img3, name: "Image_3", description: "Description 3" },
  { _id: 4, image: img2, name: "Image_1", description: "Description 1" },
  { _id: 5, image: img3, name: "Image_2", description: "Description 2" },
  { _id: 6, image: img2, name: "Image_3", description: "Description 3" },
  { _id: 7, image: img3, name: "Image_2", description: "Description 2" },
  { _id: 8, image: img2, name: "Image_3", description: "Description 3" },
  { _id: 9, image: img3, name: "Image_2", description: "Description 2" },
  { _id: 10, image: img2, name: "Image_3", description: "Description 3" },
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
