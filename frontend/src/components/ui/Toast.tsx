import React from "react";
import { ToastContainer, toast, ToastOptions, Slide } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";

// /c:/Users/Projects/shopsmart-AI/frontend/src/components/ui/Toast.tsx

type Variant = "success" | "error" | "info" | "warning";

const DEFAULT_OPTIONS: ToastOptions = {
    position: "top-right",
    autoClose: 4000,
    hideProgressBar: false,
    closeOnClick: true,
    pauseOnHover: true,
    draggable: true,
    progress: undefined,
    transition: Slide,
    theme: "light",
};

export function showToast(
    message: React.ReactNode,
    variant: Variant = "info",
    options?: Partial<ToastOptions>
) {
    const opts: ToastOptions = { ...DEFAULT_OPTIONS, ...options };

    switch (variant) {
        case "success":
            return toast.success(message, opts);
        case "error":
            return toast.error(message, opts);
        case "warning":
            return toast.warn(message, opts);
        case "info":
        default:
            return toast.info(message, opts);
    }
}

export const toastSuccess = (message: React.ReactNode, options?: Partial<ToastOptions>) =>
    showToast(message, "success", options);
export const toastError = (message: React.ReactNode, options?: Partial<ToastOptions>) =>
    showToast(message, "error", options);
export const toastInfo = (message: React.ReactNode, options?: Partial<ToastOptions>) =>
    showToast(message, "info", options);
export const toastWarning = (message: React.ReactNode, options?: Partial<ToastOptions>) =>
    showToast(message, "warning", options);

/**
 * Toast component to place once in your app (e.g. in App.tsx or Layout)
 * It renders the container that displays toasts triggered via showToast / helpers above.
 */
export default function Toast(): React.ReactElement {
    return (
        <ToastContainer
            position={DEFAULT_OPTIONS.position}
            autoClose={DEFAULT_OPTIONS.autoClose}
            hideProgressBar={DEFAULT_OPTIONS.hideProgressBar}
            newestOnTop={false}
            closeOnClick={DEFAULT_OPTIONS.closeOnClick}
            rtl={false}
            pauseOnFocusLoss
            draggable={DEFAULT_OPTIONS.draggable}
            pauseOnHover={DEFAULT_OPTIONS.pauseOnHover}
            transition={DEFAULT_OPTIONS.transition}
            theme={DEFAULT_OPTIONS.theme}
        />
    );
}