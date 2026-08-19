import React, { useState } from 'react';
import { Search, RotateCcw, Sparkles, SlidersHorizontal } from 'lucide-react';
import { SampleCard } from '../components/SampleCard';
import { getApiUrl } from '../config';
import { filterSamplesLocally } from '../data/samplesData';

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

  const suggestChips = ['Soft Feel', 'Shiny', 'Crisp', 'Stretchable', 'Easy Care', 'Anti Microbial'];

  const handleChipClick = (term) => {
    if (!feelTerms) setFeelTerms(term);
    else if (!feelTerms.toLowerCase().includes(term.toLowerCase())) setFeelTerms(`${feelTerms}, ${term}`);
  };

  const handleReset = () => {
    setProductType('ALL'); setWeave('ALL'); setYarn('ALL');
    setBlend('ALL'); setFinishType('ALL'); setGsmMin(''); setGsmMax(''); setFeelTerms('');
    setResultsData(null); setError('');
  };

  const handleSearch = async (e) => {
    if (e) e.preventDefault();
    setLoading(true); setError('');
    const searchParams = { product_type: productType, weave, yarn, blend, finish: finishType, finish_type: finishType, gsm_min: gsmMin, gsm_max: gsmMax, feel_terms: feelTerms };
    try {
      const res = await fetch(getApiUrl('/api/search'), {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        credentials: 'include',
        body: JSON.stringify(searchParams),
      });
      const contentType = res.headers.get('content-type') || '';
      if (!res.ok || contentType.includes('text/html') || res.redirected) {
        setResultsData(filterSamplesLocally(searchParams)); return;
      }
      const data = await res.json();
      setResultsData(data);
    } catch (err) {
      setResultsData(filterSamplesLocally(searchParams));
    } finally {
      setLoading(false);
    }
  };

  const fieldLabel = (text) => (
    <label style={{ display: 'block', fontSize: '10px', fontWeight: 700, textTransform: 'uppercase', letterSpacing: '0.1em', color: 'var(--text-dim)', marginBottom: '0.45rem' }}>
      {text}
    </label>
  );

  return (
    <div style={{ maxWidth: '1200px', margin: '0 auto' }}>
      {/* Editorial page header */}
      <div
        style={{
          paddingBottom: '2rem',
          marginBottom: '2rem',
          borderBottom: '1px solid var(--border)',
        }}
      >
        <h2
          style={{
            fontSize: 'clamp(36px, 5vw, 64px)',
            fontWeight: 900,
            letterSpacing: '-0.045em',
            lineHeight: 0.95,
            color: 'var(--charcoal)',
          }}
        >
          Smart Search
        </h2>
      </div>

      {/* Filter panel */}
      <div
        style={{
          background: 'var(--white)',
          border: '1.5px solid var(--border)',
          borderRadius: 'var(--radius-xl)',
          overflow: 'hidden',
          marginBottom: '2rem',
        }}
      >
        {/* Panel header */}
        <div
          style={{
            display: 'flex', alignItems: 'center', gap: '0.6rem',
            padding: '1.25rem 1.75rem',
            borderBottom: '1px solid var(--border)',
            background: 'var(--bg-surface)',
          }}
        >
          <SlidersHorizontal size={17} color="var(--text-dim)" />
          <span style={{ fontSize: '0.88rem', fontWeight: 700, color: 'var(--charcoal)', letterSpacing: '-0.02em' }}>
            Search Parameters
          </span>
        </div>

        <div style={{ padding: '1.75rem' }}>
          <form onSubmit={handleSearch}>
            <div
              style={{
                display: 'grid',
                gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))',
                gap: '1.25rem',
                marginBottom: '1.5rem',
              }}
            >
              <div>
                {fieldLabel('Product Type')}
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
                {fieldLabel('Weave')}
                <select className="input-field" value={weave} onChange={(e) => setWeave(e.target.value)}>
                  <option value="ALL">All Weaves</option>
                  <option value="PLAIN">PLAIN</option>
                  <option value="TWILL">TWILL</option>
                  <option value="DOBBY">DOBBY</option>
                  <option value="SATIN">SATIN</option>
                </select>
              </div>

              <div>
                {fieldLabel('Yarn Type')}
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
                {fieldLabel('Composition / Blend')}
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
                {fieldLabel('Finish Type')}
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
                {fieldLabel('GSM Min')}
                <input type="number" className="input-field" placeholder="e.g., 100" value={gsmMin} onChange={(e) => setGsmMin(e.target.value)} />
              </div>

              <div>
                {fieldLabel('GSM Max')}
                <input type="number" className="input-field" placeholder="e.g., 200" value={gsmMax} onChange={(e) => setGsmMax(e.target.value)} />
              </div>
            </div>

            {/* Feel terms */}
            <div style={{ marginBottom: '1.5rem' }}>
              {fieldLabel('Performance / Feel Terms (Natural Language)')}
              <input
                type="text"
                className="input-field"
                placeholder="e.g., soft feel, shiny, stretchable, crisp"
                value={feelTerms}
                onChange={(e) => setFeelTerms(e.target.value)}
              />

              {/* Chips */}
              <div style={{ display: 'flex', flexWrap: 'wrap', gap: '0.4rem', marginTop: '0.75rem', alignItems: 'center' }}>
                <span style={{ fontSize: '10px', color: 'var(--text-dim)', fontWeight: 700, textTransform: 'uppercase', letterSpacing: '0.08em' }}>Quick Add:</span>
                {suggestChips.map((chip) => (
                  <button
                    type="button"
                    key={chip}
                    onClick={() => handleChipClick(chip)}
                    style={{
                      background: 'transparent',
                      border: '1.5px solid var(--border-mid)',
                      color: 'var(--text-muted)',
                      borderRadius: 'var(--radius-pill)',
                      padding: '3px 12px',
                      fontSize: '0.78rem',
                      fontWeight: 500,
                      cursor: 'pointer',
                      transition: 'all 0.18s ease',
                      fontFamily: 'var(--font-sans)',
                    }}
                    onMouseEnter={(e) => {
                      e.currentTarget.style.background = 'var(--charcoal)';
                      e.currentTarget.style.borderColor = 'var(--charcoal)';
                      e.currentTarget.style.color = 'var(--white)';
                    }}
                    onMouseLeave={(e) => {
                      e.currentTarget.style.background = 'transparent';
                      e.currentTarget.style.borderColor = 'var(--border-mid)';
                      e.currentTarget.style.color = 'var(--text-muted)';
                    }}
                  >
                    + {chip}
                  </button>
                ))}
              </div>
            </div>

            {/* Actions */}
            <div style={{ display: 'flex', gap: '0.75rem', justifyContent: 'flex-end', paddingTop: '1.25rem', borderTop: '1px solid var(--border)' }}>
              <button type="button" onClick={handleReset} className="btn-secondary" style={{ gap: '0.4rem' }}>
                <RotateCcw size={15} />
                <span>Clear All</span>
              </button>
              <button type="submit" className="btn-primary-red" disabled={loading} style={{ gap: '0.5rem', minWidth: '180px' }}>
                <Search size={16} />
                <span>{loading ? 'Searching…' : 'Search Samples'}</span>
              </button>
            </div>
          </form>
        </div>
      </div>

      {/* Loading */}
      {loading && (
        <div style={{ textAlign: 'center', padding: '4rem 2rem' }}>
          <div style={{ display: 'inline-block', width: '32px', height: '32px', border: '2.5px solid rgba(14,14,14,0.1)', borderTopColor: 'var(--charcoal)', borderRadius: '50%', animation: 'spin 0.75s linear infinite' }} />
          <p style={{ marginTop: '1rem', fontSize: '0.88rem', color: 'var(--text-muted)', fontWeight: 500 }}>
            Matching priority rules against database samples…
          </p>
        </div>
      )}

      {error && (
        <div style={{ padding: '0.9rem 1.1rem', background: 'rgba(232,51,26,0.07)', border: '1.5px solid rgba(232,51,26,0.2)', color: 'var(--red)', borderRadius: 'var(--radius-md)', marginBottom: '1.5rem', fontSize: '0.88rem', fontWeight: 600 }}>
          {error}
        </div>
      )}

      {/* Results */}
      {resultsData && !loading && (
        <div className="animate-fade-in">
          {/* Results header */}
          <div
            style={{
              padding: '1.25rem 1.5rem',
              background: 'var(--white)',
              border: '1.5px solid var(--border)',
              borderRadius: 'var(--radius-lg)',
              marginBottom: '1.5rem',
              display: 'flex',
              justifyContent: 'space-between',
              alignItems: 'center',
              flexWrap: 'wrap',
              gap: '1rem',
            }}
          >
            <div>
              <div style={{ fontSize: '1.5rem', fontWeight: 900, letterSpacing: '-0.04em', color: 'var(--charcoal)' }}>
                {resultsData.total_count} match{resultsData.total_count !== 1 ? 'es' : ''} found
              </div>
              {resultsData.standard_terms && resultsData.standard_terms.length > 0 && (
                <div style={{ display: 'flex', gap: '0.4rem', flexWrap: 'wrap', marginTop: '0.5rem', alignItems: 'center' }}>
                  <span style={{ fontSize: '10px', color: 'var(--text-dim)', fontWeight: 700, textTransform: 'uppercase', letterSpacing: '0.08em' }}>Matched:</span>
                  {resultsData.standard_terms.map((t) => (
                    <span
                      key={t}
                      style={{
                        background: 'var(--charcoal)', color: 'var(--white)',
                        padding: '2px 10px', borderRadius: 'var(--radius-pill)',
                        fontSize: '11px', fontWeight: 700,
                      }}
                    >
                      {t}
                    </span>
                  ))}
                </div>
              )}
            </div>

            {resultsData.standard_terms && resultsData.standard_terms.length > 0 && (
              <div style={{ display: 'flex', alignItems: 'center', gap: '0.4rem', fontSize: '0.82rem', color: 'var(--text-muted)', fontWeight: 600 }}>
                <Sparkles size={14} color="var(--red)" />
                <span>Priority Engine Ranked</span>
              </div>
            )}
          </div>

          {resultsData.results.length === 0 ? (
            <div
              style={{
                textAlign: 'center', padding: '4rem 2rem',
                border: '1.5px solid var(--border)',
                borderRadius: 'var(--radius-xl)',
                background: 'var(--white)',
              }}
            >
              <p style={{ fontSize: '1.1rem', fontWeight: 700, color: 'var(--charcoal)', letterSpacing: '-0.02em' }}>
                No samples matched.
              </p>
              <p style={{ fontSize: '0.88rem', color: 'var(--text-muted)', marginTop: '0.4rem' }}>
                Try broadening your parameters or changing the composition blend.
              </p>
            </div>
          ) : (
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(265px, 1fr))', gap: '1.25rem' }}>
              {resultsData.results.map((sample, idx) => {
                const hasRank = resultsData.standard_terms && resultsData.standard_terms.length > 0;
                return (
                  <SampleCard
                    key={sample.sample_no}
                    sample={sample}
                    onOpenModal={onOpenModal}
                    rankInfo={hasRank ? { rank: sample.rank || idx + 1 } : null}
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
