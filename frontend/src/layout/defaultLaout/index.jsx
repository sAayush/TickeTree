import { Outlet } from "react-router-dom";
import Navbar from "../../component/nav";

const Layout = () => {
  return (
    <div>
      <Navbar />
      <main className="container">
        <Outlet /> 
      </main>
    </div>
  );
};

export default Layout;
