import React, { useState } from 'react';
import glossaryData from '../data/glossary.json';
import { useLanguage, LANGUAGE_MODES } from '../context/LanguageContext';
import { BookOpen, Search, X, Tag, Factory } from 'lucide-react';

export const GlossaryModal = ({ isOpen, onClose }) => {
  const [search, setSearch] = useState('');
  const [selectedCategory, setSelectedCategory] = useState('All');
  const { langMode } = useLanguage();

  if (!isOpen) return null;

  const categories = ['All', ...new Set(glossaryData.map(item => item.category))];

  const filteredTerms = glossaryData.filter(item => {
    const matchesCat = selectedCategory === 'All' || item.category === selectedCategory;
    const query = search.toLowerCase();
    const matchesSearch =
      item.termEn.toLowerCase().includes(query) ||
      item.termPl.toLowerCase().includes(query) ||
      item.id.toLowerCase().includes(query) ||
      item.defEn.toLowerCase().includes(query) ||
      item.defPl.toLowerCase().includes(query);
    return matchesCat && matchesSearch;
  });

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/70 backdrop-blur-sm animate-in fade-in duration-200">
      <div className="bg-white dark:bg-industrial-900 border border-industrial-300 dark:border-industrial-700 w-full max-w-4xl max-h-[88vh] rounded-2xl shadow-2xl flex flex-col overflow-hidden font-sans">
        {/* Header */}
        <div className="p-5 border-b border-industrial-200 dark:border-industrial-800 bg-industrial-50 dark:bg-industrial-950 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="p-2 bg-amber-500/10 text-amber-500 rounded-lg border border-amber-500/20">
              <BookOpen size={20} />
            </div>
            <div>
              <h2 className="text-lg font-bold text-industrial-900 dark:text-white">
                Industrial ML & Data Science Bilingual Glossary
              </h2>
              <p className="text-xs text-industrial-500 dark:text-industrial-400">
                {glossaryData.length} core engineering terms in Simple English & Polish with factory SCADA examples.
              </p>
            </div>
          </div>

          <button
            onClick={onClose}
            className="p-1.5 text-industrial-400 hover:text-industrial-900 dark:hover:text-white rounded-lg hover:bg-industrial-200 dark:hover:bg-industrial-800 transition"
          >
            <X size={20} />
          </button>
        </div>

        {/* Search & Categories Bar */}
        <div className="p-4 border-b border-industrial-200 dark:border-industrial-800 bg-white dark:bg-industrial-900 space-y-3">
          <div className="relative">
            <Search size={16} className="absolute left-3 top-1/2 -translate-y-1/2 text-industrial-400" />
            <input
              type="text"
              placeholder="Search terms by English, Polish, keyword, or concept..."
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              className="w-full pl-9 pr-4 py-2 bg-industrial-100 dark:bg-industrial-800 border border-industrial-300 dark:border-industrial-700 rounded-lg text-xs font-mono text-industrial-900 dark:text-white placeholder:text-industrial-400 focus:outline-none focus:border-amber-500"
            />
          </div>

          <div className="flex items-center gap-1.5 overflow-x-auto pb-1 text-xs font-mono">
            {categories.map((cat) => (
              <button
                key={cat}
                onClick={() => setSelectedCategory(cat)}
                className={`px-2.5 py-1 rounded-md transition whitespace-nowrap ${
                  selectedCategory === cat
                    ? 'bg-amber-500 text-industrial-950 font-bold'
                    : 'bg-industrial-100 dark:bg-industrial-800 text-industrial-600 dark:text-industrial-400 hover:bg-industrial-200 dark:hover:bg-industrial-700'
                }`}
              >
                {cat}
              </button>
            ))}
          </div>
        </div>

        {/* Terms Grid */}
        <div className="p-5 overflow-y-auto flex-1 space-y-4">
          {filteredTerms.length === 0 ? (
            <div className="text-center py-12 text-industrial-400 font-mono text-xs">
              No matching terms found. Try a different search query.
            </div>
          ) : (
            filteredTerms.map((item) => (
              <div
                key={item.id}
                className="p-4 rounded-xl border border-industrial-200 dark:border-industrial-800 bg-industrial-50/50 dark:bg-industrial-850/50 hover:border-amber-500/40 transition"
              >
                <div className="flex flex-wrap items-start justify-between gap-2 pb-2 mb-2 border-b border-industrial-200/60 dark:border-industrial-800">
                  <div>
                    <span className="text-[10px] font-mono uppercase tracking-wider text-amber-600 dark:text-amber-400 bg-amber-500/10 px-2 py-0.5 rounded border border-amber-500/20 mr-2">
                      {item.category}
                    </span>
                    <span className="text-xs font-mono text-industrial-400">ID: {item.id}</span>
                    <h3 className="text-sm font-bold text-industrial-900 dark:text-white mt-1">
                      {item.termEn}
                    </h3>
                    <p className="text-xs font-medium text-emerald-600 dark:text-emerald-400 mt-0.5">
                      🇵🇱 {item.termPl}
                    </p>
                  </div>
                </div>

                <div className="space-y-2 text-xs leading-relaxed">
                  <div>
                    <span className="font-mono text-[10px] uppercase text-industrial-400 font-bold">Simple English: </span>
                    <span className="text-industrial-700 dark:text-industrial-200">{item.defEn}</span>
                  </div>

                  <div className="p-2.5 bg-industrial-100 dark:bg-industrial-900 rounded border border-industrial-200 dark:border-industrial-800">
                    <span className="font-mono text-[10px] uppercase text-emerald-600 dark:text-emerald-400 font-bold">🇵🇱 Definicja Techniczna: </span>
                    <span className="text-industrial-800 dark:text-industrial-300">{item.defPl}</span>
                  </div>

                  {item.contextEn && (
                    <div className="p-2 bg-amber-500/5 dark:bg-amber-950/20 border-l-2 border-amber-500 rounded-r text-[11px]">
                      <div className="flex items-center gap-1 font-mono text-[10px] text-amber-600 dark:text-amber-400 font-bold mb-0.5">
                        <Factory size={11} />
                        <span>FACTORY APPLICATION:</span>
                      </div>
                      <div className="text-industrial-700 dark:text-industrial-300">
                        <span className="font-medium">EN:</span> {item.contextEn}
                      </div>
                      <div className="text-industrial-600 dark:text-industrial-400 mt-0.5">
                        <span className="font-medium text-amber-500">PL:</span> {item.contextPl}
                      </div>
                    </div>
                  )}
                </div>
              </div>
            ))
          )}
        </div>

        {/* Footer */}
        <div className="p-3 border-t border-industrial-200 dark:border-industrial-800 bg-industrial-100/60 dark:bg-industrial-950 text-right text-xs font-mono text-industrial-500">
          Showing {filteredTerms.length} of {glossaryData.length} terms
        </div>
      </div>
    </div>
  );
};

export default GlossaryModal;
