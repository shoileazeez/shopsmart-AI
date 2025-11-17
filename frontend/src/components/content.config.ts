

import { 
    FaHome, 
    FaShoppingBag, 
    FaInfoCircle, 
    FaEnvelope,
    FaTachometerAlt,
    FaBoxes,
    FaShoppingCart,
    FaRobot,
    FaCamera,
    FaBell,
    FaUser,
    FaCog,
    FaSignOutAlt
} from 'react-icons/fa';
import { IconType } from 'react-icons';

// Navigation Types
export interface NavItem {
    id: string;
    title: string;
    path: string;
    icon: IconType;
    badge?: string;
}

export interface HeaderConfig {
    title: string;
    navigation: NavItem[];
}

// Button Types
export interface ButtonConfig {
    label: string;
    path: string;
    variant?: 'primary' | 'secondary' | 'outline';
}

// Hero Section Types
export interface HeroConfig {
    headline: string;
    description: string;
    primaryButton: ButtonConfig;
    secondaryButton: ButtonConfig;
    backgroundImage?: string;
}

// Feature Section Types
export interface Feature {
    id: string;
    title: string;
    description: string;
    icon: IconType;
}

export interface FeatureSection {
    headline: string;
    subheadline?: string;
    features: Feature[];
}

// Footer Types
export interface FooterLink {
    label: string;
    path: string;
}

export interface FooterSection {
    title: string;
    links: FooterLink[];
}

export interface FooterConfig {
    copyright: string;
    sections: {
        company: FooterSection;
        support: FooterSection;
        legal: FooterSection;
    };
    socialMedia: {
        platform: string;
        url: string;
        icon: IconType;
    }[];
}

// Main Config Type
export interface ContentConfig {
    publicHeader: HeaderConfig;
    privateHeader: HeaderConfig;
    hero: HeroConfig;
    features: FeatureSection;
    footer: FooterConfig;
}

const contentConfig: ContentConfig = {
    publicHeader: {
        title: "ShopSmart AI",
        navigation: [
            { id: "home", title: "Home", path: "/", icon: FaHome },
            { id: "products", title: "Products", path: "/products", icon: FaShoppingBag },
            { id: "about", title: "About Us", path: "/about", icon: FaInfoCircle },
            { id: "contact", title: "Contact", path: "/contact", icon: FaEnvelope }
        ]
    },
    privateHeader: {
        title: "Welcome Back to ShopSmart",
        navigation: [
            { id: "dashboard", title: "Dashboard", path: "/dashboard", icon: FaTachometerAlt },
            { id: "orders", title: "Orders", path: "/orders", icon: FaBoxes },
            { id: "cart", title: "Cart", path: "/cart", icon: FaShoppingCart, badge: "0" },
            { id: "chat", title: "AI Chat", path: "/chat", icon: FaRobot },
            { id: "image-search", title: "Image Search", path: "/image-search", icon: FaCamera },
            { id: "notifications", title: "Notifications", path: "/notifications", icon: FaBell, badge: "New" },
            { id: "profile", title: "Profile", path: "/profile", icon: FaUser },
            { id: "settings", title: "Settings", path: "/settings", icon: FaCog },
            { id: "logout", title: "Logout", path: "/logout", icon: FaSignOutAlt }
        ]
    },
    hero: {
        headline: "Discover Amazing Deals Every Day",
        description: "Experience the future of e-commerce with AI-powered shopping. Find products instantly with text or image search.",
        primaryButton: {
            label: "Shop Now",
            path: "/products",
            variant: "primary"
        },
        secondaryButton: {
            label: "Learn More",
            path: "/about",
            variant: "outline"
        },
        backgroundImage: "/images/hero-background.jpg"
    },
    features: {
        headline: "Shop Smarter with AI",
        subheadline: "Discover the future of shopping with our innovative AI features",
        features: [
            {
                id: "visual-search",
                title: "Visual Search",
                description: "Find products by uploading images or using your camera",
                icon: FaCamera
            },
            {
                id: "ai-assistant",
                title: "AI Shopping Assistant",
                description: "Get personalized recommendations and answers to your questions",
                icon: FaRobot
            },
            {
                id: "smart-cart",
                title: "Smart Cart",
                description: "Intelligent cart management with price tracking and alerts",
                icon: FaShoppingCart
            }
        ]
    },
    footer: {
        copyright: "© 2025 ShopSmart. All rights reserved.",
        sections: {
            company: {
                title: "Company",
                links: [
                    { label: "About Us", path: "/about" },
                    { label: "Careers", path: "/careers" },
                    { label: "Blog", path: "/blog" }
                ]
            },
            support: {
                title: "Support",
                links: [
                    { label: "Help Center", path: "/help" },
                    { label: "Contact Us", path: "/contact" },
                    { label: "FAQs", path: "/faqs" }
                ]
            },
            legal: {
                title: "Legal",
                links: [
                    { label: "Privacy Policy", path: "/privacy" },
                    { label: "Terms of Service", path: "/terms" },
                    { label: "Cookie Policy", path: "/cookies" }
                ]
            }
        },
        socialMedia: [
            { platform: "Twitter", url: "https://twitter.com/shopsmart", icon: FaUser },
            { platform: "Facebook", url: "https://facebook.com/shopsmart", icon: FaUser },
            { platform: "Instagram", url: "https://instagram.com/shopsmart", icon: FaUser }
        ]
    }
};

export default contentConfig;
