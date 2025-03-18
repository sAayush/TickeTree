import { NavLink } from "react-router-dom"
import "./style.scss"

export default function DashBoard(){
    const content =[
        {Name: "Add Movies", icon: <svg width="54" height="53" viewBox="0 0 54 53" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M53.1657 33.125H33.2286V53H19.9371V33.125H0V19.875H19.9371V0H33.2286V19.875H53.1657V33.125Z" fill="#017246"/>
            </svg>,
            url: "#"
            },
        {Name: "Add Events", icon: <svg width="54" height="53" viewBox="0 0 54 53" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M53.1657 33.125H33.2286V53H19.9371V33.125H0V19.875H19.9371V0H33.2286V19.875H53.1657V33.125Z" fill="#017246"/>
            </svg>,
            url: "#"
            },
        {Name: "Show Movies", icon: <svg width="49" height="44" viewBox="0 0 49 44" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M44.6923 2H4.30769C3.03319 2 2 3.27921 2 4.85719V34.8577C2 36.4357 3.03319 37.7149 4.30769 37.7149H44.6923C45.9668 37.7149 47 36.4357 47 34.8577V4.85719C47 3.27921 45.9668 2 44.6923 2Z" stroke="#017246" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>
            <path d="M13.5361 42H35.4592M31.4207 19.8567L19.8823 11.6094V28.104L31.4207 19.8567Z" stroke="#017246" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>,
            url: "#"
            },
        {Name: "Show Events", icon: <svg width="49" height="44" viewBox="0 0 49 44" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M44.6923 2H4.30769C3.03319 2 2 3.27921 2 4.85719V34.8577C2 36.4357 3.03319 37.7149 4.30769 37.7149H44.6923C45.9668 37.7149 47 36.4357 47 34.8577V4.85719C47 3.27921 45.9668 2 44.6923 2Z" stroke="#017246" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>
            <path d="M13.5361 42H35.4592M31.4207 19.8567L19.8823 11.6094V28.104L31.4207 19.8567Z" stroke="#017246" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>
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