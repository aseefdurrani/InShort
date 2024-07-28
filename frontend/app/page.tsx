import React from 'react';
import Link from 'next/link';
import styles from './page.module.css';

const LandingPage: React.FC = () => {
  return (
    <div className={styles.container}>
      <header className={styles.header}>
        <h1>InShort</h1>
        <p>Your personalized news and insights</p>
        <Link href="/chat" className={styles.button}>
          Get Started
        </Link>
      </header>
      <main className={styles.main}>
        <section className={styles.feature}>
          <h2>Personalized Summarization</h2>
          <p>Get summaries tailored to your preferences.</p>
        </section>
        <section className={styles.feature}>
          <h2>Sentiment Analysis</h2>
          <p>Understand the sentiment behind the news.</p>
        </section>
        <section className={styles.feature}>
          <h2>Trend Analysis</h2>
          <p>Discover emerging trends in the news.</p>
        </section>
      </main>
      <footer className={styles.footer}>
        <p>© 2024 InShort. All rights reserved.</p>
      </footer>
    </div>
  );
};

export default LandingPage;
