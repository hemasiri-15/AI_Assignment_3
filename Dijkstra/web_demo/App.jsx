import { useState, useCallback } from "react";

const CITIES = [
  "Delhi","Mumbai","Kolkata","Chennai","Bangalore","Hyderabad","Ahmedabad",
  "Pune","Jaipur","Lucknow","Kanpur","Nagpur","Indore","Bhopal","Patna",
  "Vadodara","Surat","Ludhiana","Agra","Varanasi","Amritsar","Meerut",
  "Visakhapatnam","Coimbatore","Kochi","Thiruvananthapuram","Bhubaneswar",
  "Guwahati","Chandigarh","Raipur","Jodhpur","Udaipur","Srinagar","Shimla"
];

const EDGES = [
  ["Delhi","Jaipur",280],["Delhi","Agra",233],["Delhi","Chandigarh",250],
  ["Delhi","Amritsar",450],["Delhi","Ludhiana",310],["Delhi","Meerut",72],
  ["Delhi","Lucknow",555],["Delhi","Dehradun",300],
  ["Agra","Lucknow",363],["Agra","Jaipur",232],["Agra","Gwalior",119],
  ["Jaipur","Jodhpur",340],["Jaipur","Udaipur",395],["Jaipur","Ahmedabad",670],
  ["Jaipur","Bhopal",610],
  ["Chandigarh","Shimla",115],["Chandigarh","Amritsar",230],
  ["Amritsar","Srinagar",290],
  ["Lucknow","Kanpur",80],["Lucknow","Varanasi",330],["Lucknow","Patna",580],
  ["Kanpur","Agra",280],["Kanpur","Varanasi",340],
  ["Varanasi","Patna",250],["Varanasi","Kolkata",680],
  ["Patna","Kolkata",600],["Patna","Bhubaneswar",850],
  ["Mumbai","Pune",155],["Mumbai","Ahmedabad",530],["Mumbai","Nagpur",900],
  ["Mumbai","Surat",290],["Mumbai","Goa",590],
  ["Surat","Ahmedabad",265],["Surat","Vadodara",153],
  ["Ahmedabad","Vadodara",110],["Ahmedabad","Udaipur",260],["Ahmedabad","Indore",570],
  ["Vadodara","Indore",398],["Vadodara","Surat",153],
  ["Pune","Hyderabad",570],["Pune","Bangalore",840],["Pune","Nagpur",710],
  ["Nagpur","Hyderabad",502],["Nagpur","Raipur",295],["Nagpur","Bhopal",370],
  ["Nagpur","Indore",500],
  ["Indore","Bhopal",195],["Indore","Ujjain",55],["Indore","Nagpur",500],
  ["Bhopal","Jabalpur",290],["Bhopal","Nagpur",370],
  ["Raipur","Bhubaneswar",430],["Raipur","Nagpur",295],["Raipur","Visakhapatnam",665],
  ["Hyderabad","Chennai",630],["Hyderabad","Bangalore",570],
  ["Hyderabad","Visakhapatnam",620],
  ["Chennai","Bangalore",350],["Chennai","Coimbatore",500],["Chennai","Visakhapatnam",800],
  ["Chennai","Kochi",680],["Chennai","Thiruvananthapuram",740],
  ["Bangalore","Coimbatore",360],["Bangalore","Kochi",540],["Bangalore","Thiruvananthapuram",680],
  ["Coimbatore","Kochi",190],["Coimbatore","Thiruvananthapuram",310],
  ["Kochi","Thiruvananthapuram",210],
  ["Kolkata","Bhubaneswar",440],["Kolkata","Guwahati",1030],["Kolkata","Visakhapatnam",1100],
  ["Bhubaneswar","Visakhapatnam",440],
  ["Jodhpur","Udaipur",260],["Jodhpur","Ahmedabad",460],
];

function buildGraph() {
  const graph = {};
  CITIES.forEach(c => { graph[c] = []; });
  EDGES.forEach(([a, b, d]) => {
    graph[a].push({ to: b, dist: d });
    graph[b].push({ to: a, dist: d });
  });
  return graph;
}

function dijkstra(graph, source) {
  const dist = {};
  const prev = {};
  const visited = new Set();
  const steps = [];
  CITIES.forEach(c => { dist[c] = Infinity; prev[c] = null; });
  dist[source] = 0;
  const pq = [{ node: source, d: 0 }];
  while (pq.length > 0) {
    pq.sort((a, b) => a.d - b.d);
    const { node: u } = pq.shift();
    if (visited.has(u)) continue;
    visited.add(u);
    steps.push({ visiting: u, distSnapshot: { ...dist }, prevSnapshot: { ...prev } });
    for (const { to: v, dist: w } of (graph[u] || [])) {
      if (!visited.has(v)) {
        const alt = dist[u] + w;
        if (alt < dist[v]) {
          dist[v] = alt;
          prev[v] = u;
          pq.push({ node: v, d: alt });
        }
      }
    }
  }
  return { dist, prev, steps };
}

