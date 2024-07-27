'use client'

import React, { useState } from "react";

export default function ChatPage() {
    const [inputValue, setInputValue] = useState("");

    const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        setInputValue(e.target.value);
    };

    const handleSubmit = (e: React.FormEvent<HTMLFormElement>) => {
        e.preventDefault();
        // Handle the submission logic here
        console.log("Submitted topic:", inputValue);
    };

    return (
        <div className="container mx-auto p-4">
            <header className="text-center my-4">
                <h1 className="text-4xl font-bold">InShort</h1>
                <p className="text-lg">Your personalized news summaries and insights</p>
            </header>
            <main className="flex flex-col items-center pt-20">
                <form onSubmit={handleSubmit} className="form-control w-full max-w-xs">
                    <div className="label">
                        <span className="label-text">Provide a topic you would like today's summary on</span>
                    </div>
                    <input 
                        type="text" 
                        placeholder="Type here" 
                        className="input input-bordered w-full max-w-xs mb-4" 
                        value={inputValue}
                        onChange={handleInputChange}
                    />
                    <button type="submit" className="btn btn-outline btn-info">Submit</button>
                </form>

                <p className="text-lg">just throwing this here</p>
            </main>
            <footer className="text-center text-sm fixed bottom-0 left-0 w-full bg-white py-2">
                <p>© 2024 InShort. All rights reserved.</p>
            </footer>
        </div>
    );
}