'use client';

import { useState } from 'react';
import { Search } from 'lucide-react';

interface SearchBarProps {
  onSearch: (query: string) => void;
  isLoading: boolean;
}

export default function SearchBar({ onSearch, isLoading }: SearchBarProps) {
  const [query, setQuery] = useState('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (query.trim()) {
      onSearch(query.trim());
    }
  };

  const handleChipClick = (sampleQuery: string) => {
    setQuery(sampleQuery);
    onSearch(sampleQuery);
  };

  return (
    <div className="w-full max-w-4xl mx-auto space-y-3">
      <form onSubmit={handleSubmit} className="relative w-full">
        <div className="relative flex items-center shadow-lg rounded-xl overflow-hidden bg-white border-2 border-gray-200 focus-within:border-bis-blue focus-within:ring-2 focus-within:ring-bis-blue/20 transition-all">
          <input
            name="query"
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Describe your procurement needs... e.g., '5 HP submersible agricultural pump'"
            className="w-full pl-5 pr-36 py-4 text-base md:text-lg outline-none text-gray-800 placeholder-gray-400 bg-transparent"
            disabled={isLoading}
            autoFocus
          />
          <button
            type="submit"
            disabled={isLoading || !query.trim()}
            className="absolute right-2 z-30 px-6 py-2.5 bg-bis-blue text-white rounded-lg font-semibold hover:bg-blue-900 active:scale-95 disabled:opacity-50 disabled:cursor-not-allowed disabled:hover:bg-bis-blue transition-all flex items-center gap-2 cursor-pointer shadow"
          >
            {isLoading ? (
              <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin" />
            ) : (
              <Search size={18} />
            )}
            <span>{isLoading ? 'Searching...' : 'Search'}</span>
          </button>
        </div>
      </form>

      {/* Quick Example Chips */}
      <div className="flex flex-wrap items-center gap-2 pt-1 text-sm text-gray-500">
        <span className="font-medium text-gray-600">Try searching:</span>
        {[
          { label: '5 HP submersible pump, stainless s...', query: '5 HP submersible pump, stainless steel shaft for agricultural borewell' },
          { label: 'खेती के लिए सबमर्सिबल पंप', query: 'खेती के लिए 5 एचपी सबमर्सिबल पंप' },
          { label: 'PVC insulated copper cable...', query: 'PVC insulated copper cable for electrical wiring in residential buildings' },
          { label: 'Fe 500D TMT steel bars...', query: 'Fe 500D TMT reinforcement steel bars for foundation RCC columns' },
        ].map((example) => (
          <button
            key={example.label}
            type="button"
            onClick={() => handleChipClick(example.query)}
            disabled={isLoading}
            className="px-3 py-1 bg-white hover:bg-blue-50 text-bis-blue hover:text-blue-900 border border-gray-200 hover:border-bis-blue/40 rounded-full text-xs font-medium transition-colors shadow-sm disabled:opacity-50 truncate max-w-[220px] cursor-pointer"
          >
            {example.label}
          </button>
        ))}
      </div>
    </div>
  );
}
