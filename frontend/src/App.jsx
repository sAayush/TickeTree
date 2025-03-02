import Home from "./page/home";
import Movies from "./page/movies";
import Sports from "./page/sports";
import Events from "./page/events";
import Layout from "./layout/defaultLaout";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
function App() {
  return (
    <>
      <Router>
        <Routes>
          {/* Apply Layout to multiple pages */}
          <Route path="/" element={<Layout />}>
            <Route index element={<Home />} />
            <Route path="/movies" element={<Movies />} />
            <Route path="/sports" element={<Sports />} />
            <Route path="/events" element={<Events />} />
          </Route>
        </Routes>
      </Router>
    </>
  );
}

export default App;
