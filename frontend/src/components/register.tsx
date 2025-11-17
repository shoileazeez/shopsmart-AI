import { useAuthActions } from "@/src/hooks/useAuthActions";
import React, { useState } from 'react';
import { toastSuccess, toastError } from '@/src/components/ui/Toast';
import { RegisterCredentials } from "@/src/types/auth.types";
import { useRouter } from 'next/router';


const Register = () => {
    const { register, isLoading, error } = useAuthActions();
    const router = useRouter();
    const [formData, setFormData] = useState({
        email: '',
        password: '',
        confirm_password: '',
        first_name: '',
        last_name: ''
    });
    const [successMessage, setSuccessMessage] = useState<string | null>(null);

    const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        const { name, value } = e.target;
        setFormData((prev) => ({ ...prev, [name]: value }));
    };

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setSuccessMessage(null);
        if (formData.password !== formData.confirm_password) {
            return;
        }
        const response = await register({
            email: formData.email,
            password: formData.password,
            confirm_password: formData.confirm_password,
            first_name: formData.first_name,
            last_name: formData.last_name
        });
        // AuthResponse may not have an 'error' property in its type, so cast to any and check common fields.
        if (response.success) {
            setSuccessMessage("Registration successful!");
            toastSuccess("Registration successful!");

            router.push('/dashboard'); // Redirect to dashboard or desired page
        }
    };
    return (
        <div className="max-w-md mx-auto mt-10 p-6 border border-gray-300 rounded-lg shadow-md">
            <h2 className="text-2xl font-bold mb-6 text-center">Register</h2>
            <form onSubmit={handleSubmit}>
                {error && <div className="error">{error}</div>}
                <div className="mb-4">
                    <label htmlFor="email" className="block text-sm font-medium text-gray-700">Email</label>
                    <input
                        type="email"
                        name="email"
                        id="email"
                        value={formData.email}
                        onChange={handleChange}
                        required
                        className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm p-2"
                    />
                </div>
                <div className="mb-4">
                    <label htmlFor="password" className="block text-sm font-medium text-gray-700">Password</label>
                    <input
                        type="password"
                        name="password"
                        id="password"
                        value={formData.password}
                        onChange={handleChange}
                        required
                        className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm p-2"
                    />
                </div>
                <div className="mb-4">
                    <label htmlFor="confirm_password" className="block text-sm font-medium text-gray-700">Confirm Password</label>
                    <input
                        type="password"
                        name="confirm_password"
                        id="confirm_password"
                        value={formData.confirm_password}
                        onChange={handleChange}
                        required
                        className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm p-2"
                    />
                </div>
                <div className="mb-4">
                    <label htmlFor="first_name" className="block text-sm font-medium text-gray-700">First Name</label>
                    <input
                        type="text"
                        name="first_name"
                        id="first_name"
                        value={formData.first_name}
                        onChange={handleChange}
                        required
                        className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm p-2"
                    />
                </div>
                <div className="mb-4">
                    <label htmlFor="last_name" className="block text-sm font-medium text-gray-700">Last Name</label>
                    <input
                        type="text"
                        name="last_name"
                        id="last_name"
                        value={formData.last_name}
                        onChange={handleChange}
                        required
                        className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm p-2"
                    />
                </div>
                <button
                    type="submit"
                    disabled={isLoading}
                    className={`mt-4 w-full bg-blue-600 text-white font-semibold py-2 px-4 rounded-md shadow-sm ${isLoading ? 'opacity-50 cursor-not-allowed' : ''}`}
                >
                    {isLoading ? 'Registering...' : 'Register'}
                </button>
            </form>
        </div>
    );
};

export default Register;