function getPath(prev, target) {
  const path = [];
  let cur = target;
  while (cur) { path.unshift(cur); cur = prev[cur]; }
  return path;
}

export default function App() {
  const [source, setSource] = useState("Delhi");
  const [target, setTarget] = useState("Mumbai");
  const [result, setResult] = useState(null);
  const [selectedTarget, setSelectedTarget] = useState(null);
  const [stepView, setStepView] = useState(false);
  const [currentStep, setCurrentStep] = useState(0);
  const graph = buildGraph();

  const run = useCallback(() => {
    const res = dijkstra(graph, source);
    setResult(res);
    setSelectedTarget(target);
    setCurrentStep(0);
    setStepView(false);
  }, [source, target]);

  const path = result && selectedTarget ? getPath(result.prev, selectedTarget) : [];
  const pathDist = result && selectedTarget ? result.dist[selectedTarget] : null;
  const stepData = result && stepView ? result.steps[currentStep] : null;

  return (
    <div style={{
      minHeight: "100vh",
      background: "linear-gradient(135deg, #0f0c29, #302b63, #24243e)",
      fontFamily: "'Courier New', monospace",
      color: "#e0e0ff", padding: "20px"
    }}>
      <div style={{ maxWidth: 1100, margin: "0 auto" }}>
        <div style={{ textAlign: "center", marginBottom: 32 }}>
          <div style={{
            display: "inline-block",
            background: "linear-gradient(90deg, #f7971e, #ffd200)",
            WebkitBackgroundClip: "text", WebkitTextFillColor: "transparent",
            fontSize: 32, fontWeight: 900, letterSpacing: 2, textTransform: "uppercase"
          }}>🗺️ Dijkstra's Algorithm</div>
          <div style={{ color: "#aaa", fontSize: 14, marginTop: 4 }}>
            Shortest Road Paths Between Major Indian Cities
          </div>
        </div>

        <div style={{ display: "flex", gap: 16, flexWrap: "wrap",
          justifyContent: "center", marginBottom: 28, alignItems: "flex-end" }}>
          {[["Source City", source, setSource], ["Target City", target, setTarget]].map(([label, val, setter]) => (
            <div key={label}>
              <div style={{ fontSize: 11, color: "#aaa", marginBottom: 4, letterSpacing: 1 }}>
                {label.toUpperCase()}
              </div>
              <select value={val} onChange={e => setter(e.target.value)}
                style={{ background: "#1a1a3a", color: "#f0f0ff",
                  border: "1px solid #5555aa", borderRadius: 8,
                  padding: "8px 14px", fontSize: 14, cursor: "pointer", minWidth: 160 }}>
                {CITIES.sort().map(c => <option key={c} value={c}>{c}</option>)}
              </select>
            </div>
          ))}
          <button onClick={run} style={{
            background: "linear-gradient(90deg, #f7971e, #ffd200)",
            color: "#1a1a2e", fontWeight: 800, border: "none",
            borderRadius: 8, padding: "10px 28px", fontSize: 14,
            cursor: "pointer", letterSpacing: 1, textTransform: "uppercase"
          }}>▶ Run Dijkstra</button>
        </div>

        {result && (
          <>
            <div style={{ background: "rgba(255,255,255,0.05)",
              border: "1px solid #ffd20066", borderRadius: 12,
              padding: "18px 24px", marginBottom: 24 }}>
              <div style={{ fontSize: 13, color: "#ffd200", marginBottom: 8, fontWeight: 700 }}>
                SHORTEST PATH: {source} → {selectedTarget}
              </div>
              {path.length > 1 ? (
                <>
                  <div style={{ display: "flex", flexWrap: "wrap", gap: 6, alignItems: "center" }}>
                    {path.map((city, i) => (
                      <span key={city} style={{ display: "flex", alignItems: "center", gap: 6 }}>
                        <span style={{
                          background: i === 0 || i === path.length-1 ? "#ffd200" : "#302b63",
                          color: i === 0 || i === path.length-1 ? "#1a1a2e" : "#e0e0ff",
                          borderRadius: 6, padding: "3px 10px", fontSize: 13, fontWeight: 700,
                          border: "1px solid #5555aa"
                        }}>{city}</span>
                        {i < path.length-1 && <span style={{ color: "#f7971e" }}>→</span>}
                      </span>
                    ))}
                  </div>
                  <div style={{ marginTop: 10, color: "#f7971e", fontWeight: 700, fontSize: 16 }}>
                    Total Distance: {pathDist} km
                    <span style={{ color: "#aaa", fontSize: 12, fontWeight: 400, marginLeft: 8 }}>
                      ({path.length - 1} hops)
                    </span>
                  </div>
                </>
              ) : (
                <div style={{ color: "#ff6b6b" }}>No path found</div>
              )}
            </div>

            <div style={{ marginBottom: 16, display: "flex", gap: 12, alignItems: "center", flexWrap: "wrap" }}>
              <button onClick={() => setStepView(v => !v)} style={{
                background: stepView ? "#5555aa" : "rgba(255,255,255,0.08)",
                color: "#e0e0ff", border: "1px solid #5555aa",
                borderRadius: 8, padding: "7px 18px", fontSize: 13, cursor: "pointer"
              }}>{stepView ? "▲ Hide" : "▼ Show"} Step-by-Step ({result.steps.length} steps)</button>
              {stepView && (
                <>
                  <button onClick={() => setCurrentStep(s => Math.max(0, s-1))}
                    disabled={currentStep === 0}
                    style={{ background: "#302b63", color: currentStep===0 ? "#666":"#fff",
                      border: "1px solid #5555aa", borderRadius: 8,
                      padding: "7px 14px", cursor: "pointer" }}>◀ Prev</button>
                  <span style={{ fontSize: 13, color: "#aaa" }}>
                    Step {currentStep+1} / {result.steps.length}
                  </span>
                  <button onClick={() => setCurrentStep(s => Math.min(result.steps.length-1, s+1))}
                    disabled={currentStep === result.steps.length-1}
                    style={{ background: "#302b63",
                      color: currentStep===result.steps.length-1 ? "#666":"#fff",
                      border: "1px solid #5555aa", borderRadius: 8,
                      padding: "7px 14px", cursor: "pointer" }}>Next ▶</button>
                </>
              )}
            </div>

            {stepView && stepData && (
              <div style={{ background: "rgba(255,255,255,0.04)",
                border: "1px solid #5555aa", borderRadius: 10,
                padding: 16, marginBottom: 20, fontSize: 13 }}>
                <span style={{ color: "#ffd200", fontWeight: 700 }}>Visiting: </span>
                <span style={{ color: "#f7971e", fontWeight: 700 }}>{stepData.visiting}</span>
                <span style={{ color: "#aaa", marginLeft: 16 }}>
                  Cost so far: <strong style={{ color: "#fff" }}>
                    {stepData.distSnapshot[stepData.visiting]} km
                  </strong>
                </span>
              </div>
            )}

            <div style={{ fontSize: 13, color: "#aaa", marginBottom: 10 }}>
              All shortest distances from{" "}
              <span style={{ color: "#ffd200", fontWeight: 700 }}>{source}</span>
              <span style={{ fontSize: 11, marginLeft: 8 }}>(click any city to update path)</span>
            </div>
            <div style={{ display: "grid",
              gridTemplateColumns: "repeat(auto-fill, minmax(200px, 1fr))", gap: 8 }}>
              {CITIES.sort().map(city => {
                const d = stepView ? stepData?.distSnapshot[city] : result.dist[city];
                const inPath = path.includes(city);
                return (
                  <div key={city} onClick={() => setSelectedTarget(city)} style={{
                    background: inPath
                      ? "linear-gradient(90deg, #302b0088, #ffd20033)"
                      : city === source ? "rgba(247,151,30,0.15)" : "rgba(255,255,255,0.04)",
                    border: inPath ? "1px solid #ffd200"
                      : city === source ? "1px solid #f7971e" : "1px solid #333366",
                    borderRadius: 8, padding: "8px 12px", cursor: "pointer",
                    display: "flex", justifyContent: "space-between", transition: "all 0.2s"
                  }}>
                    <span style={{ fontWeight: inPath ? 700:400, color: inPath ? "#ffd200":"#ccc" }}>
                      {city === source ? "📍 " : ""}{city}
                    </span>
                    <span style={{ color: d===Infinity ? "#666" : inPath ? "#f7971e":"#88aaff", fontWeight: 700 }}>
                      {d === Infinity ? "∞" : `${d} km`}
                    </span>
                  </div>
                );
              })}
            </div>
          </>
        )}

        <div style={{ marginTop: 32, background: "rgba(255,255,255,0.03)",
          border: "1px solid #333366", borderRadius: 12, padding: 18, fontSize: 13, color: "#aaa" }}>
          <div style={{ color: "#ffd200", fontWeight: 700, marginBottom: 8 }}>
            About This Implementation
          </div>
          <div>
            Uses a <strong style={{ color: "#fff" }}>min-priority queue (best-first search)</strong> on
            road distances between {CITIES.length} major Indian cities with {EDGES.length} road connections.
            Guarantees the globally optimal shortest path to every reachable city.
            Time complexity: <strong style={{ color: "#fff" }}>O((V + E) log V)</strong>.
          </div>
        </div>
      </div>
    </div>
  );
}
