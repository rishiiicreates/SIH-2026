'use client';

import { useState } from 'react';
import { Recommendation } from '../types';
import ReferenceList from './ReferenceList';
import TenderClauseModal from './TenderClauseModal';
import { CheckCircle, Info, FileSignature } from 'lucide-react';

interface ResultCardProps {
  recommendation: Recommendation;
  query: string;
}

export default function ResultCard({ recommendation, query }: ResultCardProps) {
  const [showClauseModal, setShowClauseModal] = useState(false);
  const { standard_id, title, similarity, references, metadata } = recommendation;
  const similarityPercentage = Math.round(similarity * 100);

  return (
    <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6 hover:shadow-md transition-shadow">
      <div className="flex flex-col md:flex-row justify-between items-start gap-4 mb-4">
        <div className="flex-1">
          <div className="flex items-center gap-3 mb-2">
            <h2 className="text-2xl font-bold text-bis-blue">{standard_id}</h2>
            {metadata?.is_mandatory_qco ? (
              <span className="flex items-center gap-1 text-xs font-medium bg-green-50 text-green-700 px-2.5 py-1 rounded-full border border-green-200">
                <CheckCircle size={14} />
                QCO Mandatory
              </span>
            ) : (
              <span className="flex items-center gap-1 text-xs font-medium bg-gray-100 text-gray-600 px-2.5 py-1 rounded-full border border-gray-200">
                <Info size={14} />
                No QCO
              </span>
            )}
          </div>
          <h3 className="text-base sm:text-lg text-gray-800 font-medium leading-snug">{title}</h3>
        </div>
        
        <div className="flex flex-row md:flex-col items-center md:items-end gap-2.5 shrink-0 w-full md:w-auto justify-between md:justify-start">
          <div className="flex items-center justify-center bg-bis-saffron/10 border border-bis-saffron/30 text-bis-saffron font-bold text-base px-3.5 py-1.5 rounded-lg">
            {similarityPercentage}% Match
          </div>
          <button
            onClick={() => setShowClauseModal(true)}
            className="flex items-center justify-center gap-1.5 bg-bis-blue text-white py-2 px-3.5 rounded-lg text-xs sm:text-sm font-semibold hover:bg-blue-900 transition-colors cursor-pointer shadow-sm active:scale-[0.98] whitespace-nowrap"
          >
            <FileSignature size={15} />
            <span>Generate Tender Clause</span>
          </button>
        </div>
      </div>

      <div className="text-sm text-gray-600 bg-blue-50/50 p-3 rounded-md mb-4 border border-blue-100/50">
        <span className="font-semibold text-gray-700">Latest Version:</span> {metadata?.latest_version || 'N/A'}
      </div>

      <ReferenceList references={references} />

      {showClauseModal && (
        <TenderClauseModal
          onClose={() => setShowClauseModal(false)}
          recommendation={recommendation}
          query={query}
        />
      )}
    </div>
  );
}
