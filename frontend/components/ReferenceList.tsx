'use client';

import { useState } from 'react';
import { ChevronDown, ChevronUp, FileText } from 'lucide-react';
import { Reference } from '../types';

interface ReferenceListProps {
  references: Reference[];
}

export default function ReferenceList({ references }: ReferenceListProps) {
  const [isExpanded, setIsExpanded] = useState(false);

  if (!references || references.length === 0) {
    return null;
  }

  const getRelationshipColor = (type: string | null | undefined) => {
    switch ((type ?? '').toUpperCase()) {
      case 'RAW_MATERIAL':
        return 'bg-amber-100 text-amber-800 border-amber-200';
      case 'TEST_METHOD':
        return 'bg-blue-100 text-blue-800 border-blue-200';
      case 'INSTALLATION_CODE':
      case 'MAINTENANCE_CODE':
      case 'APPLICATION_CODE':
      case 'SAFETY_CODE':
      case 'DESIGN_CODE':
      case 'HIGHWAY_CODE':
        return 'bg-green-100 text-green-800 border-green-200';
      case 'COMPONENT':
      case 'COMPONENT_DRIVER':
      case 'PARENT_STANDARD':
        return 'bg-purple-100 text-purple-800 border-purple-200';
      case 'SEISMIC_SAFETY':
      case 'ALLIED_SAFETY':
        return 'bg-red-100 text-red-800 border-red-200';
      case 'PERFORMANCE':
        return 'bg-teal-100 text-teal-800 border-teal-200';
      default:
        return 'bg-gray-100 text-gray-800 border-gray-200';
    }
  };

  return (
    <div className="mt-4 border border-gray-100 rounded-lg overflow-hidden bg-gray-50/50">
      <button
        onClick={() => setIsExpanded(!isExpanded)}
        className="w-full flex items-center justify-between p-3 text-sm font-medium text-gray-700 hover:bg-gray-100 transition-colors cursor-pointer"
      >
        <div className="flex items-center gap-2">
          <FileText size={16} className="text-gray-500" />
          <span>Normative & Allied References ({references.length})</span>
        </div>
        {isExpanded ? <ChevronUp size={18} /> : <ChevronDown size={18} />}
      </button>

      {isExpanded && (
        <div className="p-3 border-t border-gray-100 flex flex-col gap-2">
          {references.map((ref, index) => (
            <div key={index} className="flex flex-col sm:flex-row sm:items-start justify-between p-3 bg-white border border-gray-100 rounded shadow-sm gap-2">
              <div className="flex-1">
                <div className="font-semibold text-bis-blue text-sm">{ref.referenced_id}</div>
                <div className="text-sm text-gray-600 mt-0.5">{ref.title}</div>
              </div>
              <div className="shrink-0 mt-1 sm:mt-0">
                <span className={`text-xs px-2.5 py-1 rounded-full border font-medium uppercase tracking-wider ${getRelationshipColor(ref.relationship_type)}`}>
                  {(ref.relationship_type ?? 'REFERENCE').replace(/_/g, ' ')}
                </span>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
