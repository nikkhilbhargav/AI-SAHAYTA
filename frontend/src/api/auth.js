import api from "./api";

// Login API
export const loginUser = async (email, password) => {

    const response = await api.post("/auth/login", {
        email,
        password
    });

    return response.data;
};

// Register API
export const registerUser = async (userData) => {

    const response = await api.post("/auth/register", userData);

    return response.data;
};