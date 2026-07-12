import { Link } from "react-router-dom";

function NotFound() {
    return (
        <div className="flex flex-col items-center justify-center min-h-screen bg-slate-900 text-white gap-6">
            <h1 className="text-6xl font-bold">404</h1>

            <p>Page Not Found</p>

            <Link
                to="/"
                className="px-5 py-3 bg-blue-600 rounded-lg hover:bg-blue-700 transition"
            >
                Go to Login
            </Link>
        </div>
    );
}

export default NotFound;