export interface Reference {
  referenced_id: string;
  title: string;
  relationship_type: string;
}

export interface StandardMetadata {
  latest_version?: string;
  amendment_date?: string;
  is_mandatory_qco?: boolean;
}

export interface Recommendation {
  standard_id: string;
  title: string;
  similarity: number;
  references: Reference[];
  metadata: StandardMetadata;
}

export interface RecommendResponse {
  query: string;
  recommendations: Recommendation[];
  total_results: number;
}
