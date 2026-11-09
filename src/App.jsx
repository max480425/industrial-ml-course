import React, { useState, useEffect } from 'react';
import syllabusData from './data/syllabus.json';
import { LanguageProvider } from './context/LanguageContext';
import { ProgressProvider } from './context/ProgressContext';
import Layout from './components/Layout';
import LessonView from './components/LessonView';

export function App() {
  // Flatten all lessons
  const allLessons = syllabusData.flatMap(m => m.lessons);

  // Initialize active lesson from URL hash or default to 1-1
  const [activeLesson, setActiveLesson] = useState(() => {
    const hash = window.location.hash.replace(/^#/, '');
    if (hash) {
      const found = allLessons.find(l => l.id === hash);
      if (found) return found;
    }
    return allLessons[0] || null;
  });

  // Find module corresponding to active lesson
  const activeModule = syllabusData.find(m =>
    m.lessons.some(l => l.id === activeLesson?.id)
  ) || syllabusData[0];

  const handleSelectLesson = (lesson) => {
    setActiveLesson(lesson);
    window.location.hash = lesson.id;
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  // Sync with browser back/forward buttons
  useEffect(() => {
    const handleHashChange = () => {
      const hash = window.location.hash.replace(/^#/, '');
      if (hash) {
        const found = allLessons.find(l => l.id === hash);
        if (found) {
          setActiveLesson(found);
          window.scrollTo({ top: 0, behavior: 'smooth' });
        }
      }
    };

    window.addEventListener('hashchange', handleHashChange);
    return () => window.removeEventListener('hashchange', handleHashChange);
  }, [allLessons]);

  return (
    <LanguageProvider>
      <ProgressProvider>
        <Layout
          activeLesson={activeLesson}
          onSelectLesson={handleSelectLesson}
        >
          <LessonView
            lesson={activeLesson}
            module={activeModule}
            onSelectLesson={handleSelectLesson}
            allLessons={allLessons}
          />
        </Layout>
      </ProgressProvider>
    </LanguageProvider>
  );
}

export default App;
