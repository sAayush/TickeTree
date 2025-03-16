import { NavLink } from "react-router-dom"
import "./style.scss"

export default function DashBoard(){
    const content =[
        {Name: "Add Movies", icon: <svg width="54" height="53" viewBox="0 0 54 53" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M53.1657 33.125H33.2286V53H19.9371V33.125H0V19.875H19.9371V0H33.2286V19.875H53.1657V33.125Z" fill="#017246"/>
            </svg>,
            url: "#"
            },
        {Name: "Add Movies", icon: <svg width="54" height="53" viewBox="0 0 54 53" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M53.1657 33.125H33.2286V53H19.9371V33.125H0V19.875H19.9371V0H33.2286V19.875H53.1657V33.125Z" fill="#017246"/>
            </svg>,
            url: "#"
            },
        {Name: "Add Movies", icon: <svg width="54" height="53" viewBox="0 0 54 53" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M53.1657 33.125H33.2286V53H19.9371V33.125H0V19.875H19.9371V0H33.2286V19.875H53.1657V33.125Z" fill="#017246"/>
            </svg>,
            url: "#"
            },
        {Name: "Add Movies", icon: <svg width="54" height="53" viewBox="0 0 54 53" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M53.1657 33.125H33.2286V53H19.9371V33.125H0V19.875H19.9371V0H33.2286V19.875H53.1657V33.125Z" fill="#017246"/>
            </svg>,
            url: "#"
            }
    ]
    return(
        <div className="dashboard-page">
            {content.map((item, index) => (
                <NavLink className="dashboard-page-cards" key={index} to={item.url}>
                    {item.icon}
                    {item.Name}
                </NavLink>
            ))}
        </div>
    )
}