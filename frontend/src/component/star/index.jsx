import { FaStar, FaStarHalfAlt } from "react-icons/fa";
import { AiOutlineStar } from "react-icons/ai";
import "./stylr.scss"

export default function Star({stars}){
    const rateStar = Array.from({length:5}, (elem, index)=>{
        let number = index+0.5;
        return(
            stars>=index+1? (
                <FaStar className="star-icon"/>
            ): stars>=number?(
                <FaStarHalfAlt className="star-icon"/>
            ):(
                <AiOutlineStar className="star-icon"/>
            )
        )
    })
    return(
        <div>{rateStar}</div>
    )
}