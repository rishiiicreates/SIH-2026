import { RecommendResponse } from '../types';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export async function fetchRecommendations(query: string, top_k: number = 5): Promise<RecommendResponse> {
  const response = await fetch(`${API_URL}/api/v1/recommend`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ query, top_k }),
  });

  if (!response.ok) {
    throw new Error('Failed to fetch recommendations');
  }

  return response.json();
}
