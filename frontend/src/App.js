import React, { useState, useRef } from 'react';
import axios from 'axios';
import { BsFileEarmarkText, BsFolder2Open, BsCheckCircle, BsXCircle } from 'react-icons/bs';
import './App.css';


const API_URL = 'http://localhost:8000/api';
const EXT_OPTIONS = [
  { label: '.txt', value: '.txt' },
  { label: '.pdf', value: '.pdf' },
];

function parseIaResponse(resp) {
  if (!resp) return { answer: '', justification: '' };
  const lower = resp.toLowerCase();
  if (lower.startsWith('sim')) {
    const [answer, ...rest] = resp.split(/\.\s|:/);
    return { answer: 'Sim', justification: rest.join('.').trim() };
  }
  if (lower.startsWith('não') || lower.startsWith('nao')) {
    const [answer, ...rest] = resp.split(/\.\s|:/);
    return { answer: 'Não', justification: rest.join('.').trim() };
  }
  return { answer: '', justification: resp };
}

function getDefaultDownloadFolder() {
  const user = window?.navigator?.userAgent?.includes('Windows') ? process.env.USERNAME : process.env.USER;
  return `C:\\Users\\${user || 'SeuUsuario'}\\Downloads`;
}

function App() {
  const [query, setQuery] = useState('');
  const [folder, setFolder] = useState('');
  const [extensions, setExtensions] = useState(['.txt', '.pdf']);
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const resultsRef = useRef(null);

  const handleExtChange = (ext) => {
    setExtensions((prev) =>
      prev.includes(ext) ? prev.filter((e) => e !== ext) : [...prev, ext]
    );
  };

  const handleSearch = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setResults([]);
    try {
      const response = await fetch(`${API_URL}/search/stream`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query, folder, extensions }),
      });
      if (!response.body) throw new Error('Stream não suportado');
      const reader = response.body.getReader();
      const decoder = new TextDecoder();
      let buffer = '';
      while (true) {
        const { done, value } = await reader.read();
        if (done) break;
        buffer += decoder.decode(value, { stream: true });
        let lines = buffer.split('\n');
        buffer = lines.pop();
        for (const line of lines) {
          if (line.trim()) {
            try {
              const parsed = JSON.parse(line);
              setResults((prev) => [...prev, parsed]);
            } catch {
              console.warn('Linha inválida:', line);
            }
            setTimeout(() => {
              if (resultsRef.current) {
                resultsRef.current.scrollTop = resultsRef.current.scrollHeight;
              }
            }, 100);
          }
        }
      }
    } catch (err) {
      setError('Erro ao realizar a busca. Tente novamente.');
    } finally {
      setLoading(false);
    }
  };

  const handleOpenFile = async (filePath) => {
    try {
      await axios.post(`${API_URL}/open`, { file_path: filePath });
    } catch {
      alert('Erro ao tentar abrir o arquivo.');
    }
  };

  return (
    <div className="bg-light py-5 min-vh-100">
      <div className="container" style={{ maxWidth: 720 }}>
        <div className="card border-0 shadow-lg rounded-4 p-4">
          <div className="text-center mb-4">
            <h2 className="fw-bold mb-1 fs-2">
              <BsFileEarmarkText /> Busca Inteligente
            </h2>
            <p className="text-muted small">Use IA local para encontrar arquivos relevantes com base no conteúdo</p>
          </div>
          <form onSubmit={handleSearch} className="mb-4">
            <div className="row g-3">
              <div className="col-12">
                <label className="form-label fw-semibold">🔍 Termo de busca</label>
                <input type="text" className="form-control" value={query} onChange={e => setQuery(e.target.value)} required />
              </div>
              <div className="col-12">
                <label className="form-label fw-semibold"><BsFolder2Open /> Pasta</label>
                <input type="text" className="form-control" value={folder} onChange={e => setFolder(e.target.value)} placeholder="(opcional) Ex: C:\\Users\\SeuUser\\Downloads" />
              </div>
              <div className="col-12">
                <label className="form-label fw-semibold">📄 Extensões</label>
                <div className="d-flex gap-3">
                  {EXT_OPTIONS.map(opt => (
                    <div key={opt.value} className="form-check">
                      <input className="form-check-input" type="checkbox" checked={extensions.includes(opt.value)} onChange={() => handleExtChange(opt.value)} id={opt.value} />
                      <label className="form-check-label" htmlFor={opt.value}>{opt.label}</label>
                    </div>
                  ))}
                </div>
              </div>
            </div>
            <button type="submit" className="btn btn-primary w-100 mt-3 fw-bold" disabled={loading}>
              {loading ? 'Buscando...' : '🔎 Buscar'}
            </button>
          </form>
          {error && <div className="alert alert-danger text-center">{error}</div>}

          <div ref={resultsRef} className="overflow-auto" style={{ maxHeight: 450 }}>
            {results.length > 0 ? (
              <ul className="list-group">
                {results.map((r, i) => {
                  const { answer, justification } = parseIaResponse(r.ia_response);
                  const fileName = r.file_path ? r.file_path.split(/\\|\//).pop() : '';
                  return (
                    <li key={i} className="list-group-item border rounded mb-2 shadow-sm">
                      <div className="d-flex justify-content-between align-items-center mb-2">
                        <div>
                          <span className="fw-bold fs-5" title={r.file_path}>{fileName}</span>
                          <div className="text-muted small" title={r.file_path} style={{ maxWidth: 500, wordBreak: 'break-word' }}>{r.file_path}</div>
                        </div>
                        <button onClick={() => handleOpenFile(r.file_path)} className="btn btn-outline-dark btn-sm ms-3">Abrir</button>
                      </div>
                      <div className="d-flex flex-wrap gap-3 align-items-center">
                        <span className={`badge ${answer === 'Sim' ? 'bg-success' : answer === 'Não' ? 'bg-danger' : 'bg-secondary'} px-3 py-2 fs-6 fw-semibold`}>
                          {answer === 'Sim' ? <BsCheckCircle className="me-1" /> : answer === 'Não' ? <BsXCircle className="me-1" /> : null}
                          {answer}
                        </span>
                        <span className="text-dark small"><strong>Justificativa:</strong> {justification}</span>
                      </div>
                    </li>
                  );
                })}
              </ul>
            ) : !loading && (
              <div className="alert alert-secondary text-center">Nenhum arquivo encontrado. 🧐</div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;
