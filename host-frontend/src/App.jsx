import { BrowserRouter as Router, Routes, Route } from "react-router-dom"
import Layout from "./layout"
import DashBoard from "./pages/Dashboard"
function App() {

  return (
    <Router>
      <Routes>
        <Route path="/" element={<Layout children={<DashBoard/>} />}>
        </Route>
      </Routes>
    </Router>
  )
}

export default App
