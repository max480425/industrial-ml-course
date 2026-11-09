import React from 'react';
import CONFIG from '../config';
import { useProgress } from '../context/ProgressContext';
import { useLanguage, LANGUAGE_MODES } from '../context/LanguageContext';
import { ExternalLink, Download, CheckSquare, Square, Clock, Terminal, CheckCircle2 } from 'lucide-react';

export const ColabLauncher = ({ lesson }) => {
  const { isTaskChecked, toggleTaskCheck } = useProgress();
  const { langMode } = useLanguage();

  if (!lesson) return null;

  const notebookFile = lesson.notebook || lesson.colab_notebook || '';
  const colabUrl = CONFIG.getColabUrl(notebookFile);
  const downloadUrl = CONFIG.getNotebookDownloadUrl(notebookFile);
  const checklist = lesson.checklist || [];

  const completedCount = checklist.filter(task => isTaskChecked(lesson.id, task.id)).length;
  const progressPct = checklist.length > 0 ? Math.round((completedCount / checklist.length) * 100) : 0;

  return (
    <div className="my-6 rounded-xl border border-industrial-200 dark:border-industrial-800 bg-white dark:bg-industrial-900 shadow-md overflow-hidden font-sans">
      {/* Top Header Card */}
      <div className="p-5 bg-gradient-to-r from-industrial-100 to-industrial-50 dark:from-industrial-850 dark:to-industrial-900 border-b border-industrial-200 dark:border-industrial-800">
        <div className="flex flex-wrap items-center justify-between gap-4">
          <div>
            <div className="flex items-center gap-2 mb-1">
              <span className="px-2 py-0.5 text-[10px] font-mono uppercase tracking-wider bg-amber-500/15 text-amber-700 dark:text-amber-400 border border-amber-500/30 rounded font-semibold">
                PRACTICAL COLAB LAB
              </span>
              <span className="flex items-center gap-1 text-xs text-industrial-500 dark:text-industrial-400 font-mono">
                <Clock size={12} />
                <span>{lesson.estimatedMinutes || 20} min</span>
              </span>
            </div>
            <h3 className="text-base font-bold text-industrial-900 dark:text-white flex items-center gap-2">
              <Terminal size={17} className="text-amber-500" />
              <span>{lesson.notebook}</span>
            </h3>
            <p className="text-xs text-industrial-600 dark:text-industrial-400 mt-0.5">
              Self-contained interactive Jupyter notebook with pre-loaded industrial dataset pipelines.
            </p>
          </div>

          {/* Action Buttons */}
          <div className="flex items-center gap-2.5">
            <a
              href={downloadUrl}
              download
              className="inline-flex items-center gap-1.5 px-3 py-2 text-xs font-mono font-medium text-industrial-700 dark:text-industrial-300 bg-industrial-200/80 hover:bg-industrial-300 dark:bg-industrial-800 dark:hover:bg-industrial-750 border border-industrial-300 dark:border-industrial-700 rounded-lg transition shadow-sm"
              title="Download raw .ipynb notebook file"
            >
              <Download size={14} />
              <span>Download .ipynb</span>
            </a>

            <a
              href={colabUrl}
              target="_blank"
              rel="noopener noreferrer"
              className="inline-flex items-center gap-2 px-4 py-2 text-xs font-mono font-bold text-industrial-950 bg-gradient-to-r from-amber-400 to-amber-500 hover:from-amber-300 hover:to-amber-400 rounded-lg transition shadow-md shadow-amber-500/20 group"
            >
              {/* Google Colab SVG icon */}
              <svg className="w-4 h-4 transition-transform group-hover:scale-110" viewBox="0 0 24 24" fill="currentColor">
                <path d="M12 0C5.37 0 0 5.37 0 12c0 5.31 3.435 9.795 8.205 11.385.6.105.825-.255.825-.57 0-.285-.015-1.23-.015-2.235-3.015.555-3.795-.735-4.035-1.41-.135-.345-.72-1.41-1.23-1.695-.42-.225-1.02-.78-.015-.795.945-.015 1.62.87 1.845 1.23 1.08 1.815 2.805 1.305 3.495.99.105-.78.42-1.305.765-1.605-2.67-.3-5.46-1.335-5.46-5.925 0-1.305.465-2.385 1.23-3.225-.12-.3-.54-1.53.12-3.18 0 0 1.005-.315 3.3 1.23.96-.27 1.98-.405 3-.405s2.04.135 3 .405c2.295-1.56 3.3-1.23 3.3-1.23.66 1.65.24 2.88.12 3.18.765.84 1.23 1.905 1.23 3.225 0 4.605-2.805 5.625-5.475 5.925.435.375.81 1.095.81 2.22 0 1.605-.015 2.895-.015 3.3 0 .315.225.69.825.57A12.02 12.02 0 0024 12c0-6.63-5.37-12-12-12z" />
              </svg>
              <span>Open in Google Colab</span>
              <ExternalLink size={13} className="opacity-80" />
            </a>
          </div>
        </div>

        {/* Runtime Spec Badges */}
        <div className="flex flex-wrap items-center gap-2 mt-3 pt-3 border-t border-industrial-200/60 dark:border-industrial-800/80 text-[11px] font-mono text-industrial-500 dark:text-industrial-400">
          <span className="bg-industrial-200/50 dark:bg-industrial-800 px-2 py-0.5 rounded">Python 3.10+</span>
          <span className="bg-industrial-200/50 dark:bg-industrial-800 px-2 py-0.5 rounded">Free Tier CPU / T4 GPU</span>
          <span className="bg-industrial-200/50 dark:bg-industrial-800 px-2 py-0.5 rounded">scikit-learn · scipy · pandas</span>
          <span className="ml-auto text-[10px] text-industrial-400">
            Repo: <code className="text-amber-600 dark:text-amber-400">{CONFIG.githubUser}/{CONFIG.githubRepo}</code>
          </span>
        </div>
      </div>

      {/* Interactive Hands-On Task Checklist */}
      <div className="p-5">
        <div className="flex items-center justify-between mb-3">
          <div className="flex items-center gap-2">
            <h4 className="text-xs font-bold uppercase tracking-wider font-mono text-industrial-800 dark:text-industrial-200">
              Interactive Notebook Checklist:
            </h4>
            <span className="text-xs font-mono px-2 py-0.5 rounded bg-emerald-500/10 text-emerald-600 dark:text-emerald-400 font-semibold border border-emerald-500/20">
              {completedCount} / {checklist.length} Completed ({progressPct}%)
            </span>
          </div>

          {progressPct === 100 && (
            <span className="flex items-center gap-1 text-xs font-mono text-emerald-600 dark:text-emerald-400 font-bold">
              <CheckCircle2 size={14} />
              <span>All Notebook Tasks Done!</span>
            </span>
          )}
        </div>

        {/* Progress bar */}
        <div className="w-full h-1.5 bg-industrial-100 dark:bg-industrial-800 rounded-full mb-4 overflow-hidden">
          <div
            className="h-full bg-emerald-500 transition-all duration-300 rounded-full"
            style={{ width: `${progressPct}%` }}
          />
        </div>

        {/* Task Items */}
        <div className="space-y-2.5">
          {checklist.map((task) => {
            const isChecked = isTaskChecked(lesson.id, task.id);
            return (
              <div
                key={task.id}
                onClick={() => toggleTaskCheck(lesson.id, task.id)}
                className={`p-3 rounded-lg border transition-all cursor-pointer flex items-start gap-3 select-none ${
                  isChecked
                    ? 'bg-emerald-500/5 dark:bg-emerald-950/20 border-emerald-500/40 text-industrial-800 dark:text-industrial-200'
                    : 'bg-industrial-50/70 dark:bg-industrial-850/40 border-industrial-200 dark:border-industrial-800/80 hover:border-industrial-300 dark:hover:border-industrial-700 text-industrial-700 dark:text-industrial-300'
                }`}
              >
                <button
                  type="button"
                  className="mt-0.5 text-emerald-500 dark:text-emerald-400 shrink-0 focus:outline-none"
                  aria-label={isChecked ? 'Uncheck task' : 'Check task'}
                >
                  {isChecked ? <CheckSquare size={17} /> : <Square size={17} />}
                </button>

                <div className="text-xs leading-relaxed flex-1">
                  <div className={`font-medium ${isChecked ? 'line-through opacity-80' : ''}`}>
                    {langMode === LANGUAGE_MODES.PL_FOCUS ? (task.textPl || task.textEn) : task.textEn}
                  </div>
                  {langMode !== LANGUAGE_MODES.PL_FOCUS && task.textPl && (
                    <div className="text-[11px] text-industrial-500 dark:text-industrial-400 mt-0.5">
                      🇵🇱 {task.textPl}
                    </div>
                  )}
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
};

export default ColabLauncher;
