import React, { createContext, useContext, useState, useEffect } from 'react';

const ProgressContext = createContext();

export const ProgressProvider = ({ children }) => {
  const [completedLessons, setCompletedLessons] = useState(() => {
    try {
      const saved = localStorage.getItem('industrial_ml_completed_lessons');
      return saved ? JSON.parse(saved) : [];
    } catch {
      return [];
    }
  });

  const [checkedTasks, setCheckedTasks] = useState(() => {
    try {
      const saved = localStorage.getItem('industrial_ml_checked_tasks');
      return saved ? JSON.parse(saved) : {};
    } catch {
      return {};
    }
  });

  const [quizScores, setQuizScores] = useState(() => {
    try {
      const saved = localStorage.getItem('industrial_ml_quiz_scores');
      return saved ? JSON.parse(saved) : {};
    } catch {
      return {};
    }
  });

  useEffect(() => {
    try {
      localStorage.setItem('industrial_ml_completed_lessons', JSON.stringify(completedLessons));
    } catch (e) {
      console.warn('Failed to save completed lessons', e);
    }
  }, [completedLessons]);

  useEffect(() => {
    try {
      localStorage.setItem('industrial_ml_checked_tasks', JSON.stringify(checkedTasks));
    } catch (e) {
      console.warn('Failed to save checked tasks', e);
    }
  }, [checkedTasks]);

  useEffect(() => {
    try {
      localStorage.setItem('industrial_ml_quiz_scores', JSON.stringify(quizScores));
    } catch (e) {
      console.warn('Failed to save quiz scores', e);
    }
  }, [quizScores]);

  const toggleLessonCompleted = (lessonId) => {
    setCompletedLessons(prev => {
      if (prev.includes(lessonId)) {
        return prev.filter(id => id !== lessonId);
      } else {
        return [...prev, lessonId];
      }
    });
  };

  const markLessonCompleted = (lessonId) => {
    setCompletedLessons(prev => (prev.includes(lessonId) ? prev : [...prev, lessonId]));
  };

  const isLessonCompleted = (lessonId) => completedLessons.includes(lessonId);

  const toggleTaskCheck = (lessonId, taskId) => {
    setCheckedTasks(prev => {
      const currentList = prev[lessonId] || [];
      const updated = currentList.includes(taskId)
        ? currentList.filter(id => id !== taskId)
        : [...currentList, taskId];
      return { ...prev, [lessonId]: updated };
    });
  };

  const isTaskChecked = (lessonId, taskId) => {
    const list = checkedTasks[lessonId] || [];
    return list.includes(taskId);
  };

  const saveQuizScore = (lessonId, score) => {
    setQuizScores(prev => ({ ...prev, [lessonId]: score }));
  };

  return (
    <ProgressContext.Provider
      value={{
        completedLessons,
        toggleLessonCompleted,
        markLessonCompleted,
        isLessonCompleted,
        checkedTasks,
        toggleTaskCheck,
        isTaskChecked,
        quizScores,
        saveQuizScore,
      }}
    >
      {children}
    </ProgressContext.Provider>
  );
};

export const useProgress = () => {
  const context = useContext(ProgressContext);
  if (!context) {
    throw new Error('useProgress must be used within a ProgressProvider');
  }
  return context;
};
