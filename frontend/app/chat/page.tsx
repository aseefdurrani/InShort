'use client';

import React, { useState, useEffect, useRef } from "react";
import styles from './page.module.css';
const BACKEND_URL = 'http://localhost:5001'; // Hardcoded backend URL

export default function ChatPage() {
    const [inputValue, setInputValue] = useState("");
    const [currentPrompt, setCurrentPrompt] = useState(0);
    const [fade, setFade] = useState(true);
    const [chatHistory, setChatHistory] = useState<{ user: string; ai: string }[]>([]);
    const textareaRef = useRef<HTMLTextAreaElement>(null);
    const chatEndRef = useRef<HTMLDivElement>(null);
    const chatContainerRef = useRef<HTMLDivElement>(null);

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

    useEffect(() => {
        if (chatEndRef.current && chatContainerRef.current) {
            chatContainerRef.current.scrollTo({
                top: chatContainerRef.current.scrollHeight,
                behavior: 'smooth'
            });
        }
    }, [chatHistory]);

    const handleInputChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
        setInputValue(e.target.value);
        if (textareaRef.current) {
            textareaRef.current.style.height = 'auto'; // Reset the height
            textareaRef.current.style.height = `${textareaRef.current.scrollHeight}px`; // Set to the new scrollHeight
        }
    };

    const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            handleSubmit(e as unknown as React.FormEvent<HTMLFormElement>);
        }
    };

    const handleSubmit = (e: React.FormEvent<HTMLFormElement>) => {
        e.preventDefault();
        const userMessage = inputValue.trim();
        if (userMessage) {
            setChatHistory([...chatHistory, { user: userMessage, ai: "" }]);
            fetchAIResponse(userMessage);
            setInputValue("");
            if (textareaRef.current) {
                textareaRef.current.style.height = 'auto'; // Reset height after submission
            }
        }
    };

    const fetchAIResponse = async (userMessage: string) => {
        try {
            const response = await fetch(`${process.env.NEXT_PUBLIC_BACKEND_URL}/api/chat`, {
            // const response = await fetch(`${BACKEND_URL}/api/chat`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ query: userMessage }),
            });
    
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
    
            const responseText = await response.text(); // Get response as text first
            let responseData: { response: string; };
    
            try {
                responseData = JSON.parse(responseText); // Attempt to parse the JSON
            } catch (error) {
                console.error('Error parsing JSON:', error);
                console.error('Response text:', responseText);
                throw new Error('Invalid JSON response');
            }
    
            setChatHistory(prevHistory => {
                const updatedHistory = [...prevHistory];
                updatedHistory[updatedHistory.length - 1].ai = responseData.response;
                return updatedHistory;
            });
        } catch (error) {
            console.error('Error fetching AI response:', error);
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
                <div className={styles.chatbox} ref={chatContainerRef}>
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
