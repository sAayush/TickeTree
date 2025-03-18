import { BrowserRouter as Router, Routes, Route } from "react-router-dom"
import Layout from "./layout"
import DashBoard from "./pages/Dashboard"
import AuthModel from "./pages/auth/AuthModel"
import Login from "./pages/auth/Login"
import Register from "./pages/auth/Register"
function App() {

  return (
    <Router>
      <Routes>
        <Route path="/" element={<Layout children={<DashBoard/>} />}/>
        <Route path="/login" element={<AuthModel children={<Login/>} />}/>
        <Route path="/register" element={<AuthModel children={<Register/>} />}/>
      </Routes>
    </Router>
  )
}

export default App
