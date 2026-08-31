export interface Reference {
  referenced_id: string;
  title?: string | null;
  relationship_type?: string | null;
}

export interface StandardMetadata {
  latest_version?: string | null;
  amendment_date?: string | null;
  is_mandatory_qco?: boolean;
}

export interface Recommendation {
  standard_id: string;
  title: string;
  similarity: number;
  references: Reference[];
  metadata?: StandardMetadata | null;
}

export interface RecommendResponse {
  query: string;
  recommendations: Recommendation[];
  total_results: number;
}
