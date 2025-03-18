import Navbar from "../components/nav";

export default function Layout({children}){
    return(
        <>
            <Navbar/>
            <div style={{margin:"30px"}}>
                {children}
            </div>
        </>
    )
}