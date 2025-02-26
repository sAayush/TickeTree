import Home from "./page/home";
import Movies from "./page/movies";
import Sports from "./page/sports";
import Events from "./page/events";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
function App() {
  return (
    <>
      <Router>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/movies" element={<Movies />} />
          <Route path="/sports" element={<Sports />} />
          <Route path="/events" element={<Events />} />
        </Routes>
      </Router>
    </>
  );
}

export default App;
