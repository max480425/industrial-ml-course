import React from 'react';
import { useProgress } from '../context/ProgressContext';
import { useLanguage, LANGUAGE_MODES } from '../context/LanguageContext';
import BilingualBlock from './BilingualBlock';
import VisualSandbox from './VisualSandbox';
import ColabLauncher from './ColabLauncher';
import QuizEngine from './QuizEngine';
import { CheckCircle2, Circle, ArrowLeft, ArrowRight, Clock, Box, Cpu } from 'lucide-react';

export const LessonView = ({ lesson, module, onSelectLesson, allLessons }) => {
  const { isLessonCompleted, toggleLessonCompleted } = useProgress();
  const { langMode } = useLanguage();

  if (!lesson || !module) {
    return (
      <div className="p-8 text-center text-industrial-400 font-mono">
        Select a lesson from the sidebar to begin.
      </div>
    );
  }

  const isCompleted = isLessonCompleted(lesson.id);

  // Find index in allLessons for Prev/Next
  const currentIndex = allLessons.findIndex(l => l.id === lesson.id);
  const prevLesson = currentIndex > 0 ? allLessons[currentIndex - 1] : null;
  const nextLesson = currentIndex < allLessons.length - 1 ? allLessons[currentIndex + 1] : null;

  return (
    <div className="max-w-4xl mx-auto py-6 px-4 sm:px-6 lg:px-8">
      {/* Top Breadcrumb & Status */}
      <div className="flex flex-wrap items-center justify-between gap-3 mb-4 text-xs font-mono">
        <div className="flex items-center gap-2 text-industrial-500 dark:text-industrial-400">
          <span className="text-amber-500 font-bold uppercase tracking-wider">
            MODULE {module.number}: {module.titleEn}
          </span>
          <span>/</span>
          <span>LESSON {lesson.id}</span>
        </div>

        <button
          onClick={() => toggleLessonCompleted(lesson.id)}
          className={`inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg border text-xs font-mono transition cursor-pointer select-none ${
            isCompleted
              ? 'bg-emerald-500/15 border-emerald-500/50 text-emerald-600 dark:text-emerald-400 font-bold'
              : 'bg-industrial-100 dark:bg-industrial-800 border-industrial-300 dark:border-industrial-700 text-industrial-600 dark:text-industrial-400 hover:text-industrial-900 dark:hover:text-white'
          }`}
        >
          {isCompleted ? <CheckCircle2 size={15} /> : <Circle size={15} />}
          <span>{isCompleted ? '✓ Completed' : 'Mark as Complete'}</span>
        </button>
      </div>

      {/* Lesson Main Heading */}
      <div className="pb-6 border-b border-industrial-200 dark:border-industrial-800">
        <h1 className="text-2xl sm:text-3xl font-extrabold text-industrial-900 dark:text-white tracking-tight">
          {langMode === LANGUAGE_MODES.PL_FOCUS ? (lesson.titlePl || lesson.titleEn) : lesson.titleEn}
        </h1>

        {langMode !== LANGUAGE_MODES.PL_FOCUS && lesson.titlePl && (
          <h2 className="text-base sm:text-lg font-medium text-amber-700 dark:text-amber-400/90 mt-1">
            🇵🇱 {lesson.titlePl}
          </h2>
        )}

        {/* Lesson Metadata Badges */}
        <div className="flex flex-wrap items-center gap-3 mt-4 text-xs font-mono text-industrial-600 dark:text-industrial-400">
          <span className="flex items-center gap-1 bg-industrial-100 dark:bg-industrial-800/80 px-2.5 py-1 rounded border border-industrial-200 dark:border-industrial-700">
            <Clock size={13} className="text-amber-500" />
            <span>{lesson.estimatedMinutes || 20} min</span>
          </span>
          <span className="flex items-center gap-1 bg-industrial-100 dark:bg-industrial-800/80 px-2.5 py-1 rounded border border-industrial-200 dark:border-industrial-700">
            <Box size={13} className="text-cyan-500" />
            <span>{lesson.notebook}</span>
          </span>
          <span className="flex items-center gap-1 bg-industrial-100 dark:bg-industrial-800/80 px-2.5 py-1 rounded border border-industrial-200 dark:border-industrial-700">
            <Cpu size={13} className="text-emerald-500" />
            <span>{lesson.sandboxType}</span>
          </span>
        </div>
      </div>

      {/* Summary Bilingual Block */}
      <div className="mt-6">
        <BilingualBlock
          en={lesson.summaryEn}
          pl={lesson.summaryPl}
          titleEn="Lesson Objective & Engineering Context"
          titlePl="Cel Lekcji i Kontekst Przemysłowy"
          type="callout"
          calloutType="engineering"
        />
      </div>

      {/* Main Content Blocks */}
      <div className="my-6 space-y-4">
        {lesson.contentBlocks?.map((block, idx) => (
          <BilingualBlock
            key={block.id || idx}
            en={block.en}
            pl={block.pl}
            titleEn={block.titleEn}
            titlePl={block.titlePl}
            type={block.type || 'paragraph'}
            calloutType={block.calloutType || 'info'}
          />
        ))}
      </div>

      {/* Section 1: Visual Sandbox Lab */}
      <div className="my-8">
        <div className="flex items-center gap-2 mb-2">
          <span className="w-2 h-2 rounded-full bg-amber-500 animate-pulse"></span>
          <h2 className="text-sm font-bold uppercase tracking-wider font-mono text-industrial-500 dark:text-industrial-400">
            Part 1: Interactive Engineering Sandbox
          </h2>
        </div>
        <VisualSandbox type={lesson.sandboxType} />
      </div>

      {/* Section 2: Colab Launcher Card & Tasks */}
      <div className="my-8">
        <div className="flex items-center gap-2 mb-2">
          <span className="w-2 h-2 rounded-full bg-cyan-500"></span>
          <h2 className="text-sm font-bold uppercase tracking-wider font-mono text-industrial-500 dark:text-industrial-400">
            Part 2: 1-Click Google Colab Notebook
          </h2>
        </div>
        <ColabLauncher lesson={lesson} />
      </div>

      {/* Section 3: Interactive Bilingual Quiz */}
      <div className="my-8">
        <div className="flex items-center gap-2 mb-2">
          <span className="w-2 h-2 rounded-full bg-emerald-500"></span>
          <h2 className="text-sm font-bold uppercase tracking-wider font-mono text-industrial-500 dark:text-industrial-400">
            Part 3: Knowledge Check Quiz
          </h2>
        </div>
        <QuizEngine lesson={lesson} />
      </div>

      {/* Navigation Buttons Prev / Next */}
      <div className="mt-12 pt-6 border-t border-industrial-200 dark:border-industrial-800 flex items-center justify-between gap-4 font-mono text-xs">
        {prevLesson ? (
          <button
            onClick={() => onSelectLesson(prevLesson)}
            className="inline-flex items-center gap-2 px-4 py-2.5 rounded-lg border border-industrial-300 dark:border-industrial-700 bg-white dark:bg-industrial-800 hover:bg-industrial-100 dark:hover:bg-industrial-750 text-industrial-800 dark:text-industrial-200 transition"
          >
            <ArrowLeft size={14} />
            <div className="text-left">
              <div className="text-[10px] text-industrial-500">PREVIOUS</div>
              <div className="font-bold truncate max-w-[140px] sm:max-w-xs">{prevLesson.titleEn}</div>
            </div>
          </button>
        ) : <div />}

        {nextLesson && (
          <button
            onClick={() => onSelectLesson(nextLesson)}
            className="inline-flex items-center gap-2 px-4 py-2.5 rounded-lg border border-industrial-300 dark:border-industrial-700 bg-white dark:bg-industrial-800 hover:bg-industrial-100 dark:hover:bg-industrial-750 text-industrial-800 dark:text-industrial-200 transition"
          >
            <div className="text-right">
              <div className="text-[10px] text-industrial-500">NEXT LESSON</div>
              <div className="font-bold truncate max-w-[140px] sm:max-w-xs">{nextLesson.titleEn}</div>
            </div>
            <ArrowRight size={14} />
          </button>
        )}
      </div>
    </div>
  );
};

export default LessonView;
