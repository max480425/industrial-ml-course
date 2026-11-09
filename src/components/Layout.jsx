import React, { useState } from 'react';
import syllabusData from '../data/syllabus.json';
import { useProgress } from '../context/ProgressContext';
import { useLanguage, LANGUAGE_MODES } from '../context/LanguageContext';
import GlossaryModal from './GlossaryModal';
import {
  Activity,
  BarChart2,
  DollarSign,
  Cpu,
  Radio,
  Scan,
  Zap,
  CheckCircle2,
  Circle,
  ChevronDown,
  ChevronRight,
  Sun,
  Moon,
  Menu,
  X,
  BookOpen,
  Search,
  ExternalLink,
  Github,
  Globe,
  Sliders,
} from 'lucide-react';

const MODULE_ICONS = {
  1: Activity,
  2: BarChart2,
  3: DollarSign,
  4: Cpu,
  5: Radio,
  6: Scan,
  7: Zap,
};

export const Layout = ({ activeLesson, onSelectLesson, children }) => {
  const { completedLessons, isLessonCompleted } = useProgress();
  const { langMode, setLangMode, theme, toggleTheme } = useLanguage();

  const [isSidebarOpen, setIsSidebarOpen] = useState(false);
  const [expandedModules, setExpandedModules] = useState(() => {
    // Default expand active module or module 1
    return [activeLesson ? parseInt(activeLesson.id.split('-')[0], 10) : 1];
  });
  const [searchQuery, setSearchQuery] = useState('');
  const [isGlossaryOpen, setIsGlossaryOpen] = useState(false);

  // Flatten all 28 lessons for global stats
  const allLessons = syllabusData.flatMap(m => m.lessons);
  const totalLessons = allLessons.length;
  const completedCount = completedLessons.length;
  const progressPercent = Math.round((completedCount / totalLessons) * 100);

  const toggleModuleAccordion = (modNum) => {
    setExpandedModules(prev =>
      prev.includes(modNum) ? prev.filter(m => m !== modNum) : [...prev, modNum]
    );
  };

  // Filter lessons if searching
  const filteredModules = syllabusData.map(mod => {
    if (!searchQuery.trim()) return mod;
    const q = searchQuery.toLowerCase();
    const matchingLessons = mod.lessons.filter(
      l =>
        l.titleEn.toLowerCase().includes(q) ||
        l.titlePl?.toLowerCase().includes(q) ||
        l.id.toLowerCase().includes(q)
    );
    return { ...mod, lessons: matchingLessons };
  }).filter(mod => mod.lessons.length > 0);

  return (
    <div className="min-h-screen flex flex-col bg-industrial-50 dark:bg-industrial-950 text-industrial-900 dark:text-industrial-100 font-sans selection:bg-amber-500/20 selection:text-amber-500">
      {/* Top Header Navbar */}
      <header className="sticky top-0 z-40 bg-white/90 dark:bg-industrial-900/90 backdrop-blur-md border-b border-industrial-200 dark:border-industrial-800">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between gap-4">
          {/* Left: Mobile hamburger & Logo */}
          <div className="flex items-center gap-3">
            <button
              onClick={() => setIsSidebarOpen(!isSidebarOpen)}
              className="lg:hidden p-2 rounded-lg text-industrial-600 dark:text-industrial-400 hover:bg-industrial-100 dark:hover:bg-industrial-800 transition"
              aria-label="Toggle Navigation"
            >
              {isSidebarOpen ? <X size={20} /> : <Menu size={20} />}
            </button>

            <div className="flex items-center gap-2.5">
              <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-amber-400 to-amber-600 flex items-center justify-center text-industrial-950 font-black font-mono text-sm shadow-md shadow-amber-500/20">
                IML
              </div>
              <div>
                <h1 className="text-sm sm:text-base font-extrabold tracking-tight text-industrial-900 dark:text-white flex items-center gap-1.5">
                  <span>Industrial Machine Learning</span>
                  <span className="hidden sm:inline-block text-[10px] font-mono px-1.5 py-0.2 bg-amber-500/10 text-amber-600 dark:text-amber-400 border border-amber-500/20 rounded">
                    LAB
                  </span>
                </h1>
                <p className="hidden md:block text-[11px] font-mono text-industrial-500 dark:text-industrial-400">
                  Dual-Language Predictive Maintenance · 7 Modules · 28 Lessons
                </p>
              </div>
            </div>
          </div>

          {/* Right: Language Switcher, Glossary, Theme, Progress */}
          <div className="flex items-center gap-2 sm:gap-3">
            {/* Global Language Mode Switcher */}
            <div className="flex items-center bg-industrial-100 dark:bg-industrial-800 p-0.5 rounded-lg border border-industrial-200 dark:border-industrial-700 text-xs font-mono">
              <button
                onClick={() => setLangMode(LANGUAGE_MODES.EN_TOGGLE)}
                className={`px-2 py-1 rounded transition text-[11px] ${
                  langMode === LANGUAGE_MODES.EN_TOGGLE
                    ? 'bg-amber-500 text-industrial-950 font-bold shadow-sm'
                    : 'text-industrial-600 dark:text-industrial-300 hover:text-industrial-900 dark:hover:text-white'
                }`}
                title="Simple English primary with 1-click Polish accordion toggle"
              >
                EN + [PL]
              </button>
              <button
                onClick={() => setLangMode(LANGUAGE_MODES.SIDE_BY_SIDE)}
                className={`px-2 py-1 rounded transition text-[11px] hidden sm:block ${
                  langMode === LANGUAGE_MODES.SIDE_BY_SIDE
                    ? 'bg-amber-500 text-industrial-950 font-bold shadow-sm'
                    : 'text-industrial-600 dark:text-industrial-300 hover:text-industrial-900 dark:hover:text-white'
                }`}
                title="Dual column side-by-side English & Polish"
              >
                Side-by-Side
              </button>
              <button
                onClick={() => setLangMode(LANGUAGE_MODES.PL_FOCUS)}
                className={`px-2 py-1 rounded transition text-[11px] ${
                  langMode === LANGUAGE_MODES.PL_FOCUS
                    ? 'bg-amber-500 text-industrial-950 font-bold shadow-sm'
                    : 'text-industrial-600 dark:text-industrial-300 hover:text-industrial-900 dark:hover:text-white'
                }`}
                title="Polish primary focus with English toggle"
              >
                PL Focus
              </button>
            </div>

            {/* Glossary Button */}
            <button
              onClick={() => setIsGlossaryOpen(true)}
              className="inline-flex items-center gap-1.5 px-2.5 py-1.5 rounded-lg text-xs font-mono bg-industrial-100 hover:bg-industrial-200 dark:bg-industrial-800 dark:hover:bg-industrial-750 text-industrial-700 dark:text-industrial-300 border border-industrial-200 dark:border-industrial-700 transition"
              title="Open 90-Term Bilingual ML Glossary"
            >
              <BookOpen size={14} className="text-amber-500" />
              <span className="hidden md:inline">Glossary</span>
              <span className="text-[10px] opacity-70">90</span>
            </button>

            {/* Dark / Light Theme Toggle */}
            <button
              onClick={toggleTheme}
              className="p-2 rounded-lg text-industrial-600 dark:text-industrial-400 hover:bg-industrial-100 dark:hover:bg-industrial-800 transition border border-transparent hover:border-industrial-300 dark:hover:border-industrial-700"
              aria-label="Toggle Theme"
              title={`Switch to ${theme === 'dark' ? 'light' : 'dark'} mode`}
            >
              {theme === 'dark' ? <Sun size={17} className="text-amber-400" /> : <Moon size={17} />}
            </button>

            {/* Progress Badge */}
            <div className="hidden lg:flex items-center gap-2 pl-2 border-l border-industrial-200 dark:border-industrial-800 text-xs font-mono">
              <div className="w-16 h-2 bg-industrial-200 dark:bg-industrial-800 rounded-full overflow-hidden">
                <div
                  className="h-full bg-emerald-500 transition-all duration-300 rounded-full"
                  style={{ width: `${progressPercent}%` }}
                />
              </div>
              <span className="text-emerald-600 dark:text-emerald-400 font-bold">
                {completedCount}/{totalLessons} ({progressPercent}%)
              </span>
            </div>
          </div>
        </div>
      </header>

      {/* Main App Body (Sidebar + Content) */}
      <div className="flex-1 flex max-w-7xl w-full mx-auto">
        {/* Mobile Sidebar Backdrop */}
        {isSidebarOpen && (
          <div
            className="fixed inset-0 z-30 bg-black/60 backdrop-blur-xs lg:hidden"
            onClick={() => setIsSidebarOpen(false)}
          />
        )}

        {/* 7-Module Sidebar Navigation */}
        <aside
          className={`fixed lg:sticky top-16 z-30 h-[calc(100vh-4rem)] w-80 sm:w-88 shrink-0 bg-white dark:bg-industrial-900 border-r border-industrial-200 dark:border-industrial-800 flex flex-col transition-transform duration-200 ease-in-out lg:translate-x-0 ${
            isSidebarOpen ? 'translate-x-0 shadow-2xl' : '-translate-x-full'
          }`}
        >
          {/* Sidebar Search Bar */}
          <div className="p-3.5 border-b border-industrial-200 dark:border-industrial-800 bg-industrial-50/50 dark:bg-industrial-950/50">
            <div className="relative">
              <Search size={14} className="absolute left-3 top-1/2 -translate-y-1/2 text-industrial-400" />
              <input
                type="text"
                placeholder="Search 28 lessons..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="w-full pl-8 pr-3 py-1.5 bg-white dark:bg-industrial-850 border border-industrial-200 dark:border-industrial-700/80 rounded-lg text-xs font-mono text-industrial-900 dark:text-white placeholder:text-industrial-400 focus:outline-none focus:border-amber-500"
              />
            </div>
          </div>

          {/* Module List Scroll Area */}
          <div className="flex-1 overflow-y-auto p-3 space-y-2.5">
            {filteredModules.map((module) => {
              const IconComponent = MODULE_ICONS[module.number] || Activity;
              const isExpanded = expandedModules.includes(module.number);
              const moduleCompletedCount = module.lessons.filter(l => isLessonCompleted(l.id)).length;
              const isModuleComplete = moduleCompletedCount === module.lessons.length && module.lessons.length > 0;

              return (
                <div
                  key={module.id}
                  className="rounded-xl border border-industrial-200 dark:border-industrial-800 bg-industrial-50/40 dark:bg-industrial-850/30 overflow-hidden"
                >
                  {/* Module Header Button */}
                  <button
                    onClick={() => toggleModuleAccordion(module.number)}
                    className="w-full text-left p-3 flex items-center justify-between gap-2.5 hover:bg-industrial-100/60 dark:hover:bg-industrial-800/60 transition cursor-pointer select-none"
                  >
                    <div className="flex items-center gap-2.5 min-w-0">
                      <div className={`p-1.5 rounded-lg shrink-0 ${
                        isModuleComplete
                          ? 'bg-emerald-500/20 text-emerald-500'
                          : 'bg-amber-500/10 text-amber-500'
                      }`}>
                        <IconComponent size={16} />
                      </div>
                      <div className="truncate">
                        <div className="flex items-center gap-1.5 text-[10px] font-mono font-bold text-amber-600 dark:text-amber-400 uppercase tracking-wider">
                          <span>MOD-0{module.number}</span>
                          <span className="text-industrial-400 dark:text-industrial-500">·</span>
                          <span className={isModuleComplete ? 'text-emerald-500' : 'text-industrial-500 dark:text-industrial-400'}>
                            {moduleCompletedCount}/{module.lessons.length}
                          </span>
                        </div>
                        <h3 className="text-xs font-bold text-industrial-900 dark:text-white truncate">
                          {module.titleEn}
                        </h3>
                      </div>
                    </div>

                    <div className="text-industrial-400 shrink-0">
                      {isExpanded ? <ChevronDown size={15} /> : <ChevronRight size={15} />}
                    </div>
                  </button>

                  {/* Lessons List Accordion */}
                  {isExpanded && (
                    <div className="border-t border-industrial-200/60 dark:border-industrial-800/80 p-1.5 space-y-1 bg-white/50 dark:bg-industrial-900/40">
                      {module.lessons.map((lesson) => {
                        const isActive = activeLesson?.id === lesson.id;
                        const isDone = isLessonCompleted(lesson.id);

                        return (
                          <button
                            key={lesson.id}
                            onClick={() => {
                              onSelectLesson(lesson);
                              setIsSidebarOpen(false);
                            }}
                            className={`w-full text-left p-2 rounded-lg text-xs font-sans transition flex items-start gap-2.5 cursor-pointer ${
                              isActive
                                ? 'bg-amber-500/15 border border-amber-500/50 text-amber-950 dark:text-amber-200 font-semibold'
                                : 'text-industrial-700 dark:text-industrial-300 hover:bg-industrial-100 dark:hover:bg-industrial-800/80'
                            }`}
                          >
                            <span className="mt-0.5 shrink-0">
                              {isDone ? (
                                <CheckCircle2 size={14} className="text-emerald-500" />
                              ) : (
                                <Circle size={14} className="text-industrial-400 dark:text-industrial-600" />
                              )}
                            </span>

                            <div className="flex-1 min-w-0">
                              <div className="flex items-center gap-1.5">
                                <span className="font-mono text-[10px] text-industrial-500 dark:text-industrial-400">
                                  {lesson.id}
                                </span>
                                <span className="truncate">{lesson.titleEn}</span>
                              </div>
                              {lesson.titlePl && (
                                <div className="text-[10px] text-industrial-500 dark:text-industrial-400 truncate mt-0.5">
                                  🇵🇱 {lesson.titlePl}
                                </div>
                              )}
                            </div>
                          </button>
                        );
                      })}
                    </div>
                  )}
                </div>
              );
            })}
          </div>

          {/* Sidebar Footer telemetry */}
          <div className="p-3 border-t border-industrial-200 dark:border-industrial-800 bg-industrial-100/40 dark:bg-industrial-950/40 text-[10px] font-mono text-industrial-500 flex items-center justify-between">
            <span className="flex items-center gap-1 text-emerald-500 font-semibold">
              <span className="w-1.5 h-1.5 rounded-full bg-emerald-500 animate-pulse"></span>
              TELEMETRY: ONLINE
            </span>
            <span>VITE 5.4 · REACT 18</span>
          </div>
        </aside>

        {/* Main Content Area */}
        <main className="flex-1 min-w-0 overflow-y-auto">
          {children}
        </main>
      </div>

      {/* 90-Term Bilingual Glossary Modal */}
      <GlossaryModal
        isOpen={isGlossaryOpen}
        onClose={() => setIsGlossaryOpen(false)}
      />
    </div>
  );
};

export default Layout;
