import React from "react"


const Button = ({ label, onClick, variant = "primary" }: ButtonProps) => {
    const baseClasses = "px-4 py-2 rounded font-medium focus:outline-none focus:ring-2 focus:ring-offset-2 transition-colors";
    const variantClasses = {
        primary: "bg-primary-600 text-white hover:bg-primary-700 focus:ring-primary-500",
        secondary: "bg-secondary-600 text-white hover:bg-secondary-700 focus:ring-secondary-500",
        outline: "border border-primary-600 text-primary-600 hover:bg-primary-50 focus:ring-primary-500",
    };
    const classes = `${baseClasses} ${variantClasses[variant]}`;
    return (
        <button className={classes} onClick={onClick}>
            {label}
        </button>
    );
};

export default Button;
interface ButtonProps {
    label: string;
    onClick: () => void;
    variant?: 'primary' | 'secondary' | 'outline';
}