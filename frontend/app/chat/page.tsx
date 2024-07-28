'use client';

import React, { useState, useEffect, useRef } from "react";
import styles from './page.module.css';

export default function ChatPage() {
    const [inputValue, setInputValue] = useState("");
    const [currentPrompt, setCurrentPrompt] = useState(0);
    const [fade, setFade] = useState(true);
    const [chatHistory, setChatHistory] = useState<{ user: string; ai: string; urls?: { title: string; url: string }[] }[]>([]);
    const [showSources, setShowSources] = useState<{ [key: number]: boolean }>({});
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
            setChatHistory([...chatHistory, { user: userMessage, ai: "", urls: [] }]);
            fetchAIResponse(userMessage);
            setInputValue("");
            if (textareaRef.current) {
                textareaRef.current.style.height = 'auto'; // Reset height after submission
            }
        }
    };

    const fetchAIResponse = async (userMessage: string) => {
        try {
            const response = await fetch('http://localhost:8080/api/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ query: userMessage }),
            });

            const responseData = await response.json();

            if (!responseData || !responseData.response) {
                throw new Error('Invalid response format');
            }

            const { text, urls } = responseData.response;

            setChatHistory(prevHistory => {
                const updatedHistory = [...prevHistory];
                updatedHistory[updatedHistory.length - 1].ai = text;
                updatedHistory[updatedHistory.length - 1].urls = urls;
                return updatedHistory;
            });
        } catch (error) {
            console.error('Error fetching AI response:', error);
        }
    };

    const toggleSourcesVisibility = (index: number) => {
        setShowSources(prevShowSources => ({
            ...prevShowSources,
            [index]: !prevShowSources[index]
        }));
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
                            {entry.urls && entry.urls.length > 0 && (
                                <div className={styles.urlToggle}>
                                    <button onClick={() => toggleSourcesVisibility(index)}>
                                        {showSources[index] ? "Hide Sources" : "Show Sources"}
                                    </button>
                                    {showSources[index] && (
                                        <div className={styles.urlList}>
                                            {entry.urls.map((url, urlIndex) => (
                                                <a key={urlIndex} href={url.url} target="_blank" rel="noopener noreferrer">
                                                    {url.title}
                                                </a>
                                            ))}
                                        </div>
                                    )}
                                </div>
                            )}
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
