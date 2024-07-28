'use client';

import React, { useState, useEffect, useRef } from "react";
import styles from './page.module.css';

export default function ChatPage() {
    // State variables
    const [inputValue, setInputValue] = useState("");
    const [currentPrompt, setCurrentPrompt] = useState(0);
    const [fade, setFade] = useState(true);
    const [response, setResponse] = useState(""); // State to store the response
    const [chatHistory, setChatHistory] = useState<{ user: string; ai: string }[]>([]);
    const textareaRef = useRef<HTMLTextAreaElement>(null);
    const chatEndRef = useRef<HTMLDivElement>(null);

    // List of prompts
    const prompts = [
        "How are the global stock markets performing?",
        "Give me updates on the Olympics",
        "What are the latest tech trends?",
        "Any new medical developments?",
        "What are the recent advancements in AI?",
        "Tell me about the latest in politics",
        "What are the top headlines today?",
        "What's new in the entertainment industry?"
    ];
    useEffect(() => {
        const interval = setInterval(() => {
            setFade(false);
            setTimeout(() => {
                setCurrentPrompt((prevPrompt) => (prevPrompt + 1) % prompts.length);
                setFade(true);
            }, 500); // Time for fade-out effect
        }, 4000); // Change prompt every 4 seconds

        return () => clearInterval(interval);
    }, [prompts.length]);

    // Handle input change in the textarea
    const handleInputChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
        setInputValue(e.target.value);
        if (textareaRef.current) {
            textareaRef.current.style.height = 'auto'; // Reset the height
            textareaRef.current.style.height = `${textareaRef.current.scrollHeight}px`; // Set to the new scrollHeight
        }
    };

    // Handle key down event in the textarea
    const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            handleSubmit(e as unknown as React.FormEvent<HTMLFormElement>);
        }
    };

    // Handle form submission
    const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
        e.preventDefault();
        try {
            const response = await fetch("http://localhost:8080/api/chat", {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ query: inputValue })
            });
            const data = await response.json();
            setResponse(data.response); // Update the response state
            console.log("Received response:", data.response);
        } catch (error) {
            console.error("Error fetching response:", error);
        }
        console.log("Submitted topic:", inputValue);
        const userMessage = inputValue.trim();
        if (userMessage) {
            const aiResponse = `Response to "${userMessage}"`; // Replace this with actual AI response logic
            setChatHistory([...chatHistory, { user: userMessage, ai: aiResponse }]);
            setInputValue("");
            if (textareaRef.current) {
                textareaRef.current.style.height = 'auto'; // Reset height after submission
            }
            if (chatEndRef.current) {
                chatEndRef.current.scrollIntoView({ behavior: 'smooth' });
            }
        }
    };

    return (
        <div className={styles.container}>
            <header className={styles.header}>
                <h1>InShort</h1>
                <p>Your personalized news and insights</p>
            </header>
            <main className={styles.main}>
                <div className={styles.prompts}>
                    <div className={`${styles.label} ${fade ? styles.fadeIn : styles.fadeOut}`}>
                        <span className={styles.labelText}>{prompts[currentPrompt]}</span>
                    </div>
                </div>
                <div className={styles.chatbox}>
                    {chatHistory.map((entry, index) => (
                        <div key={index} className={styles.chatEntry}>
                            <div className={styles.userMessage}>{entry.user}</div>
                            <div className={styles.aiMessage}>{entry.ai}</div>
                        </div>
                    ))}
                    <div ref={chatEndRef}></div>
                </div>
                <form onSubmit={handleSubmit} className={styles.form}>
                    <div className={styles.inputWrapper}>
                        <textarea
                            ref={textareaRef}
                            placeholder="What's on your mind?"
                            className={styles.textarea}
                            value={inputValue}
                            onChange={handleInputChange}
                            onKeyDown={handleKeyDown}
                            rows={1}
                        />
                        <button type="submit" className={styles.submitButton}>
                            ➤
                        </button>
                    </div>
                </form>
            </main>
            <footer className={styles.footer}>
                <p>© 2024 InShort. All rights reserved.</p>
            </footer>
        </div>
    );
}