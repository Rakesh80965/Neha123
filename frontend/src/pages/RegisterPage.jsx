import React, { useState } from 'react';
import { ArrowRight, Lock, AlertCircle, User } from 'lucide-react';
import { useAuth } from '../context/AuthContext';

const BRAND_OPTIONS = [
  'Select Brand',
  'Allen Solly',
  'Indian Terrain',
  'Louis Philippe',
  'Van Heusen',
  'Blackberrys',
  'Pepe Jeans London',
  'Lee Cooper',
  'Wrogn',
  'Parx',
  'Reliance Trends',
  'ColorPlus',
  'Jockey',
  'Max',
  'Scullers',
  'Peter England',
  'DNMX',
  'Buffalo',
  'Bare Denim',
  'WLS',
  'Aditya Birla Group',
  'Izod',
  'Indigo Nation',
  'John Players',
  'Mufti',
  'Park Avenue',
  'Boss (Hugo Boss)',
  'Camaïeu',
  'Mango',
  'Esprit',
  'Lee',
  's.Oliver',
  'Zara',
  'Matalan',
  'Pull&Bear',
  'Celio*',
  'Next',
  'Tommy Hilfiger',
  'RB Sellars',
  "Levi's",
  'CK (Calvin Klein)',
  'Zalando',
  'Giovanni Galli',
  'Wrangler',
  'Diesel',
  "Sainsbury's",
  'M&S (Marks & Spencer)',
  'Gant',
  'United Colors of Benetton',
  'Scotch & Soda',
  'Hackett London',
  'H&M',
  'Nike',
  'Adidas',
  'Puma',
  'Uniqlo',
  'Gap',
  'Gucci',
  'Prada',
  'Other (Custom)',
];

const COUNTRY_OPTIONS = [
  'Select Country',
  'Spain',
  'India',
  'United States',
  'United Kingdom',
  'Germany',
  'France',
  'Italy',
  'Turkey',
  'Bangladesh',
  'China',
  'Vietnam',
  'Japan',
  'Brazil',
  'Canada',
  'Australia',
  'United Arab Emirates',
  'Other',
];

