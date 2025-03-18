import { NavLink } from "react-router-dom";
export default function Register(){
    return(
        <div>
            <div className="auth-page-header">Register</div>
            <div className="register-auth-context">
                <label>User Name</label>
                <input type="text" name="userName" />
                <label>Organization Name</label>
                <input type="text" name="organizationName" />
                <label>Address</label>
                <textarea name="address" />
                <label>Description</label>
                <textarea name="address" />
                <label>Website</label>
                <input type="text" name="email" />
                <label>Email</label>
                <input type="email" name="email" />
                <label>Password</label>
                <input type="password" name="email"  />
                <p>Already have an account? <NavLink to="/login">Login</NavLink></p>
            </div>
            <button formAction={SubmitEvent} className="authButton">Register</button>
        </div>
    )
}