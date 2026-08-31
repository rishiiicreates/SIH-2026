'use client';

import { useState } from 'react';
import SearchBar from '../components/SearchBar';
import ResultCard from '../components/ResultCard';
import { RecommendResponse } from '../types';
import { fetchRecommendations } from '../lib/api';
import { BookOpen, AlertCircle } from 'lucide-react';

export default function Home() {
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [data, setData] = useState<RecommendResponse | null>(null);

  const handleSearch = async (query: string) => {
    setIsLoading(true);
    setError(null);
    try {
      const response = await fetchRecommendations(query);
      setData(response);
    } catch (err: any) {
      console.error(err);
      setData(null);
      setError(err?.message || 'Failed to fetch recommendations. Please try again later.');
    } finally {
      setIsLoading(false);
    }
  };

  const handleClear = () => {
    setData(null);
    setError(null);
  };

  return (
    <main className="flex-1 w-full flex flex-col min-h-screen">
      {/* Header */}
      <header className="bg-bis-blue text-white py-12 px-4 shadow-md relative overflow-hidden">
        <div className="absolute top-0 left-0 w-full h-2 bg-bis-saffron"></div>
        <div className="max-w-5xl mx-auto text-center space-y-2">
          <h1 className="text-4xl sm:text-5xl md:text-6xl font-extrabold tracking-tight">
            Manak
          </h1>
          <p className="text-blue-100 text-base md:text-lg font-medium tracking-wide">
            BIS Standards Recommendation Engine
          </p>
        </div>
      </header>

      {/* Main Content */}
      <div className="max-w-5xl mx-auto w-full px-4 py-8 flex-1 flex flex-col">
        <div className="mb-8 -mt-16 relative z-10">
          <SearchBar onSearch={handleSearch} isLoading={isLoading} />
        </div>

        <div className="flex-1">
          {error && (
            <div className="bg-red-50 border-l-4 border-red-500 p-4 mb-8 rounded-lg shadow-sm">
              <div className="flex items-center justify-between">
                <div className="flex items-center">
                  <AlertCircle className="text-red-500 mr-3 shrink-0" size={20} />
                  <p className="text-red-700 font-medium text-sm md:text-base">{error}</p>
                </div>
                <button
                  onClick={() => setError(null)}
                  className="text-xs font-semibold text-red-600 hover:text-red-800 underline ml-4 cursor-pointer"
                >
                  Dismiss
                </button>
              </div>
            </div>
          )}

          {!isLoading && !data && !error && (
            <div className="flex flex-col items-center justify-center py-20 text-gray-400">
              <BookOpen size={56} className="mb-4 text-gray-300" />
              <h2 className="text-lg font-medium text-gray-500">Enter a product description to find applicable Indian Standards</h2>
              <p className="text-xs text-gray-400 mt-1">Or click one of the example chips above to see live recommendations</p>
            </div>
          )}

          {isLoading && (
            <div className="space-y-5">
              {[1, 2, 3].map((i) => (
                <div key={i} className="bg-white rounded-xl shadow-sm border border-gray-200 p-6 animate-pulse space-y-4">
                  <div className="flex justify-between items-start">
                    <div className="space-y-2.5 w-2/3">
                      <div className="h-7 bg-gray-200 rounded w-1/3"></div>
                      <div className="h-4 bg-gray-200 rounded w-full"></div>
                      <div className="h-4 bg-gray-200 rounded w-4/5"></div>
                    </div>
                    <div className="h-9 w-24 bg-gray-200 rounded-lg"></div>
                  </div>
                  <div className="h-10 bg-gray-100 rounded-md w-full"></div>
                </div>
              ))}
            </div>
          )}

          {data && data.recommendations.length > 0 && !isLoading && (
            <div className="space-y-5">
              <div className="flex items-center justify-between pb-2 border-b border-gray-200">
                <h2 className="text-lg font-semibold text-gray-800">
                  Found {data.total_results} Standards for "{data.query}"
                </h2>
                <button
                  onClick={handleClear}
                  className="text-xs font-semibold text-gray-500 hover:text-bis-blue px-3 py-1 bg-gray-100 hover:bg-blue-50 border border-gray-200 rounded-md transition-colors cursor-pointer"
                >
                  Clear Results
                </button>
              </div>
              {data.recommendations.map((rec) => (
                <ResultCard key={rec.standard_id} recommendation={rec} query={data.query} />
              ))}
            </div>
          )}

          {data && data.recommendations.length === 0 && !isLoading && (
            <div className="text-center py-16 bg-white rounded-xl border border-gray-200 shadow-sm">
              <AlertCircle size={44} className="mx-auto text-gray-400 mb-3" />
              <h2 className="text-lg font-semibold text-gray-800">No matching standards found</h2>
              <p className="text-xs text-gray-500 mt-1">Try a broader description or check your standard keywords.</p>
            </div>
          )}
        </div>
      </div>
    </main>
  );
}