export const RegisterPage = ({ onSwitchToLogin }) => {
  const { register } = useAuth();
  
  // Auto-generate a Buyer ID formatted as B-XXXXX
  const [buyerId] = useState(() => 'B-' + String(Math.floor(10000 + Math.random() * 90000)));

  // All initial input states empty by default
  const [buyerName, setBuyerName] = useState('');
  const [brandName, setBrandName] = useState('Select Brand');
  const [customBrand, setCustomBrand] = useState('');
  const [company, setCompany] = useState('');
  const [country, setCountry] = useState('Select Country');
  const [contactPerson, setContactPerson] = useState('');
  const [email, setEmail] = useState('');
  const [phoneNumber, setPhoneNumber] = useState('');

  const [password, setPassword] = useState('');
  const [confirm, setConfirm] = useState('');
  const [error, setError] = useState('');
  const [submitting, setSubmitting] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');

    const effectiveBrand = brandName === 'Other (Custom)' ? customBrand : brandName;

    if (!effectiveBrand.trim() || effectiveBrand === 'Select Brand') { setError('Brand Name is required'); return; }
    if (!country || country === 'Select Country') { setError('Country selection is required'); return; }
    if (!email.trim()) { setError('Email is required'); return; }
    if (password !== confirm) { setError('Passwords do not match'); return; }
    if (password.length < 6) { setError('Password must be at least 6 characters'); return; }

    setSubmitting(true);
    try {
      await register({
        email: email.trim(),
        password,
        confirm,
        buyerName: effectiveBrand.trim(),
        brandName: effectiveBrand.trim(),
        company,
        country,
        contactPerson,
        phoneNumber,
        buyerId,
      });
    } catch (err) {
      setError(err.message || 'Registration failed');
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div
      style={{
        minHeight: '100vh',
        background: '#f8fafc',
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        padding: '2rem 1.5rem 4rem',
        fontFamily: 'Inter, system-ui, -apple-system, sans-serif',
      }}
    >
      {/* Top Header */}
      <div style={{ maxWidth: '960px', width: '100%', marginBottom: '1.8rem' }}>
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '0.75rem' }}>
          <div>
            <h1
              style={{
                fontSize: '1.85rem',
                fontWeight: 800,
                color: '#0f172a',
                letterSpacing: '-0.025em',
                marginBottom: '0.25rem',
              }}
            >
              Buyer Enquiry Registration
            </h1>
            <p style={{ fontSize: '0.92rem', color: '#64748b' }}>
              Register new buyer enquiry and requirement details
            </p>
          </div>

          <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
            <button
              onClick={onSwitchToLogin}
              style={{
                padding: '0.55rem 1.25rem',
                borderRadius: '8px',
                border: '1px solid #cbd5e1',
                background: '#ffffff',
                color: '#334155',
                fontSize: '0.88rem',
                fontWeight: 600,
                cursor: 'pointer',
                transition: 'all 0.2s',
              }}
            >
              Cancel / Back to Sign In
            </button>
          </div>
        </div>
      </div>

      {/* Main Registration Form Container */}
      <div
        style={{
          maxWidth: '960px',
          width: '100%',
          background: '#ffffff',
          borderRadius: '16px',
          boxShadow: '0 4px 20px -2px rgba(15, 23, 42, 0.06), 0 2px 6px -1px rgba(15, 23, 42, 0.04)',
          border: '1px solid #e2e8f0',
          padding: '2.25rem',
        }}
      >
        {error && (
          <div
            style={{
              marginBottom: '1.5rem',
              padding: '0.88rem 1.1rem',
              borderRadius: '10px',
              background: '#fef2f2',
              border: '1px solid #fecaca',
              color: '#dc2626',
              fontSize: '0.88rem',
              display: 'flex',
              alignItems: 'center',
              gap: '0.6rem',
              fontWeight: 500,
            }}
          >
            <AlertCircle size={18} style={{ flexShrink: 0 }} />
            <span>{error}</span>
          </div>
        )}

        <form onSubmit={handleSubmit}>
          {/* Section 1 Card */}
          <div
            style={{
              background: '#ffffff',
              borderRadius: '12px',
              border: '1px solid #f1f5f9',
              padding: '1.5rem',
              boxShadow: '0 1px 3px rgba(0,0,0,0.02)',
              marginBottom: '2rem',
            }}
          >
            {/* Section Title Header */}
            <div
              style={{
                display: 'flex',
                alignItems: 'center',
                gap: '0.85rem',
                marginBottom: '1.75rem',
                paddingBottom: '0.85rem',
                borderBottom: '1.5px solid #f1f5f9',
              }}
            >
              <div
                style={{
                  width: '38px',
                  height: '38px',
                  borderRadius: '50%',
                  background: '#eff6ff',
                  color: '#2563eb',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  fontWeight: 700,
                }}
              >
                <User size={20} />
              </div>
              <h2 style={{ fontSize: '1.15rem', fontWeight: 700, color: '#1e293b' }}>
                1. Buyer Information
              </h2>
            </div>

            {/* Fields Grid */}
            <div
              style={{
                display: 'grid',
                gridTemplateColumns: 'repeat(auto-fit, minmax(260px, 1fr))',
                gap: '1.35rem 1.5rem',
              }}
            >
              {/* Brand Name */}
              <div>
                <label style={{ display: 'block', fontSize: '0.82rem', fontWeight: 600, color: '#334155', marginBottom: '0.45rem' }}>
                  Brand Name <span style={{ color: '#ef4444' }}>*</span>
                </label>
                <select
                  value={brandName}
                  onChange={(e) => setBrandName(e.target.value)}
                  style={{
                    width: '100%',
                    padding: '0.7rem 0.9rem',
                    borderRadius: '8px',
                    border: '1.5px solid #cbd5e1',
                    fontSize: '0.92rem',
                    background: '#ffffff',
                    outline: 'none',
                    boxSizing: 'border-box',
                  }}
                >
                  {BRAND_OPTIONS.map((b) => (
                    <option key={b} value={b}>{b}</option>
                  ))}
                </select>
                {brandName === 'Other (Custom)' && (
                  <input
                    type="text"
                    required
                    placeholder="Enter custom brand name"
                    value={customBrand}
                    onChange={(e) => setCustomBrand(e.target.value)}
                    style={{
                      width: '100%',
                      marginTop: '0.5rem',
                      padding: '0.65rem 0.9rem',
                      borderRadius: '8px',
                      border: '1.5px solid #cbd5e1',
                      fontSize: '0.88rem',
                      boxSizing: 'border-box',
                    }}
                  />
                )}
              </div>

              {/* Company */}
              <div>
                <label style={{ display: 'block', fontSize: '0.82rem', fontWeight: 600, color: '#334155', marginBottom: '0.45rem' }}>
                  Company
                </label>
                <input
                  type="text"
                  value={company}
                  onChange={(e) => setCompany(e.target.value)}
                  placeholder="e.g. Inditex"
                  style={{
                    width: '100%',
                    padding: '0.7rem 0.9rem',
                    borderRadius: '8px',
                    border: '1.5px solid #cbd5e1',
                    fontSize: '0.92rem',
                    outline: 'none',
                    boxSizing: 'border-box',
                  }}
                />
              </div>

              {/* Country */}
              <div>
                <label style={{ display: 'block', fontSize: '0.82rem', fontWeight: 600, color: '#334155', marginBottom: '0.45rem' }}>
                  Country <span style={{ color: '#ef4444' }}>*</span>
                </label>
                <select
                  value={country}
                  onChange={(e) => setCountry(e.target.value)}
                  style={{
                    width: '100%',
                    padding: '0.7rem 0.9rem',
                    borderRadius: '8px',
                    border: '1.5px solid #cbd5e1',
                    fontSize: '0.92rem',
                    background: '#ffffff',
                    outline: 'none',
                    boxSizing: 'border-box',
                  }}
                >
                  {COUNTRY_OPTIONS.map((c) => (
                    <option key={c} value={c}>{c}</option>
                  ))}
                </select>
              </div>

              {/* Contact Person */}
              <div>
                <label style={{ display: 'block', fontSize: '0.82rem', fontWeight: 600, color: '#334155', marginBottom: '0.45rem' }}>
                  Contact Person
                </label>
                <input
                  type="text"
                  value={contactPerson}
                  onChange={(e) => setContactPerson(e.target.value)}
                  placeholder="e.g. Mr. David Garcia"
                  style={{
                    width: '100%',
                    padding: '0.7rem 0.9rem',
                    borderRadius: '8px',
                    border: '1.5px solid #cbd5e1',
                    fontSize: '0.92rem',
                    outline: 'none',
                    boxSizing: 'border-box',
                  }}
                />
              </div>

              {/* Email */}
              <div>
                <label style={{ display: 'block', fontSize: '0.82rem', fontWeight: 600, color: '#334155', marginBottom: '0.45rem' }}>
                  Email <span style={{ color: '#ef4444' }}>*</span>
                </label>
                <input
                  type="email"
                  required
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  placeholder="e.g. david.garcia@zara.com"
                  style={{
                    width: '100%',
                    padding: '0.7rem 0.9rem',
                    borderRadius: '8px',
                    border: '1.5px solid #cbd5e1',
                    fontSize: '0.92rem',
                    outline: 'none',
                    boxSizing: 'border-box',
                  }}
                />
              </div>

              {/* Phone Number */}
              <div>
                <label style={{ display: 'block', fontSize: '0.82rem', fontWeight: 600, color: '#334155', marginBottom: '0.45rem' }}>
                  Phone Number
                </label>
                <input
                  type="text"
                  value={phoneNumber}
                  onChange={(e) => setPhoneNumber(e.target.value)}
                  placeholder="e.g. +34 612 345 678"
                  style={{
                    width: '100%',
                    padding: '0.7rem 0.9rem',
                    borderRadius: '8px',
                    border: '1.5px solid #cbd5e1',
                    fontSize: '0.92rem',
                    outline: 'none',
                    boxSizing: 'border-box',
                  }}
                />
              </div>

              {/* Buyer ID */}
              <div>
                <label style={{ display: 'block', fontSize: '0.82rem', fontWeight: 600, color: '#64748b', marginBottom: '0.45rem' }}>
                  Buyer ID
                </label>
                <input
                  type="text"
                  readOnly
                  disabled
                  value={buyerId}
                  style={{
                    width: '100%',
                    padding: '0.7rem 0.9rem',
                    borderRadius: '8px',
                    border: '1.5px solid #e2e8f0',
                    background: '#f8fafc',
                    color: '#475569',
                    fontSize: '0.92rem',
                    fontWeight: 600,
                    boxSizing: 'border-box',
                  }}
                />
              </div>
            </div>
          </div>

          {/* Account Credentials Card */}
          <div
            style={{
              background: '#f8fafc',
              borderRadius: '12px',
              border: '1px solid #e2e8f0',
              padding: '1.5rem',
              marginBottom: '2rem',
            }}
          >
            <div
              style={{
                display: 'flex',
                alignItems: 'center',
                gap: '0.65rem',
                marginBottom: '1.25rem',
              }}
            >
              <Lock size={18} color="#334155" />
              <h3 style={{ fontSize: '1rem', fontWeight: 700, color: '#1e293b' }}>
                Account Password & Credentials
              </h3>
            </div>

            <div
              style={{
                display: 'grid',
                gridTemplateColumns: 'repeat(auto-fit, minmax(260px, 1fr))',
                gap: '1.25rem',
              }}
            >
              <div>
                <label style={{ display: 'block', fontSize: '0.82rem', fontWeight: 600, color: '#334155', marginBottom: '0.45rem' }}>
                  Password <span style={{ color: '#ef4444' }}>*</span>
                </label>
                <input
                  type="password"
                  required
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  placeholder="At least 6 characters"
                  style={{
                    width: '100%',
                    padding: '0.7rem 0.9rem',
                    borderRadius: '8px',
                    border: '1.5px solid #cbd5e1',
                    fontSize: '0.92rem',
                    boxSizing: 'border-box',
                  }}
                />
              </div>

              <div>
                <label style={{ display: 'block', fontSize: '0.82rem', fontWeight: 600, color: '#334155', marginBottom: '0.45rem' }}>
                  Confirm Password <span style={{ color: '#ef4444' }}>*</span>
                </label>
                <input
                  type="password"
                  required
                  value={confirm}
                  onChange={(e) => setConfirm(e.target.value)}
                  placeholder="Confirm password"
                  style={{
                    width: '100%',
                    padding: '0.7rem 0.9rem',
                    borderRadius: '8px',
                    border: '1.5px solid #cbd5e1',
                    fontSize: '0.92rem',
                    boxSizing: 'border-box',
                  }}
                />
              </div>
            </div>
          </div>

          {/* Form Action Controls */}
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
            <div style={{ fontSize: '0.88rem', color: '#64748b' }}>
              Already registered?{' '}
              <button
                type="button"
                onClick={onSwitchToLogin}
                style={{
                  background: 'none',
                  border: 'none',
                  color: '#2563eb',
                  fontWeight: 700,
                  cursor: 'pointer',
                  fontSize: '0.88rem',
                  textDecoration: 'underline',
                }}
              >
                Sign in here
              </button>
            </div>

            <button
              type="submit"
              disabled={submitting}
              style={{
                padding: '0.85rem 2.25rem',
                borderRadius: '10px',
                background: submitting ? '#94a3b8' : 'linear-gradient(135deg, #1e293b, #0f172a)',
                color: '#ffffff',
                fontSize: '0.95rem',
                fontWeight: 700,
                border: 'none',
                cursor: submitting ? 'not-allowed' : 'pointer',
                display: 'inline-flex',
                alignItems: 'center',
                gap: '0.6rem',
                boxShadow: '0 4px 12px rgba(15, 23, 42, 0.15)',
                transition: 'all 0.2s',
              }}
            >
              <span>{submitting ? 'Registering Buyer Account…' : 'Register Buyer Account'}</span>
              <ArrowRight size={18} />
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default RegisterPage;
