import React, { useState } from 'react';
import axios from 'axios';

const API_URL = 'http://localhost:8000/api';

const EXT_OPTIONS = [
  { label: '.txt', value: '.txt' },
  { label: '.pdf', value: '.pdf' },
];

function App() {
  const [query, setQuery] = useState('');
  const [folder, setFolder] = useState('C:\\Users\\kaue\\Downloads\\Novapasta');
  const [extensions, setExtensions] = useState(['.txt', '.pdf']);
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleExtChange = (ext) => {
    setExtensions((prev) =>
      prev.includes(ext)
        ? prev.filter((e) => e !== ext)
        : [...prev, ext]
    );
  };

  const handleSearch = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setResults([]);
    try {
      const response = await axios.post(`${API_URL}/search`, {
        query,
        folder,
        extensions,
      });
      setResults(response.data);
    } catch (err) {
      setError('Erro ao realizar a busca. Tente novamente.');
    } finally {
      setLoading(false);
    }
  };

  const handleOpenFile = async (filePath) => {
    try {
      await axios.post(`${API_URL}/open`, { file_path: filePath });
    } catch (err) {
      alert('Não foi possível abrir o arquivo.');
    }
  };

  return (
    <div className="min-h-screen bg-gray-100 flex items-center justify-center">
      <div className="bg-white p-8 rounded-2xl shadow-lg w-full max-w-xl">
        <h2 className="text-2xl font-bold mb-6 flex items-center gap-2">
          <span role="img" aria-label="lupa">🔍</span> Busca Inteligente de Arquivos
        </h2>
        <form onSubmit={handleSearch} className="space-y-4">
          <div>
            <label className="block font-semibold mb-1 flex items-center gap-2">
              <span role="img" aria-label="abc">🔤</span> Termo de busca
            </label>
            <input
              type="text"
              className="w-full border rounded px-3 py-2"
              value={query}
              onChange={e => setQuery(e.target.value)}
              required
            />
          </div>
          <div>
            <label className="block font-semibold mb-1 flex items-center gap-2">
              <span role="img" aria-label="pasta">📁</span> Pasta (ex: C:\Users\kaue\Downloads)
            </label>
            <input
              type="text"
              className="w-full border rounded px-3 py-2"
              value={folder}
              onChange={e => setFolder(e.target.value)}
              required
            />
          </div>
          <div>
            <label className="block font-semibold mb-1 flex items-center gap-2">
              <span role="img" aria-label="extensoes">📄</span> Extensões
            </label>
            <div className="flex gap-4">
              {EXT_OPTIONS.map(opt => (
                <label key={opt.value} className="flex items-center gap-1">
                  <input
                    type="checkbox"
                    checked={extensions.includes(opt.value)}
                    onChange={() => handleExtChange(opt.value)}
                  />
                  {opt.label}
                </label>
              ))}
            </div>
          </div>
          <button
            type="submit"
            className="bg-blue-600 text-white px-6 py-2 rounded font-semibold mt-2"
            disabled={loading}
          >
            {loading ? 'Buscando...' : 'Buscar'}
          </button>
        </form>
        <div className="mt-8">
          {error && <div className="text-red-600 mb-2">{error}</div>}
          {results.length > 0 ? (
            <ul className="space-y-4">
              {results.map((result, idx) => (
                <li key={idx} className="bg-gray-50 p-4 rounded shadow flex flex-col gap-2">
                  <div className="flex items-center gap-2">
                    <span className="text-gray-700 font-mono text-xs flex-1 truncate">{result.file_path}</span>
                    <button
                      onClick={() => handleOpenFile(result.file_path)}
                      className="ml-2 px-2 py-1 bg-blue-500 text-white rounded hover:bg-blue-700"
                    >
                      Abrir
                    </button>
                  </div>
                  <div className="text-green-700 text-sm font-mono">
                    {result.ia_response}
                  </div>
                </li>
              ))}
            </ul>
          ) : (
            !loading && (
              <div className="text-center text-gray-500 mt-8">
                Nenhum resultado encontrado<br />
                Tente uma busca diferente ou verifique se os arquivos foram indexados.
              </div>
            )
          )}
        </div>
      </div>
    </div>
  );
}

export default App;
