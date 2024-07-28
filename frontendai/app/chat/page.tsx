'use client';

import React, { useState, useEffect, useRef } from "react";
import styles from './page.module.css';

export default function ChatPage() {
    const [inputValue, setInputValue] = useState("");
    const [currentPrompt, setCurrentPrompt] = useState(0);
    const [fade, setFade] = useState(true);
    const textareaRef = useRef<HTMLTextAreaElement>(null);

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
        // Handle the submission logic here
        console.log("Submitted topic:", inputValue);
    };

    return (
        <div className={styles.container}>
            <header className={styles.header}>
                <h1>InShort</h1>
                <p>Your personalized news and insights</p>
            </header>
            <main className={styles.main}>
                <form onSubmit={handleSubmit} className={styles.form}>
                    <div className={`${styles.label} ${fade ? styles.fadeIn : styles.fadeOut}`}>
                        <span className={styles.labelText}>{prompts[currentPrompt]}</span>
                    </div>
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
