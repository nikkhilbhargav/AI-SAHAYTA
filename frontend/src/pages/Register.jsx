import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { registerUser } from "../api/auth";

function Register() {

    const navigate = useNavigate();

    const [full_name, setFullName] = useState("");
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");

    const [loading, setLoading] = useState(false);
    const [error, setError] = useState("");

    const handleSubmit = async (e) => {

        e.preventDefault();

        try {

            setLoading(true);
            setError("");

            await registerUser({
                full_name,
                email,
                password
            });

            alert("Registration Successful!");

            navigate("/");

        } catch (err) {

            setError(
                err.response?.data?.detail ||
                "Registration failed."
            );

        } finally {

            setLoading(false);

        }

    };

    return (

        <div className="min-h-screen bg-slate-900 flex items-center justify-center p-6">

            <div className="w-full max-w-md bg-slate-800 rounded-2xl shadow-2xl p-8">

                <div className="text-center mb-8">

                    <h1 className="text-4xl font-bold text-blue-500">
                        AI SAHAYTA
                    </h1>

                    <p className="text-gray-400 mt-2">
                        Create your account
                    </p>

                </div>

                <form
                    className="space-y-5"
                    onSubmit={handleSubmit}
                >

                    <div>

                        <label className="block text-gray-300 mb-2">
                            Full Name
                        </label>

                        <input
                            type="text"
                            value={full_name}
                            onChange={(e)=>setFullName(e.target.value)}
                            placeholder="Enter your full name"
                            required
                            className="w-full rounded-lg bg-slate-700 border border-slate-600 px-4 py-3 text-white"
                        />

                    </div>

                    <div>

                        <label className="block text-gray-300 mb-2">
                            Email
                        </label>

                        <input
                            type="email"
                            value={email}
                            onChange={(e)=>setEmail(e.target.value)}
                            placeholder="Enter your email"
                            required
                            className="w-full rounded-lg bg-slate-700 border border-slate-600 px-4 py-3 text-white"
                        />

                    </div>

                    <div>

                        <label className="block text-gray-300 mb-2">
                            Password
                        </label>

                        <input
                            type="password"
                            value={password}
                            onChange={(e)=>setPassword(e.target.value)}
                            placeholder="Create password"
                            required
                            className="w-full rounded-lg bg-slate-700 border border-slate-600 px-4 py-3 text-white"
                        />

                    </div>

                    {error && (
                        <p className="text-red-500">
                            {error}
                        </p>
                    )}

                    <button
                        type="submit"
                        disabled={loading}
                        className="w-full bg-blue-600 hover:bg-blue-700 py-3 rounded-lg text-white"
                    >
                        {loading ? "Registering..." : "Register"}
                    </button>

                </form>

                <p className="text-center text-gray-400 mt-6">

                    Already have an account?

                    <Link
                        to="/"
                        className="text-blue-400 ml-2"
                    >
                        Login
                    </Link>

                </p>

            </div>

        </div>

    );

}

export default Register;