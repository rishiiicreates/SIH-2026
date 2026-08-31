import { RecommendResponse } from '../types';

const API_URL = process.env.NEXT_PUBLIC_API_URL || '';

export async function fetchRecommendations(query: string, top_k: number = 5): Promise<RecommendResponse> {
  const controller = new AbortController();
  const timeoutId = setTimeout(() => controller.abort(), 15000);

  try {
    const response = await fetch(`${API_URL}/api/v1/recommend`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ query, top_k }),
      signal: controller.signal,
    });
    clearTimeout(timeoutId);

    if (!response.ok) {
      const errorText = await response.text();
      let errorDetail = response.statusText;
      try {
        const jsonError = JSON.parse(errorText);
        errorDetail = jsonError.detail || errorDetail;
      } catch {
        errorDetail = errorText || errorDetail;
      }
      throw new Error(`API Error (${response.status}): ${errorDetail}`);
    }

    return response.json();
  } catch (err: any) {
    clearTimeout(timeoutId);
    if (err.name === 'AbortError') {
      throw new Error('Search request timed out after 15 seconds. Please try again.');
    }
    if (err.message && (err.message.includes('Failed to fetch') || err.message.includes('NetworkError') || err.name === 'TypeError')) {
      throw new Error(
        `Cannot connect to backend server at ${API_URL}. Ensure the FastAPI server is running (uvicorn app.main:app --port 8000).`
      );
    }
    throw err;
  }
}

