import React, { useState, useRef, useEffect } from 'react';
import glossaryData from '../data/glossary.json';
import { BookOpen, X, ExternalLink, Factory } from 'lucide-react';

const glossaryMap = glossaryData.reduce((acc, item) => {
  acc[item.id] = item;
  return acc;
}, {});

export const TermTooltip = ({ termId, children }) => {
  const term = glossaryMap[termId];
  const [isOpen, setIsOpen] = useState(false);
  const [coords, setCoords] = useState({ top: 0, left: 0 });
  const triggerRef = useRef(null);
  const popupRef = useRef(null);

  useEffect(() => {
    const handleClickOutside = (event) => {
      if (
        popupRef.current &&
        !popupRef.current.contains(event.target) &&
        triggerRef.current &&
        !triggerRef.current.contains(event.target)
      ) {
        setIsOpen(false);
      }
    };

    if (isOpen) {
      document.addEventListener('mousedown', handleClickOutside);
    }
    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
    };
  }, [isOpen]);

  const handleToggle = (e) => {
    e.preventDefault();
    e.stopPropagation();
    if (!isOpen && triggerRef.current) {
      const rect = triggerRef.current.getBoundingClientRect();
      const popupWidth = 340;
      let left = rect.left + window.scrollX;
      // Prevent offscreen overflow
      if (left + popupWidth > window.innerWidth - 20) {
        left = window.innerWidth - popupWidth - 20;
      }
      if (left < 10) left = 10;
      setCoords({
        top: rect.bottom + window.scrollY + 6,
        left,
      });
    }
    setIsOpen(!isOpen);
  };

  if (!term) {
    return <span className="underline decoration-amber-500/50">{children || termId}</span>;
  }

  return (
    <span className="relative inline-block">
      <button
        ref={triggerRef}
        onClick={handleToggle}
        className="inline-flex items-center gap-0.5 px-1 py-0.5 mx-0.5 text-inherit font-medium border-b-2 border-dashed border-amber-500/80 hover:border-amber-400 hover:bg-amber-500/10 dark:hover:bg-amber-400/15 rounded transition-all cursor-pointer group text-left"
        title={`Click for engineering definition: ${term.termEn} (${term.termPl})`}
      >
        <span>{children || term.termEn}</span>
        <span className="text-[10px] font-mono text-amber-600 dark:text-amber-400 opacity-70 group-hover:opacity-100">ⓘ</span>
      </button>

      {isOpen && (
        <div
          ref={popupRef}
          style={{
            position: 'fixed',
            top: `${Math.min(coords.top, window.innerHeight - 300)}px`,
            left: `${coords.left}px`,
            zIndex: 9999,
          }}
          className="w-80 sm:w-96 max-w-[92vw] bg-industrial-900 border border-amber-500/40 text-industrial-100 shadow-2xl rounded-lg p-4 font-sans text-xs animate-in fade-in zoom-in-95 duration-150 backdrop-blur-md"
        >
          {/* Header */}
          <div className="flex items-start justify-between gap-2 pb-2 mb-2.5 border-b border-industrial-700/80">
            <div>
              <div className="flex items-center gap-1.5 mb-1">
                <span className="px-1.5 py-0.5 text-[9px] font-mono uppercase tracking-wider bg-amber-500/20 text-amber-400 border border-amber-500/30 rounded">
                  {term.category}
                </span>
                <span className="text-[10px] font-mono text-industrial-400">ID: {term.id}</span>
              </div>
              <h4 className="text-sm font-bold text-white flex items-center gap-1.5">
                <span>{term.termEn}</span>
              </h4>
              <p className="text-xs font-medium text-amber-300/90 mt-0.5">
                🇵🇱 {term.termPl}
              </p>
            </div>
            <button
              onClick={() => setIsOpen(false)}
              className="text-industrial-400 hover:text-white p-1 rounded hover:bg-industrial-800 transition"
              aria-label="Close"
            >
              <X size={14} />
            </button>
          </div>

          {/* Definitions */}
          <div className="space-y-2.5">
            <div>
              <div className="text-[10px] font-mono text-industrial-400 uppercase tracking-wider mb-0.5">
                Simple English:
              </div>
              <p className="text-industrial-200 leading-relaxed">{term.defEn}</p>
            </div>

            <div className="bg-industrial-850/80 p-2.5 rounded border border-industrial-800">
              <div className="text-[10px] font-mono text-amber-400 uppercase tracking-wider mb-0.5 flex items-center gap-1">
                <span>🇵🇱 Polski Kontekst Inżynierski:</span>
              </div>
              <p className="text-industrial-300 leading-relaxed">{term.defPl}</p>
            </div>

            {/* Industrial Context */}
            <div className="bg-amber-950/20 border-l-2 border-amber-500 p-2 rounded-r">
              <div className="flex items-center gap-1 text-[10px] font-mono text-amber-400 mb-0.5 font-semibold">
                <Factory size={11} />
                <span>REAL FACTORY / SCADA APPLICATION</span>
              </div>
              <p className="text-[11px] text-industrial-300">
                <span className="text-white font-medium">EN:</span> {term.contextEn}
              </p>
              <p className="text-[11px] text-industrial-400 mt-1">
                <span className="text-amber-300/80 font-medium">PL:</span> {term.contextPl}
              </p>
            </div>
          </div>
        </div>
      )}
    </span>
  );
};

export default TermTooltip;
