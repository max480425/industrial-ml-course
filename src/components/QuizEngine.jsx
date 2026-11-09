import React, { useState } from 'react';
import { useProgress } from '../context/ProgressContext';
import { useLanguage, LANGUAGE_MODES } from '../context/LanguageContext';
import confetti from 'canvas-confetti';
import { HelpCircle, CheckCircle2, XCircle, RotateCcw, Award, Check } from 'lucide-react';

export const QuizEngine = ({ lesson }) => {
  const { markLessonCompleted, isLessonCompleted } = useProgress();
  const { langMode } = useLanguage();

  const quiz = lesson?.quiz || [];
  const [userAnswers, setUserAnswers] = useState({});
  const [isSubmitted, setIsSubmitted] = useState(false);

  if (!quiz || quiz.length === 0) return null;

  const handleSelectOption = (qIndex, optionIndex) => {
    if (isSubmitted) return;
    setUserAnswers(prev => ({
      ...prev,
      [qIndex]: optionIndex,
    }));
  };

  const calculateScore = () => {
    let correct = 0;
    quiz.forEach((q, idx) => {
      if (userAnswers[idx] === q.correctIndex) {
        correct++;
      }
    });
    return {
      correct,
      total: quiz.length,
      pct: Math.round((correct / quiz.length) * 100),
    };
  };

  const handleSubmit = () => {
    setIsSubmitted(true);
    const score = calculateScore();
    if (score.pct >= 75) {
      try {
        confetti({
          particleCount: 80,
          spread: 60,
          origin: { y: 0.7 },
        });
      } catch (e) {
        // ignore in non-browser envs
      }
    }
  };

  const handleReset = () => {
    setUserAnswers({});
    setIsSubmitted(false);
  };

  const score = isSubmitted ? calculateScore() : null;
  const isAllAnswered = Object.keys(userAnswers).length === quiz.length;
  const isPassed = score && score.pct >= 75;
  const isCompleted = isLessonCompleted(lesson.id);

  return (
    <div className="my-8 rounded-xl border border-industrial-200 dark:border-industrial-800 bg-white dark:bg-industrial-900 shadow-md p-5 sm:p-6 font-sans">
      {/* Header */}
      <div className="flex flex-wrap items-center justify-between gap-3 pb-4 mb-5 border-b border-industrial-200 dark:border-industrial-800">
        <div>
          <div className="flex items-center gap-2 mb-1">
            <span className="px-2 py-0.5 text-[10px] font-mono uppercase tracking-wider bg-emerald-500/15 text-emerald-700 dark:text-emerald-400 border border-emerald-500/30 rounded font-semibold">
              KNOWLEDGE CHECK
            </span>
            <span className="text-xs font-mono text-industrial-500 dark:text-industrial-400">
              {quiz.length} Questions
            </span>
          </div>
          <h3 className="text-base font-bold text-industrial-900 dark:text-white flex items-center gap-2">
            <HelpCircle size={18} className="text-emerald-500" />
            <span>Interactive Industrial ML Mastery Quiz</span>
          </h3>
        </div>

        {score && (
          <div className="flex items-center gap-3">
            <div className={`px-3 py-1.5 rounded-lg border font-mono text-xs flex items-center gap-2 ${
              isPassed
                ? 'bg-emerald-500/15 border-emerald-500/50 text-emerald-400 font-bold'
                : 'bg-rose-500/15 border-rose-500/50 text-rose-400 font-bold'
            }`}>
              <Award size={15} />
              <span>Score: {score.correct} / {score.total} ({score.pct}%)</span>
            </div>

            <button
              onClick={handleReset}
              className="p-1.5 text-industrial-400 hover:text-white rounded hover:bg-industrial-800 transition"
              title="Retake Quiz"
            >
              <RotateCcw size={16} />
            </button>
          </div>
        )}
      </div>

      {/* Quiz Questions List */}
      <div className="space-y-6">
        {quiz.map((q, qIdx) => {
          const selectedOption = userAnswers[qIdx];
          const isAnswered = selectedOption !== undefined;
          const isCorrect = isSubmitted && selectedOption === q.correctIndex;
          const isWrong = isSubmitted && isAnswered && selectedOption !== q.correctIndex;

          const questionText = langMode === LANGUAGE_MODES.PL_FOCUS ? (q.questionPl || q.questionEn) : q.questionEn;
          const optionsList = langMode === LANGUAGE_MODES.PL_FOCUS && q.optionsPl ? q.optionsPl : q.optionsEn;

          return (
            <div
              key={q.id || qIdx}
              className={`p-4 rounded-lg border transition ${
                isSubmitted
                  ? isCorrect
                    ? 'border-emerald-500/40 bg-emerald-500/5 dark:bg-emerald-950/20'
                    : 'border-rose-500/40 bg-rose-500/5 dark:bg-rose-950/20'
                  : 'border-industrial-200 dark:border-industrial-800 bg-industrial-50/50 dark:bg-industrial-850/40'
              }`}
            >
              {/* Question Title */}
              <div className="flex items-start gap-2.5 mb-3">
                <span className="font-mono text-xs font-bold px-2 py-0.5 rounded bg-industrial-200 dark:bg-industrial-800 text-industrial-700 dark:text-industrial-300">
                  Q{qIdx + 1}
                </span>
                <div className="flex-1">
                  <h4 className="text-sm font-semibold text-industrial-900 dark:text-white leading-relaxed">
                    {questionText}
                  </h4>
                  {langMode !== LANGUAGE_MODES.PL_FOCUS && q.questionPl && (
                    <p className="text-xs text-industrial-500 dark:text-industrial-400 mt-0.5">
                      🇵🇱 {q.questionPl}
                    </p>
                  )}
                </div>
              </div>

              {/* Options */}
              <div className="space-y-2 mt-3 pl-8">
                {optionsList.map((optText, optIdx) => {
                  const isThisSelected = selectedOption === optIdx;
                  let optStyle = 'border-industrial-200 dark:border-industrial-800 hover:border-industrial-300 dark:hover:border-industrial-700 bg-white dark:bg-industrial-900';

                  if (isSubmitted) {
                    if (optIdx === q.correctIndex) {
                      optStyle = 'border-emerald-500 bg-emerald-500/15 text-emerald-800 dark:text-emerald-200 font-medium';
                    } else if (isThisSelected) {
                      optStyle = 'border-rose-500 bg-rose-500/15 text-rose-800 dark:text-rose-200 line-through';
                    } else {
                      optStyle = 'opacity-50 border-industrial-200 dark:border-industrial-800';
                    }
                  } else if (isThisSelected) {
                    optStyle = 'border-amber-500 bg-amber-500/10 text-amber-700 dark:text-amber-300 font-medium';
                  }

                  return (
                    <button
                      key={optIdx}
                      type="button"
                      disabled={isSubmitted}
                      onClick={() => handleSelectOption(qIdx, optIdx)}
                      className={`w-full text-left p-2.5 rounded-lg border text-xs leading-relaxed transition flex items-center justify-between cursor-pointer ${optStyle}`}
                    >
                      <span>{optText}</span>
                      {isSubmitted && optIdx === q.correctIndex && (
                        <CheckCircle2 size={15} className="text-emerald-500 shrink-0 ml-2" />
                      )}
                      {isSubmitted && isThisSelected && optIdx !== q.correctIndex && (
                        <XCircle size={15} className="text-rose-500 shrink-0 ml-2" />
                      )}
                    </button>
                  );
                })}
              </div>

              {/* Feedback Explanation */}
              {isSubmitted && (
                <div className="mt-3.5 pt-3 border-t border-dashed border-industrial-200 dark:border-industrial-800 text-xs text-industrial-600 dark:text-industrial-300 pl-8 leading-relaxed">
                  <div className="font-mono text-[10px] uppercase font-bold text-emerald-600 dark:text-emerald-400 mb-0.5">
                    Engineering Rationale:
                  </div>
                  <div>
                    {langMode === LANGUAGE_MODES.PL_FOCUS
                      ? (q.explanationPl || q.explanationEn)
                      : q.explanationEn}
                  </div>
                  {langMode !== LANGUAGE_MODES.PL_FOCUS && q.explanationPl && (
                    <div className="text-[11px] text-industrial-500 dark:text-industrial-400 mt-1">
                      🇵🇱 {q.explanationPl}
                    </div>
                  )}
                </div>
              )}
            </div>
          );
        })}
      </div>

      {/* Footer Controls */}
      <div className="mt-6 pt-4 border-t border-industrial-200 dark:border-industrial-800 flex flex-wrap items-center justify-between gap-3">
        {!isSubmitted ? (
          <button
            onClick={handleSubmit}
            disabled={!isAllAnswered}
            className={`px-5 py-2.5 rounded-lg text-xs font-mono font-bold transition shadow-md ${
              isAllAnswered
                ? 'bg-amber-500 hover:bg-amber-400 text-industrial-950 cursor-pointer shadow-amber-500/20'
                : 'bg-industrial-200 dark:bg-industrial-800 text-industrial-400 dark:text-industrial-500 cursor-not-allowed'
            }`}
          >
            {isAllAnswered ? 'Submit Quiz Answers' : `Answer all questions (${Object.keys(userAnswers).length}/${quiz.length})`}
          </button>
        ) : (
          <div className="flex flex-wrap items-center gap-3 w-full justify-between">
            <button
              onClick={handleReset}
              className="inline-flex items-center gap-1.5 px-4 py-2 text-xs font-mono bg-industrial-200 dark:bg-industrial-800 hover:bg-industrial-300 dark:hover:bg-industrial-700 text-industrial-700 dark:text-industrial-200 rounded-lg transition"
            >
              <RotateCcw size={13} />
              <span>Retry Quiz</span>
            </button>

            {isPassed && (
              <button
                onClick={() => markLessonCompleted(lesson.id)}
                className={`inline-flex items-center gap-2 px-5 py-2.5 rounded-lg text-xs font-mono font-bold transition shadow-md ${
                  isCompleted
                    ? 'bg-emerald-600/20 text-emerald-400 border border-emerald-500/40'
                    : 'bg-emerald-500 hover:bg-emerald-400 text-industrial-950 shadow-emerald-500/20'
                }`}
              >
                <Check size={16} />
                <span>{isCompleted ? '✓ Lesson Marked as Complete' : 'Mark Lesson as Completed (Passed)'}</span>
              </button>
            )}
          </div>
        )}
      </div>
    </div>
  );
};

export default QuizEngine;
