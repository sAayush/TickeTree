import Navbar from "../components/nav";

export default function Layout({children}){
    return(
        <>
            <Navbar/>
            <div style={{marginTop:"20px"}}>
                {children}
            </div>
        </>
    )
}