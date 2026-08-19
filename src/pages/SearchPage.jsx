import React, { useState } from 'react';
import { Search, RotateCcw, Sparkles, Filter, SlidersHorizontal } from 'lucide-react';
import { SampleCard } from '../components/SampleCard';
import { getApiUrl } from '../config';

export const SearchPage = ({ onOpenModal }) => {
  const [productType, setProductType] = useState('ALL');
  const [weave, setWeave] = useState('ALL');
  const [yarn, setYarn] = useState('ALL');
  const [blend, setBlend] = useState('ALL');
  const [finishType, setFinishType] = useState('ALL');
  const [gsmMin, setGsmMin] = useState('');
  const [gsmMax, setGsmMax] = useState('');
  const [feelTerms, setFeelTerms] = useState('');

  const [loading, setLoading] = useState(false);
  const [resultsData, setResultsData] = useState(null);
  const [error, setError] = useState('');

  const suggestChips = [
    'Soft Feel',
    'Shiny',
    'Crisp',
    'Stretchable',
    'Easy Care',
    'Anti Microbial',
  ];

  const handleChipClick = (term) => {
    if (!feelTerms) {
      setFeelTerms(term);
    } else if (!feelTerms.toLowerCase().includes(term.toLowerCase())) {
      setFeelTerms(`${feelTerms}, ${term}`);
    }
  };

  const handleReset = () => {
    setProductType('ALL');
    setWeave('ALL');
    setYarn('ALL');
    setBlend('ALL');
    setFinishType('ALL');
    setGsmMin('');
    setGsmMax('');
    setFeelTerms('');
    setResultsData(null);
    setError('');
  };

  const handleSearch = async (e) => {
    if (e) e.preventDefault();
    setLoading(true);
    setError('');
    try {
      const res = await fetch(getApiUrl('/api/search'), {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        credentials: 'include',
        body: JSON.stringify({
          product_type: productType,
          weave,
          yarn,
          blend,
          gsm_min: gsmMin,
          gsm_max: gsmMax,
          feel_terms: feelTerms,
        }),
      });


      if (!res.ok) throw new Error('Search failed');
      const data = await res.json();
      setResultsData(data);
    } catch (err) {
      setError('Error running search matching engine. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ maxWidth: '1200px', margin: '0 auto' }}>
      {/* Search Header */}
      <div style={{ marginBottom: '2rem' }}>
        <div style={{ fontSize: '0.8rem', color: 'var(--sand-500)', fontWeight: 700, textTransform: 'uppercase', letterSpacing: '0.12em', fontFamily: 'var(--font-heading)' }}>
          Intelligent Fabric Matcher
        </div>
        <h2 style={{ fontSize: '2.1rem', fontWeight: 800, color: '#FFFFFF', marginTop: '0.2rem', fontFamily: 'var(--font-heading)', letterSpacing: '-0.03em' }}>
          Search Samples by Buyer Requirements
        </h2>
        <p style={{ color: 'var(--text-muted)', fontSize: '0.95rem', marginTop: '0.3rem', fontFamily: 'var(--font-sans)' }}>
          Combine construction specs with natural performance & feel terms to get exact priority-ranked recommendations.
        </p>
      </div>

      {/* Filter Card */}
      <div
        className="glass-panel"
        style={{
          borderRadius: 'var(--radius-xl)',
          padding: '2rem',
          marginBottom: '2rem',
          borderTop: '3px solid var(--sand-500)',
        }}
      >
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.6rem', marginBottom: '1.5rem' }}>
          <SlidersHorizontal size={20} color="var(--sand-500)" />
          <h3 style={{ fontSize: '1.18rem', color: '#FFFFFF', fontWeight: 700, fontFamily: 'var(--font-heading)' }}>Search Parameters</h3>
        </div>

        <form onSubmit={handleSearch}>
          <div
            style={{
              display: 'grid',
              gridTemplateColumns: 'repeat(auto-fit, minmax(220px, 1fr))',
              gap: '1.2rem',
              marginBottom: '1.5rem',
            }}
          >
            <div>
              <label style={{ display: 'block', fontSize: '0.72rem', fontWeight: 700, textTransform: 'uppercase', color: 'var(--text-dim)', marginBottom: '0.4rem', letterSpacing: '0.05em' }}>
                Product Type
              </label>
              <select className="input-field" value={productType} onChange={(e) => setProductType(e.target.value)}>
                <option value="ALL">All Products</option>
                <option value="DYED">DYED</option>
                <option value="PRINT">PRINT</option>
                <option value="CHECKS">CHECKS</option>
                <option value="STRIPES">STRIPES</option>
                <option value="WHITE">WHITE</option>
                <option value="YD+PRINT">YD+PRINT</option>
                <option value="WHITE+PRINT">WHITE+PRINT</option>
                <option value="DYED+PRINT">DYED+PRINT</option>
                <option value="YD+PIGMENT PRINT">YD+PIGMENT PRINT</option>
              </select>
            </div>

            <div>
              <label style={{ display: 'block', fontSize: '0.72rem', fontWeight: 700, textTransform: 'uppercase', color: 'var(--text-dim)', marginBottom: '0.4rem', letterSpacing: '0.05em' }}>
                Weave
              </label>
              <select className="input-field" value={weave} onChange={(e) => setWeave(e.target.value)}>
                <option value="ALL">All Weaves</option>
                <option value="PLAIN">PLAIN</option>
                <option value="TWILL">TWILL</option>
                <option value="DOBBY">DOBBY</option>
                <option value="SATIN">SATIN</option>
              </select>
            </div>

            <div>
              <label style={{ display: 'block', fontSize: '0.72rem', fontWeight: 700, textTransform: 'uppercase', color: 'var(--text-dim)', marginBottom: '0.4rem', letterSpacing: '0.05em' }}>
                Yarn Type
              </label>
              <select className="input-field" value={yarn} onChange={(e) => setYarn(e.target.value)}>
                <option value="ALL">All Yarn Types</option>
                <option value="COMPACT">COMPACT</option>
                <option value="COMBED">COMBED</option>
                <option value="SLUB">SLUB</option>
                <option value="TFO">TFO</option>
                <option value="CARDED">CARDED</option>
              </select>
            </div>

            <div>
              <label style={{ display: 'block', fontSize: '0.72rem', fontWeight: 700, textTransform: 'uppercase', color: 'var(--text-dim)', marginBottom: '0.4rem', letterSpacing: '0.05em' }}>
                Composition / Blend
              </label>
              <select className="input-field" value={blend} onChange={(e) => setBlend(e.target.value)}>
                <option value="ALL">All Compositions / Blends</option>
                <option value="100% COTTON">100% COTTON</option>
                <option value="100% VISCOSE">100% VISCOSE</option>
                <option value="100% MODAL">100% MODAL</option>
                <option value="100% TENCEL">100% TENCEL</option>
                <option value="100% LINEN">100% LINEN</option>
                <option value="COTTON">COTTON (All Cotton & Blends)</option>
                <option value="VISCOSE">VISCOSE (All Viscose & Blends)</option>
                <option value="MODAL">MODAL (All Modal & Blends)</option>
                <option value="TENCEL">TENCEL (All Tencel & Blends)</option>
                <option value="LINEN">LINEN (All Linen & Blends)</option>
                <option value="LYCRA">LYCRA (All Lycra & Blends)</option>
                <option value="COTTON:LYCRA">COTTON / LYCRA</option>
                <option value="COTTON:VISCOSE">COTTON / VISCOSE</option>
                <option value="COTTON:MODAL">COTTON / MODAL</option>
                <option value="COTTON:LINEN">COTTON / LINEN</option>
                <option value="COTTON:TENCEL">COTTON / TENCEL</option>
                <option value="TENCEL:LINEN">TENCEL / LINEN</option>
              </select>
            </div>

            <div>
              <label style={{ display: 'block', fontSize: '0.72rem', fontWeight: 700, textTransform: 'uppercase', color: 'var(--text-dim)', marginBottom: '0.4rem', letterSpacing: '0.05em' }}>
                Finish Type
              </label>
              <select className="input-field" value={finishType} onChange={(e) => setFinishType(e.target.value)}>
                <option value="ALL">All Finish Types</option>
                <option value="SOFT TOUCH">SOFT TOUCH</option>
                <option value="COTTON SOFT FIN">COTTON SOFT FIN</option>
                <option value="NORMAL SOFT FIN">NORMAL SOFT FIN</option>
                <option value="PEACH FIN HAND">PEACH FIN HAND</option>
                <option value="EASY TO IRON">EASY TO IRON</option>
                <option value="BRUSHED">BRUSHED</option>
                <option value="ANTI MICROBIAL">ANTI MICROBIAL</option>
                <option value="EASY TO IRON+CALENDER">EASY TO IRON + CALENDER</option>
              </select>
            </div>

            <div>
              <label style={{ display: 'block', fontSize: '0.72rem', fontWeight: 700, textTransform: 'uppercase', color: 'var(--text-dim)', marginBottom: '0.4rem', letterSpacing: '0.05em' }}>
                GSM Min
              </label>
              <input
                type="number"
                className="input-field"
                placeholder="e.g., 100"
                value={gsmMin}
                onChange={(e) => setGsmMin(e.target.value)}
              />
            </div>

            <div>
              <label style={{ display: 'block', fontSize: '0.72rem', fontWeight: 700, textTransform: 'uppercase', color: 'var(--text-dim)', marginBottom: '0.4rem', letterSpacing: '0.05em' }}>
                GSM Max
              </label>
              <input
                type="number"
                className="input-field"
                placeholder="e.g., 200"
                value={gsmMax}
                onChange={(e) => setGsmMax(e.target.value)}
              />
            </div>
          </div>

          {/* Feel Terms Full-Width Field */}
          <div style={{ marginBottom: '1.5rem' }}>
            <label style={{ display: 'block', fontSize: '0.72rem', fontWeight: 700, textTransform: 'uppercase', color: 'var(--text-dim)', marginBottom: '0.4rem', letterSpacing: '0.05em' }}>
              Performance / Feel Terms (Natural Language Search)
            </label>
            <input
              type="text"
              className="input-field"
              placeholder="e.g., soft feel, shiny, stretchable, crisp"
              value={feelTerms}
              onChange={(e) => setFeelTerms(e.target.value)}
            />

            {/* Quick Suggest Chips */}
            <div style={{ display: 'flex', flexWrap: 'wrap', gap: '0.5rem', marginTop: '0.8rem' }}>
              <span style={{ fontSize: '0.75rem', color: 'var(--text-dim)', alignSelf: 'center', fontWeight: 600 }}>Quick Add:</span>
              {suggestChips.map((chip) => (
                <button
                  type="button"
                  key={chip}
                  onClick={() => handleChipClick(chip)}
                  style={{
                    background: 'rgba(255, 255, 255, 0.05)',
                    border: '1px solid var(--border-subtle)',
                    color: 'var(--text-muted)',
                    borderRadius: '20px',
                    padding: '0.25rem 0.75rem',
                    fontSize: '0.78rem',
                    fontWeight: 500,
                    cursor: 'pointer',
                    transition: 'all 0.2s ease',
                  }}
                  onMouseEnter={(e) => {
                    e.currentTarget.style.borderColor = 'var(--gold-400)';
                    e.currentTarget.style.color = '#FFF';
                  }}
                  onMouseLeave={(e) => {
                    e.currentTarget.style.borderColor = 'var(--border-subtle)';
                    e.currentTarget.style.color = 'var(--text-muted)';
                  }}
                >
                  + {chip}
                </button>
              ))}
            </div>
          </div>

          {/* Buttons */}
          <div style={{ display: 'flex', gap: '1rem', justifyContent: 'flex-end' }}>
            <button type="button" onClick={handleReset} className="btn-secondary">
              <RotateCcw size={16} />
              <span>Clear</span>
            </button>
            <button type="submit" className="btn-primary" disabled={loading}>
              <Search size={18} />
              <span>{loading ? 'Searching...' : 'Search Fabric Samples'}</span>
            </button>
          </div>
        </form>
      </div>

      {/* Loading state */}
      {loading && (
        <div style={{ textContent: 'center', padding: '3rem', textAlign: 'center', color: 'var(--gold-400)' }}>
          <div style={{ display: 'inline-block', width: '36px', height: '36px', border: '3px solid rgba(245,158,11,0.2)', borderTopColor: '#F59E0B', borderRadius: '50%', animation: 'spin 0.8s linear infinite' }} />
          <p style={{ marginTop: '1rem', color: 'var(--text-muted)', fontSize: '0.9rem' }}>Matching priority rules against database samples...</p>
        </div>
      )}

      {error && (
        <div style={{ padding: '1rem', background: 'rgba(153,27,27,0.2)', border: '1px solid #EF4444', color: '#F87171', borderRadius: 'var(--radius-md)', marginBottom: '1.5rem' }}>
          {error}
        </div>
      )}

      {/* Search Results */}
      {resultsData && !loading && (
        <div className="animate-fade-in">
          <div
            style={{
              background: 'linear-gradient(135deg, rgba(245, 158, 11, 0.12) 0%, rgba(30, 41, 59, 0.6) 100%)',
              borderLeft: '4px solid var(--gold-400)',
              borderRadius: 'var(--radius-lg)',
              padding: '1.4rem 1.8rem',
              marginBottom: '2rem',
              border: '1px solid rgba(245, 158, 11, 0.25)',
              display: 'flex',
              justifyContent: 'space-between',
              alignItems: 'center',
              flexWrap: 'wrap',
              gap: '1rem',
            }}
          >
            <div>
              <h3 style={{ fontSize: '1.3rem', color: '#FFFFFF', fontWeight: 700 }}>
                {resultsData.total_count} sample(s) found
              </h3>
              {resultsData.standard_terms && resultsData.standard_terms.length > 0 ? (
                <div style={{ marginTop: '0.6rem' }}>
                  <div style={{ fontSize: '0.78rem', color: 'var(--text-dim)', fontWeight: 600, uppercase: true }}>
                    Detected Standard Properties:
                  </div>
                  <div style={{ display: 'flex', gap: '0.5rem', flexWrap: 'wrap', marginTop: '0.3rem' }}>
                    {resultsData.standard_terms.map((t) => (
                      <span
                        key={t}
                        style={{
                          background: 'linear-gradient(135deg, var(--gold-500), #B45309)',
                          color: '#FFFFFF',
                          padding: '0.2rem 0.7rem',
                          borderRadius: '12px',
                          fontSize: '0.78rem',
                          fontWeight: 700,
                        }}
                      >
                        {t}
                      </span>
                    ))}
                  </div>
                </div>
              ) : null}
            </div>

            {resultsData.standard_terms && resultsData.standard_terms.length > 0 && (
              <div
                style={{
                  display: 'flex',
                  alignItems: 'center',
                  gap: '0.4rem',
                  fontSize: '0.82rem',
                  color: 'var(--gold-400)',
                  background: 'rgba(15, 23, 42, 0.6)',
                  padding: '0.5rem 1rem',
                  borderRadius: '20px',
                  border: '1px solid rgba(245, 158, 11, 0.3)',
                }}
              >
                <Sparkles size={16} />
                <span>Priority Engine Ranked — Best Match First</span>
              </div>
            )}
          </div>

          {/* Cards Grid */}
          {resultsData.results.length === 0 ? (
            <div style={{ textAlign: 'center', padding: '4rem', color: 'var(--text-muted)', background: 'rgba(30,41,59,0.3)', borderRadius: 'var(--radius-xl)' }}>
              <p style={{ fontSize: '1.1rem', fontWeight: 600 }}>No samples matched your exact requirements.</p>
              <p style={{ fontSize: '0.88rem', marginTop: '0.4rem' }}>Try broadening your search parameters or composition blend.</p>
            </div>
          ) : (
            <div
              style={{
                display: 'grid',
                gridTemplateColumns: 'repeat(auto-fill, minmax(270px, 1fr))',
                gap: '1.6rem',
              }}
            >
              {resultsData.results.map((sample, idx) => {
                const hasRank = resultsData.standard_terms && resultsData.standard_terms.length > 0;
                const rankInfo = hasRank ? { rank: sample.rank || idx + 1 } : null;

                return (
                  <SampleCard
                    key={sample.sample_no}
                    sample={sample}
                    onOpenModal={onOpenModal}
                    rankInfo={rankInfo}
                  />
                );
              })}
            </div>
          )}
        </div>
      )}
    </div>
  );
};
