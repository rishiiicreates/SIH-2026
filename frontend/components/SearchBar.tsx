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

  return (
    <form onSubmit={handleSubmit} className="w-full max-w-4xl mx-auto">
      <div className="relative flex items-center">
        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Describe your procurement needs... e.g., '5 HP submersible agricultural pump'"
          className="w-full pl-5 pr-32 py-4 text-lg border-2 border-gray-300 rounded-xl focus:border-bis-blue focus:ring-1 focus:ring-bis-blue outline-none transition-all shadow-sm"
          disabled={isLoading}
        />
        <button
          type="submit"
          disabled={isLoading || !query.trim()}
          className="absolute right-2 px-6 py-2.5 bg-bis-blue text-white rounded-lg font-medium hover:bg-blue-900 disabled:opacity-70 disabled:cursor-not-allowed transition-colors flex items-center gap-2"
        >
          {isLoading ? (
            <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin" />
          ) : (
            <Search size={20} />
          )}
          <span>Search</span>
        </button>
      </div>
    </form>
  );
}
