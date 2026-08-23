import { Recommendation } from '../types';
import ReferenceList from './ReferenceList';
import { CheckCircle, Info } from 'lucide-react';

interface ResultCardProps {
  recommendation: Recommendation;
}

export default function ResultCard({ recommendation }: ResultCardProps) {
  const { standard_id, title, similarity, references, metadata } = recommendation;
  const similarityPercentage = Math.round(similarity * 100);

  return (
    <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6 hover:shadow-md transition-shadow">
      <div className="flex flex-col md:flex-row justify-between items-start gap-4 mb-4">
        <div>
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
          <h3 className="text-lg text-gray-800 font-medium leading-snug">{title}</h3>
        </div>
        
        <div className="flex flex-col items-end">
          <div className="flex items-center justify-center bg-bis-saffron/10 border border-bis-saffron/30 text-bis-saffron font-bold text-lg px-4 py-2 rounded-lg">
            {similarityPercentage}% Match
          </div>
        </div>
      </div>

      <div className="text-sm text-gray-600 bg-blue-50/50 p-3 rounded-md mb-4 border border-blue-100/50">
        <span className="font-semibold text-gray-700">Latest Version:</span> {metadata?.latest_version || 'N/A'}
      </div>

      <ReferenceList references={references} />
    </div>
  );
}
