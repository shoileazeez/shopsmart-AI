export default function Card({ children }: CardProps) {
    return (
        <div className="bg-white dark:bg-gray-800 shadow-md rounded-lg p-6">
            {children}
        </div>
    );
}

interface CardProps {
    children: React.ReactNode;
}

