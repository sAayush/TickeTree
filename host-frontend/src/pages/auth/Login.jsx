import { NavLink } from "react-router-dom";

export default function Login(){
    return(
        <div>
            <div className="auth-page-header">Login</div>
            <div className="auth-context">
                <label>Email</label>
                <input type="email" name="email" />
                <label>Password</label>
                <input type="password" name="email"  />
                <p>Don't have an account? <NavLink to="/register">Create</NavLink> one.</p>
            </div>
            <button formAction={SubmitEvent} className="authButton">Login</button>
        </div>
    )
}