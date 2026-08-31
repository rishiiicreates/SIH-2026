import { NextRequest, NextResponse } from "next/server";

const SUPABASE_URL = process.env.SUPABASE_URL || "";
const SUPABASE_KEY = process.env.SUPABASE_KEY || "";
const GEMINI_API_KEY = process.env.GEMINI_API_KEY || "";
const EMBEDDING_MODEL = process.env.EMBEDDING_MODEL || "models/gemini-embedding-001";

function cosineSimilarity(v1: number[], v2: number[]): number {
  let dot = 0, mag1 = 0, mag2 = 0;
  for (let i = 0; i < v1.length; i++) {
    dot += v1[i] * v2[i];
    mag1 += v1[i] * v1[i];
    mag2 += v2[i] * v2[i];
  }
  if (mag1 === 0 || mag2 === 0) return 0;
  return dot / (Math.sqrt(mag1) * Math.sqrt(mag2));
}

async function getEmbedding(text: string): Promise<number[]> {
  const modelName = EMBEDDING_MODEL.startsWith("models/") ? EMBEDDING_MODEL : "models/" + EMBEDDING_MODEL;
  const url = "https://generativelanguage.googleapis.com/v1beta/" + modelName + ":embedContent?key=" + GEMINI_API_KEY;
  
  const res = await fetch(url, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      content: { parts: [{ text }] },
      outputDimensionality: 768
    })
  });

  if (!res.ok) {
    const errText = await res.text();
    throw new Error("Gemini embedding failed (" + res.status + "): " + errText);
  }

  const data = await res.json();
  return data.embedding.values;
}

export async function POST(req: NextRequest) {
  try {
    const body = await req.json();
    const query = (body.query || "").trim();
    const top_k = Math.min(Math.max(body.top_k || 5, 1), 20);

    if (!query) {
      return NextResponse.json({ error: "Query is required" }, { status: 400 });
    }

    const queryEmbedding = await getEmbedding(query);

    let searchResults: Array<{ standard_id: string; title: string; similarity: number }> = [];

    // 1. Try Supabase pgvector RPC
    try {
      const rpcRes = await fetch(SUPABASE_URL + "/rest/v1/rpc/match_standards", {
        method: "POST",
        headers: {
          "apikey": SUPABASE_KEY,
          "Authorization": "Bearer " + SUPABASE_KEY,
          "Content-Type": "application/json",
          "Prefer": "return=representation"
        },
        body: JSON.stringify({
          query_embedding: queryEmbedding,
          match_count: top_k
        })
      });

      if (rpcRes.ok) {
        const rpcData = await rpcRes.json();
        if (Array.isArray(rpcData) && rpcData.length > 0) {
          searchResults = rpcData;
        }
      }
    } catch (e) {
      console.warn("RPC vector match failed, falling back to in-memory search", e);
    }

    // 2. Fallback in-memory search if RPC yielded nothing
    if (searchResults.length === 0) {
      const tableRes = await fetch(SUPABASE_URL + "/rest/v1/standards?select=standard_id,title,embedding", {
        headers: {
          "apikey": SUPABASE_KEY,
          "Authorization": "Bearer " + SUPABASE_KEY
        }
      });
      if (tableRes.ok) {
        const tableData = await tableRes.json();
        const scored = [];
        for (const row of tableData) {
          if (!row.embedding) continue;
          let emb = row.embedding;
          if (typeof emb === "string") {
            try { emb = JSON.parse(emb); } catch { continue; }
          }
          const sim = cosineSimilarity(queryEmbedding, emb);
          scored.push({
            standard_id: row.standard_id,
            title: row.title,
            similarity: sim
          });
        }
        scored.sort((a, b) => b.similarity - a.similarity);
        searchResults = scored.slice(0, top_k);
      }
    }

    if (searchResults.length === 0) {
      return NextResponse.json({
        query,
        recommendations: [],
        total_results: 0
      });
    }

    const standardIds = searchResults.map(r => r.standard_id);

    // 3. Batch fetch references and metadata
    const idsParam = "in.(" + standardIds.map(s => encodeURIComponent(s)).join(",") + ")";

    const [refsRes, metaRes] = await Promise.all([
      fetch(SUPABASE_URL + "/rest/v1/standard_references?standard_id=" + idsParam + "&select=standard_id,referenced_id,referenced_title,relationship_type", {
        headers: { "apikey": SUPABASE_KEY, "Authorization": "Bearer " + SUPABASE_KEY }
      }),
      fetch(SUPABASE_URL + "/rest/v1/standards?standard_id=" + idsParam + "&select=standard_id,latest_version,amendment_date,is_mandatory_qco", {
        headers: { "apikey": SUPABASE_KEY, "Authorization": "Bearer " + SUPABASE_KEY }
      })
    ]);

    const allRefs: Record<string, any[]> = {};
    for (const sid of standardIds) allRefs[sid] = [];

    if (refsRes.ok) {
      const refsData = await refsRes.json();
      if (Array.isArray(refsData)) {
        for (const r of refsData) {
          if (allRefs[r.standard_id]) {
            allRefs[r.standard_id].push({
              referenced_id: r.referenced_id,
              title: r.referenced_title,
              relationship_type: r.relationship_type
            });
          }
        }
      }
    }

    const allMeta: Record<string, any> = {};
    if (metaRes.ok) {
      const metaData = await metaRes.json();
      if (Array.isArray(metaData)) {
        for (const m of metaData) {
          allMeta[m.standard_id] = {
            latest_version: m.latest_version,
            amendment_date: m.amendment_date,
            is_mandatory_qco: Boolean(m.is_mandatory_qco)
          };
        }
      }
    }

    const recommendations = searchResults.map(res => ({
      standard_id: res.standard_id,
      title: res.title,
      similarity: res.similarity,
      references: allRefs[res.standard_id] || [],
      metadata: allMeta[res.standard_id] || null
    }));

    return NextResponse.json({
      query,
      recommendations,
      total_results: recommendations.length
    });
  } catch (error: any) {
    console.error("Recommend API error:", error);
    return NextResponse.json(
      { error: error?.message || "Internal recommendation error" },
      { status: 500 }
    );
  }
}
