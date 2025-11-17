'use client';

import React, { useState } from "react";
import Link from 'next/link';
import contentConfig from "../content.config";
import { FaBars, FaTimes, FaShoppingCart, FaUser } from 'react-icons/fa';

interface NavItem {
    id: string | number;
    path: string;
    title: string;
    icon: React.ComponentType<any>;
    badge?: string | number | null;
    }

export default function PrivateHeader({ navigation }: { navigation: NavItem[] }) {
    const [isMenuOpen, setIsMenuOpen] = useState(false);
    const header = {
        title: contentConfig.privateHeader.title,
        navigation: navigation,
    };

    const toggleMenu = () => {
        setIsMenuOpen(!isMenuOpen);
    };

    return (
        <header className="fixed w-full top-0 z-50 bg-white dark:bg-gray-900 shadow-md">
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                <div className="flex justify-between items-center h-16">
                    {/* Logo and Title */}
                    <div className="shrink-0 flex items-center">
                        <Link href="/" className="flex items-center">
                            <h1 className="text-xl md:text-2xl font-bold text-gray-900 dark:text-white">
                                {header.title}
                            </h1>
                        </Link>
                    </div>

                    {/* Desktop Navigation */}
                    <nav className="hidden md:flex space-x-8">
                        {(() => {

                            return header.navigation.map((item: NavItem) => (
                                <Link
                                    key={item.id}
                                    href={item.path}
                                    className="flex items-center text-gray-700 dark:text-gray-200 hover:text-primary-600 dark:hover:text-primary-400 px-3 py-2 rounded-md text-sm font-medium transition-colors"
                                >
                                    <item.icon className="h-5 w-5 mr-2" />
                                    <span>{item.title}</span>
                                    {item.badge && (
                                        <span className="ml-2 inline-flex items-center px-2 py-0.5 rounded text-xs font-medium bg-primary-100 text-primary-800 dark:bg-primary-800 dark:text-primary-100">
                                            {item.badge}
                                        </span>
                                    )}
                                </Link>
                            ));
                        })()}
                    </nav>

                    {/* User Actions - Desktop */}
                    <div className="hidden md:flex items-center space-x-4">
                        <Link href="/cart" className="text-gray-700 dark:text-gray-200 hover:text-primary-600 dark:hover:text-primary-400">
                            <FaShoppingCart className="h-6 w-6" />
                        </Link>
                        <Link href="/profile" className="text-gray-700 dark:text-gray-200 hover:text-primary-600 dark:hover:text-primary-400">
                            <FaUser className="h-6 w-6" />
                        </Link>
                    </div>

                    {/* Mobile menu button */}
                    <div className="md:hidden flex items-center">
                        <button
                            onClick={toggleMenu}
                            className="inline-flex items-center justify-center p-2 rounded-md text-gray-700 dark:text-gray-200 hover:text-primary-600 dark:hover:text-primary-400 focus:outline-none"
                            aria-expanded="false"
                        >
                            <span className="sr-only">Open main menu</span>
                            {isMenuOpen ? (
                                <FaTimes className="h-6 w-6" />
                            ) : (
                                <FaBars className="h-6 w-6" />
                            )}
                        </button>
                    </div>
                </div>

                {/* Mobile menu */}
                <div className={`${isMenuOpen ? 'block' : 'hidden'} md:hidden`}>
                    <div className="px-2 pt-2 pb-3 space-y-1 sm:px-3">
                        {navigation.map((item: NavItem) => (
                            <Link
                                key={item.id}
                                href={item.path}
                                className="flex items-center text-gray-700 dark:text-gray-200 hover:text-primary-600 dark:hover:text-primary-400 px-3 py-2 rounded-md text-base font-medium"
                                onClick={() => setIsMenuOpen(false)}
                            >
                                <item.icon className="h-5 w-5 mr-3" />
                                <span>{item.title}</span>
                                {item.badge && (
                                    <span className="ml-2 inline-flex items-center px-2 py-0.5 rounded text-xs font-medium bg-primary-100 text-primary-800 dark:bg-primary-800 dark:text-primary-100">
                                        {item.badge}
                                    </span>
                                )}
                            </Link>
                        ))}
                        
                        {/* Mobile User Actions */}
                        <div className="flex items-center space-x-4 px-3 py-2">
                            <Link
                                href="/cart"
                                className="flex items-center text-gray-700 dark:text-gray-200 hover:text-primary-600 dark:hover:text-primary-400"
                                onClick={() => setIsMenuOpen(false)}
                            >
                                <FaShoppingCart className="h-5 w-5 mr-3" />
                                <span>Cart</span>
                            </Link>
                            <Link
                                href="/profile"
                                className="flex items-center text-gray-700 dark:text-gray-200 hover:text-primary-600 dark:hover:text-primary-400"
                                onClick={() => setIsMenuOpen(false)}
                            >
                                <FaUser className="h-5 w-5 mr-3" />
                                <span>Profile</span>
                            </Link>
                        </div>
                    </div>
                </div>
            </div>
        </header>
    );
}