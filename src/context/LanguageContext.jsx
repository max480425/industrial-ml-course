import React, { createContext, useContext, useState, useEffect } from 'react';

const LanguageContext = createContext();

export const LANGUAGE_MODES = {
  EN_TOGGLE: 'en-toggle', // "EN + [PL Toggle]"
  SIDE_BY_SIDE: 'side-by-side', // "Side-by-Side EN/PL"
  PL_FOCUS: 'pl-focus', // "PL Focus"
};

export const LanguageProvider = ({ children }) => {
  const [langMode, setLangMode] = useState(() => {
    try {
      const saved = localStorage.getItem('industrial_ml_lang_mode');
      return saved || LANGUAGE_MODES.EN_TOGGLE;
    } catch {
      return LANGUAGE_MODES.EN_TOGGLE;
    }
  });

  const [theme, setTheme] = useState(() => {
    try {
      const saved = localStorage.getItem('industrial_ml_theme');
      return saved || 'dark';
    } catch {
      return 'dark';
    }
  });

  useEffect(() => {
    try {
      localStorage.setItem('industrial_ml_lang_mode', langMode);
    } catch (e) {
      console.warn('Failed to save lang mode to localStorage', e);
    }
  }, [langMode]);

  useEffect(() => {
    try {
      localStorage.setItem('industrial_ml_theme', theme);
      if (theme === 'dark') {
        document.documentElement.classList.add('dark');
      } else {
        document.documentElement.classList.remove('dark');
      }
    } catch (e) {
      console.warn('Failed to save theme to localStorage', e);
    }
  }, [theme]);

  const toggleTheme = () => {
    setTheme(prev => (prev === 'dark' ? 'light' : 'dark'));
  };

  return (
    <LanguageContext.Provider value={{ langMode, setLangMode, theme, setTheme, toggleTheme }}>
      {children}
    </LanguageContext.Provider>
  );
};

export const useLanguage = () => {
  const context = useContext(LanguageContext);
  if (!context) {
    throw new Error('useLanguage must be used within a LanguageProvider');
  }
  return context;
};
