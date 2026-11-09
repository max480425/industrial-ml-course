import React, { useState } from 'react';
import { useLanguage, LANGUAGE_MODES } from '../context/LanguageContext';
import TermTooltip from './TermTooltip';
import { ChevronDown, ChevronUp, Globe, Wrench, AlertTriangle, Lightbulb } from 'lucide-react';

/**
 * Parses text containing `{{term:id}}` or `{{term:id|Custom Label}}`
 * and replaces them with interactive TermTooltip components.
 */
export const parseTerms = (text) => {
  if (!text) return '';
  const regex = /\{\{term:([a-zA-Z0-9_-]+)(?:\|([^}]+))?\}\}/g;
  const parts = [];
  let lastIndex = 0;
  let match;

  while ((match = regex.exec(text)) !== null) {
    if (match.index > lastIndex) {
      parts.push(text.substring(lastIndex, match.index));
    }
    const termId = match[1];
    const customLabel = match[2];
    parts.push(
      <TermTooltip key={`term-${termId}-${match.index}`} termId={termId}>
        {customLabel}
      </TermTooltip>
    );
    lastIndex = regex.lastIndex;
  }

  if (lastIndex < text.length) {
    parts.push(text.substring(lastIndex));
  }

  return parts;
};

export const BilingualBlock = ({
  en,
  pl,
  titleEn,
  titlePl,
  type = 'paragraph',
  calloutType = 'info', // 'engineering', 'warning', 'info'
}) => {
  const { langMode } = useLanguage();
  const [isAccordionOpen, setIsAccordionOpen] = useState(false);

  const parsedEn = parseTerms(en);
  const parsedPl = parseTerms(pl);

  // Callout styling
  const isCallout = type === 'callout';
  const getCalloutBorder = () => {
    switch (calloutType) {
      case 'engineering':
        return 'border-l-4 border-amber-500 bg-amber-500/5 dark:bg-amber-950/20';
      case 'warning':
        return 'border-l-4 border-rose-500 bg-rose-500/5 dark:bg-rose-950/20';
      default:
        return 'border-l-4 border-cyan-500 bg-cyan-500/5 dark:bg-cyan-950/20';
    }
  };

  const getCalloutIcon = () => {
    switch (calloutType) {
      case 'engineering':
        return <Wrench size={16} className="text-amber-500 shrink-0" />;
      case 'warning':
        return <AlertTriangle size={16} className="text-rose-500 shrink-0" />;
      default:
        return <Lightbulb size={16} className="text-cyan-500 shrink-0" />;
    }
  };

  // 1. SIDE-BY-SIDE MODE
  if (langMode === LANGUAGE_MODES.SIDE_BY_SIDE) {
    return (
      <div className={`my-4 p-4 rounded-lg border border-industrial-200 dark:border-industrial-800 bg-white/70 dark:bg-industrial-900/60 shadow-sm ${isCallout ? getCalloutBorder() : ''}`}>
        {(titleEn || titlePl) && (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 pb-2 mb-3 border-b border-industrial-100 dark:border-industrial-800">
            <div className="flex items-center gap-2">
              {isCallout && getCalloutIcon()}
              <span className="text-xs font-mono font-semibold px-1.5 py-0.5 rounded bg-blue-500/10 text-blue-600 dark:text-blue-400 border border-blue-500/20">
                🇬🇧 EN
              </span>
              <h4 className="text-sm font-bold text-industrial-900 dark:text-white">{titleEn}</h4>
            </div>
            <div className="flex items-center gap-2">
              <span className="text-xs font-mono font-semibold px-1.5 py-0.5 rounded bg-emerald-500/10 text-emerald-600 dark:text-emerald-400 border border-emerald-500/20">
                🇵🇱 PL
              </span>
              <h4 className="text-sm font-bold text-industrial-800 dark:text-industrial-200">{titlePl || titleEn}</h4>
            </div>
          </div>
        )}

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div className="text-sm leading-relaxed text-industrial-800 dark:text-industrial-200">
            {parsedEn}
          </div>
          <div className="text-sm leading-relaxed text-industrial-700 dark:text-industrial-300 md:border-l md:border-industrial-200 dark:md:border-industrial-800 md:pl-6">
            {parsedPl}
          </div>
        </div>
      </div>
    );
  }

  // 2. PL FOCUS MODE
  if (langMode === LANGUAGE_MODES.PL_FOCUS) {
    return (
      <div className={`my-4 p-4 rounded-lg border border-industrial-200 dark:border-industrial-800 bg-white/70 dark:bg-industrial-900/60 shadow-sm ${isCallout ? getCalloutBorder() : ''}`}>
        {(titlePl || titleEn) && (
          <div className="flex items-center gap-2 mb-2 pb-2 border-b border-industrial-100 dark:border-industrial-800">
            {isCallout && getCalloutIcon()}
            <span className="text-xs font-mono font-semibold px-1.5 py-0.5 rounded bg-emerald-500/10 text-emerald-600 dark:text-emerald-400 border border-emerald-500/20">
              🇵🇱 PL
            </span>
            <h4 className="text-sm font-bold text-industrial-900 dark:text-white">{titlePl || titleEn}</h4>
          </div>
        )}

        <div className="text-sm leading-relaxed text-industrial-800 dark:text-industrial-200">
          {parsedPl}
        </div>

        {/* English Toggle Accordion */}
        <div className="mt-3 pt-2 border-t border-dashed border-industrial-200 dark:border-industrial-800">
          <button
            onClick={() => setIsAccordionOpen(!isAccordionOpen)}
            className="inline-flex items-center gap-1.5 text-xs font-mono text-industrial-600 dark:text-industrial-400 hover:text-industrial-900 dark:hover:text-amber-400 transition cursor-pointer py-1"
          >
            <Globe size={13} />
            <span>{isAccordionOpen ? '[ Hide English original ]' : '[ 🇬🇧 Show Simple English ]'}</span>
            {isAccordionOpen ? <ChevronUp size={13} /> : <ChevronDown size={13} />}
          </button>

          {isAccordionOpen && (
            <div className="mt-2 p-3 bg-industrial-100/70 dark:bg-industrial-950/70 rounded border border-industrial-200 dark:border-industrial-800/80 text-sm leading-relaxed text-industrial-700 dark:text-industrial-300 animate-in fade-in duration-150">
              <div className="text-[10px] font-mono text-blue-600 dark:text-blue-400 uppercase tracking-wider mb-1">
                Original Simple English:
              </div>
              {parsedEn}
            </div>
          )}
        </div>
      </div>
    );
  }

  // 3. DEFAULT: EN + [PL TOGGLE] MODE
  return (
    <div className={`my-4 p-4 rounded-lg border border-industrial-200 dark:border-industrial-800 bg-white/70 dark:bg-industrial-900/60 shadow-sm ${isCallout ? getCalloutBorder() : ''}`}>
      {titleEn && (
        <div className="flex items-center gap-2 mb-2 pb-2 border-b border-industrial-100 dark:border-industrial-800">
          {isCallout && getCalloutIcon()}
          <span className="text-xs font-mono font-semibold px-1.5 py-0.5 rounded bg-blue-500/10 text-blue-600 dark:text-blue-400 border border-blue-500/20">
            🇬🇧 EN
          </span>
          <h4 className="text-sm font-bold text-industrial-900 dark:text-white">{titleEn}</h4>
        </div>
      )}

      {/* English Primary Paragraph */}
      <div className="text-sm leading-relaxed text-industrial-800 dark:text-industrial-200">
        {parsedEn}
      </div>

      {/* 1-Click Polish Accordion Toggle */}
      <div className="mt-3 pt-2 border-t border-dashed border-industrial-200 dark:border-industrial-800">
        <button
          onClick={() => setIsAccordionOpen(!isAccordionOpen)}
          className="inline-flex items-center gap-1.5 text-xs font-mono font-medium text-amber-700 dark:text-amber-400/90 hover:text-amber-600 dark:hover:text-amber-300 transition cursor-pointer py-1 px-2 rounded bg-amber-500/5 hover:bg-amber-500/15 border border-amber-500/20"
        >
          <span>{isAccordionOpen ? '[ 🇵🇱 Ukryj tłumaczenie ]' : '[ 🇵🇱 Pokaż po polsku ]'}</span>
          {isAccordionOpen ? <ChevronUp size={13} /> : <ChevronDown size={13} />}
        </button>

        {isAccordionOpen && (
          <div className="mt-2.5 p-3.5 bg-industrial-50 dark:bg-industrial-950/80 rounded border-l-2 border-emerald-500 text-sm leading-relaxed text-industrial-800 dark:text-industrial-300 animate-in fade-in slide-in-from-top-1 duration-150">
            <div className="flex items-center justify-between mb-1.5">
              <span className="text-[10px] font-mono font-semibold text-emerald-600 dark:text-emerald-400 uppercase tracking-wider">
                🇵🇱 Polskie Tłumaczenie Techniczne
              </span>
              {titlePl && (
                <span className="text-xs font-bold text-industrial-900 dark:text-white">
                  {titlePl}
                </span>
              )}
            </div>
            <div>{parsedPl}</div>
          </div>
        )}
      </div>
    </div>
  );
};

export default BilingualBlock;
